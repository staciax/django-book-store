from __future__ import annotations

import importlib.util
import inspect
import re
from abc import ABC, abstractmethod
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, get_type_hints  # noqa: UP035

from django.shortcuts import render as django_render
from django.urls import path, resolve

from ._get_frame import get_frame

__all__ = (
    'AppRouter',
    'get_page_template',
    'render',
)

if TYPE_CHECKING:
    from types import ModuleType

    from django.http.request import HttpRequest
    from django.http.response import HttpResponse
    from django.urls.resolvers import URLPattern

    from .metadata import Metadata

PATH_IGNORE_PREFIXES = ('(', '_')  # group, and private segments


def _get_route(
    path: Path,
    func: Callable[..., Any],
    *,
    trailing_slash: bool = True,
) -> str:
    """
    Constructs a route string based on the given path and function.
    """
    parameters = []
    func_type_hints = get_type_hints(func)
    for segment in path.parts:
        if segment.startswith(PATH_IGNORE_PREFIXES):
            continue

        if segment.startswith('[') and segment.endswith(']'):
            parameter_name = segment[1:-1]
            parameter_type = func_type_hints.get(parameter_name, str)
            parameter = f'<{parameter_type.__name__}:{parameter_name}>'
            parameters.append(parameter)
        else:
            parameters.append(segment)

    route = '/'.join(parameters)
    if trailing_slash and route and not route.endswith('/'):
        route += '/'

    return route


def import_module_from_path(fp: Path) -> ModuleType:
    """
    Import a module from the given file path.
    """
    spec = importlib.util.spec_from_file_location('module', fp)
    if spec is None:
        raise ImportError(f"Can't import module from {fp}")
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(f"Can't import module from {fp}")
    spec.loader.exec_module(module)
    return module


class BaseRouter(ABC):
    def __init__(self) -> None:
        self.app_router_paths: list[Path] = []

    def include_app(self, app_name: str, /, *, app_dir: bool = True) -> None:
        """
        Includes an app in the router.
        """
        app_path = Path(app_name).resolve()

        if not app_path.exists():
            raise FileNotFoundError(f'No app directory found in {app_name}')

        router_path = app_path.joinpath('routes')
        if not router_path.exists():
            raise FileNotFoundError(f'No routes directory found in {app_name}')

        if app_dir and router_path.joinpath(app_name).exists():
            router_path = router_path.joinpath(app_name)

        self.app_router_paths.append(router_path)

        # invalidate the urls cache
        if hasattr(self, '_urls'):
            del self._urls

    @abstractmethod
    def get_urls(self) -> list[URLPattern]:
        """Return a list of URL patterns."""

    @property
    def urls(self) -> list[URLPattern]:
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls


class AppRouter(BaseRouter):
    def __init__(
        self,
        trailing_slash: bool = True,
    ) -> None:
        super().__init__()
        self.trailing_slash = trailing_slash

    def get_urls(self) -> list[URLPattern]:
        """
        Return a list of URL Pattern for the app router.
        """
        urls = []

        for route_path in self.app_router_paths:
            page_files = route_path.glob(r'**/page.py')
            for page_file in page_files:
                module = import_module_from_path(page_file)

                # TODO: Future features
                # - Add support custom method name
                if method := getattr(module, 'page', None):
                    file_path = page_file.relative_to(route_path).parent
                    route = _get_route(
                        file_path,
                        method,
                        trailing_slash=self.trailing_slash,
                    )
                    urls.append(
                        path(
                            route,
                            method,
                            name=method.__doc__,
                        )
                    )

        return urls


@lru_cache
def get_view_module_from_request_path(request_path: str) -> str:
    func = resolve(request_path).func
    func = inspect.unwrap(func)
    fp = inspect.getfile(func)  # func.__code__.co_filename

    return fp


@lru_cache
def get_page_template(fp: str, *, filename: str = 'page.html') -> str:
    template_path = Path(fp).resolve()
    template_path = template_path.parent / filename

    routes = Path()
    for segment in template_path.parts:
        routes /= segment
        if segment == 'routes':
            break

    template_path = template_path.relative_to(routes)

    return str(template_path.with_suffix('.html'))


# @lru_cache
# def get_default_metadata(fp: str) -> Metadata | None:
#     root_path = Path(fp).resolve()

#     routes = Path()
#     maybe_app_name: str | None = None
#     for segment in root_path.parts:
#         routes = routes / segment
#         if segment == 'routes':
#             break
#         maybe_app_name = segment

#     metadata_path = routes / 'metadata.py'

#     if not metadata_path.exists() and maybe_app_name and routes.parent.name == maybe_app_name:
#         metadata_path = routes / maybe_app_name / 'metadata.py'
#         if not metadata_path.exists():
#             return None

#     module = import_module_from_path(metadata_path)
#     metadata = getattr(module, 'metadata', None)

#     if not metadata:
#         return None

#     return metadata


def render(
    request: HttpRequest,
    /,
    context: dict[str, Any] | None = None,
    *,
    filename: str = 'page.html',
    metadata: Metadata | None = None,
    **kwargs: Any,
) -> HttpResponse:
    if context is None:
        context = {}

    # module = get_view_module_from_request_path(request.path)
    frame = get_frame(1)

    # NOTE: trust me, it's not None
    assert frame is not None

    frame_path = Path(frame.f_code.co_filename)

    template_name = get_page_template(frame_path, filename=filename)
    # meta = get_default_metadata(module)

    metadata = metadata or getattr(inspect.unwrap(resolve(request.path).func), '__meta__', None)

    if metadata:
        STRING_FORMAT = re.compile(r'\{.*\}')

        for attr_name, attr_value in metadata.__dict__.items():
            if isinstance(attr_value, str) and STRING_FORMAT.match(attr_value):
                setattr(metadata, attr_name, attr_value.format(**context))

        context['metadata'] = metadata.to_html()
    else:
        from .metadata import GLOBAL_METADATA  # noqa: PLC0415

        if GLOBAL_METADATA:
            context['metadata'] = GLOBAL_METADATA.to_html()

    return django_render(request, template_name, context, **kwargs)
