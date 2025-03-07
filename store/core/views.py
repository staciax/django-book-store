from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable  # noqa: UP035

from django.contrib.auth.decorators import login_required as django_login_required
from django.urls import path
from django.views.decorators.http import require_http_methods

__all__ = (
    'ViewRouter',
    'get',
    'post',
    'view',
    'view_router',
)

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern


class ViewRouter:
    def __init__(self) -> None:
        self.routes: list[URLPattern] = []

    @property
    def urls(self) -> list[URLPattern]:
        return self.routes

    def add(
        self,
        pattern: str,
        handler: Callable[..., Any],
        *,
        name: str | None = None,
    ) -> None:
        url_pattern = path(pattern, handler, name=name or handler.__name__)
        self.routes.append(url_pattern)

    def _decorator(  # noqa: PLR0913
        self,
        methods: list[str] | None = None,
        pattern: str = '',
        *,
        name: str | None = None,
        login_required: bool = False,
        login_redirect_field_name: str = 'next',
        login_url: str | None = '/login',
    ) -> Callable[..., Any]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            if methods is not None:
                func = require_http_methods(methods)(func)
            if login_required:
                func = django_login_required(
                    login_url=login_url,
                    redirect_field_name=login_redirect_field_name,
                )(func)
            self.add(pattern, func, name=name)
            return func

        return decorator

    def get(
        self,
        pattern: str = '',
        *,
        name: str | None = None,
        login_required: bool = False,
        login_redirect_field_name: str = 'next',
        login_url: str | None = '/login',
    ) -> Callable[..., Any]:
        return self._decorator(
            ['GET'],
            pattern,
            name=name,
            login_required=login_required,
            login_redirect_field_name=login_redirect_field_name,
            login_url=login_url,
        )

    def post(
        self,
        pattern: str = '',
        *,
        name: str | None = None,
        login_required: bool = False,
        login_redirect_field_name: str = 'next',
        login_url: str | None = '/login',
    ) -> Callable[..., Any]:
        return self._decorator(
            ['POST'],
            pattern,
            name=name,
            login_required=login_required,
            login_redirect_field_name=login_redirect_field_name,
            login_url=login_url,
        )

    def view(  # noqa: PLR0913
        self,
        pattern: str,
        methods: list[str] | None = None,
        *,
        name: str | None = None,
        login_required: bool = False,
        login_redirect_field_name: str = 'next',
        login_url: str | None = '/login',
    ) -> Callable[..., Any]:
        return self._decorator(
            methods,
            pattern,
            name=name,
            login_required=login_required,
            login_redirect_field_name=login_redirect_field_name,
            login_url=login_url,
        )


view_router = ViewRouter()

get = view_router.get
post = view_router.post
view = view_router.view
