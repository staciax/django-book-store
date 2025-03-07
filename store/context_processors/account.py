from __future__ import annotations

from itertools import starmap
from typing import TYPE_CHECKING, Any

from django.urls import reverse

if TYPE_CHECKING:
    from django.http.request import HttpRequest


def account_navigator(request: HttpRequest) -> dict[str, Any]:
    if not request.user.is_authenticated:
        return {}

    class Navigator:
        def __init__(self, text: str, data: dict[str, Any]) -> None:
            self.text = text
            self.icon: str | None = data['icon']
            self.url: str | None = data['url']

    navigator = {
        'บัญชีของฉัน': {
            'icon': 'account-blue.svg',
            'url': reverse('store:account'),
        },
        'ที่อยู่': {
            'icon': 'address.svg',
            'url': reverse('store:account-address'),
        },
        'คำสั่งซื้อ': {
            'icon': 'order.svg',
            'url': reverse('store:account-orders'),
        },
        'ออกจากระบบ': {
            'icon': 'logout.svg',
            'url': reverse('store:logout'),
        },
    }

    return {'store_account_navigator': list(starmap(Navigator, navigator.items()))}
