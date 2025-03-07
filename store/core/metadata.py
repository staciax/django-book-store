from __future__ import annotations

from typing import Any, Callable, Self  # noqa: UP035

from django.utils.safestring import SafeString

__all__ = (
    'Metadata',
    'metadata',
)


class Metadata:
    def __init__(  # noqa: PLR0913
        self,
        *,
        title: str,
        shortcut_icon: str | None = None,
        og_type: str | None = None,
        og_title: str | None = None,
        og_description: str | None = None,
        og_url: str | None = None,
        og_image: str | None = None,  # TODO: support list of images
        og_image_width: int | None = None,
        og_image_height: int | None = None,
    ) -> None:
        self.title = title
        self.shortcut_icon = shortcut_icon
        self.og_type = og_type
        self.og_title = og_title
        self.og_description = og_description
        self.og_url = og_url
        self.og_image = og_image
        self.og_image_width = og_image_width
        self.og_image_height = og_image_height

    def to_html(self) -> str:
        html = SafeString(f'<title>{self.title}</title>')
        if self.shortcut_icon:
            html += SafeString(f'\n<link rel="shortcut icon" href="{self.shortcut_icon}" />')
        if self.og_type:
            html += SafeString(f'\n<meta property="og:type" content="{self.og_type}" />')
        if self.og_title:
            html += SafeString(f'\n<meta property="og:title" content="{self.og_title}" />')
        if self.og_description:
            html += SafeString(f'\n<meta property="og:description" content="{self.og_description}" />')
        if self.og_url:
            html += SafeString('\n<meta property="og:url" content="{self.url}" />')
        if self.og_image:
            html += SafeString(f'\n<meta property="og:image" content="{self.og_image}" />')
            if self.og_image_width:
                html += SafeString(f'\n<meta property="og:image:width" content="{self.og_image_width}" />')
            if self.og_image_height:
                html += SafeString(f'\n<meta property="og:image:height" content="{self.og_image_height}" />')
        return html

    def merge(self, other: Metadata) -> Metadata:
        self.title = other.title or self.title
        self.shortcut_icon = other.shortcut_icon or self.shortcut_icon
        self.og_type = other.og_type or self.og_type
        self.og_title = other.og_title or self.og_title
        self.og_description = other.og_description or self.og_description
        self.og_url = other.og_url or self.og_url
        self.og_image = other.og_image or self.og_image
        self.og_image_width = other.og_image_width or self.og_image_width
        self.og_image_height = other.og_image_height or self.og_image_height
        return self

    @classmethod
    def copy(cls, other: Metadata) -> Self:
        self = cls.__new__(cls)  # bypass __init__
        self.title = other.title
        self.shortcut_icon = other.shortcut_icon
        self.og_type = other.og_type
        self.og_title = other.og_title
        self.og_description = other.og_description
        self.og_url = other.og_url
        self.og_image = other.og_image
        self.og_image_width = other.og_image_width
        self.og_image_height = other.og_image_height
        return self

    def _decorator(  # noqa: PLR0913
        self,
        *,
        title: str,
        shortcut_icon: str | None = None,
        og_type: str | None = None,
        og_title: str | None = None,
        og_description: str | None = None,
        og_url: str | None = None,
        og_image: str | None = None,
        og_image_width: int | None = None,
        og_image_height: int | None = None,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            metadata = self.copy(self)
            func.__meta__ = metadata.merge(  # type: ignore[attr-defined]
                Metadata(
                    title=title,
                    shortcut_icon=shortcut_icon,
                    og_type=og_type,
                    og_title=og_title,
                    og_description=og_description,
                    og_url=og_url,
                    og_image=og_image,
                    og_image_width=og_image_width,
                    og_image_height=og_image_height,
                    **kwargs,
                )
            )
            return func

        return decorator

    def __call__(  # noqa: PLR0913
        self,
        *,
        title: str,
        shortcut_icon: str | None = None,
        og_type: str | None = None,
        og_title: str | None = None,
        og_description: str | None = None,
        og_url: str | None = None,
        og_image: str | None = None,
        og_image_width: int | None = None,
        og_image_height: int | None = None,
        **kwargs: Any,
    ) -> Callable[..., Any]:
        return self._decorator(
            title=title,
            shortcut_icon=shortcut_icon,
            og_type=og_type,
            og_title=og_title,
            og_description=og_description,
            og_url=og_url,
            og_image=og_image,
            og_image_width=og_image_width,
            og_image_height=og_image_height,
            **kwargs,
        )


def metadata(  # noqa: PLR0913
    *,
    title: str,
    shortcut_icon: str | None = None,
    og_type: str | None = None,
    og_title: str | None = None,
    og_description: str | None = None,
    og_url: str | None = None,
    og_image: str | None = None,
    og_image_width: int | None = None,
    og_image_height: int | None = None,
    **kwargs: Any,
) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.__meta__ = Metadata(  # type: ignore[attr-defined]
            title=title,
            shortcut_icon=shortcut_icon,
            og_type=og_type,
            og_title=og_title,
            og_description=og_description,
            og_url=og_url,
            og_image=og_image,
            og_image_width=og_image_width,
            og_image_height=og_image_height,
            **kwargs,
        )
        return func

    return decorator


def set_global_metadata(metadata: Metadata) -> None:
    global GLOBAL_METADATA  # noqa: PLW0603
    GLOBAL_METADATA = metadata


GLOBAL_METADATA: Metadata | None = None
