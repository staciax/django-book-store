from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..models import Cart

if TYPE_CHECKING:
    from django.http.request import HttpRequest


def counter(request: HttpRequest) -> dict[str, Any]:
    if not request.user.is_authenticated:
        return {}

    if request.path.startswith('/admin'):
        return {}

    cart_items = Cart.objects.filter(
        user=request.user,
        product__quantity__gt=0,
        product__is_available=True,
    )

    return {'store_cart_count': sum(item.quantity for item in cart_items)}
