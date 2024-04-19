from __future__ import annotations

from typing import TYPE_CHECKING

from user.models import User as _User

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from .addresses import Address
    from .carts import Cart
    from .orders import Order


class User(_User):
    id: int
    addresses: RelatedManager[Address]
    carts: RelatedManager[Cart]
    orders: RelatedManager[Order]

    class Meta:
        abstract = True
