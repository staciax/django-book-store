from decimal import Decimal
from typing import TYPE_CHECKING, ClassVar

from django.conf import settings
from django.db import models

from .base_model import TimestampModel

if TYPE_CHECKING:
    from .products import Product
    from .user import User


class Cart(TimestampModel):
    user_id: int
    user = models.ForeignKey['User'](
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
    )
    product_id: int
    product = models.ForeignKey['Product'](
        'store.Product',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'store_carts'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_cart_item',
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name='cart_item_quantity_gte_1',
            ),
        ]
        # https://docs.djangoproject.com/en/5.0/ref/models/options/#constraints

    def __str__(self) -> str:
        return f'{self.user} - {self.product}'

    def sub_total(self) -> Decimal:
        return Decimal(self.product.price * self.quantity)
