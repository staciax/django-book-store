from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import BaseManager

    from store.models import Cart


def refresh_cart_item_quantity(cart: BaseManager[Cart]):
    # TODO: message alert for quantity change
    for item in cart.all():
        # if item.product.quantity <= 0:
        #     item.delete()
        if item.product.quantity and item.product.quantity < item.quantity:
            item.quantity = item.product.quantity
            item.save()
