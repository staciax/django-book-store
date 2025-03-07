from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, ClassVar

from django.conf import settings
from django.db import models
from django.urls import reverse

from .base_model import TimestampModel

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from .payments import Payment
    from .products import Product
    from .user import User


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'pending'
    PAID = 'paid', 'paid'
    APPROVED = 'approved', 'approved'
    CANCELED = 'canceled', 'canceled'
    SHIPPED = 'shipped', 'shipped'
    COMPLETED = 'completed', 'completed'
    RETURNED = 'returned', 'returned'


class Order(TimestampModel):
    user_id: int
    user = models.ForeignKey['User'](
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    address = models.TextField()
    status = models.CharField(
        max_length=32,
        choices=OrderStatus,  # pyright: ignore[reportCallIssue, reportArgumentType]
        default=OrderStatus.PENDING,
    )
    tracking_number = models.CharField(max_length=32, default='')
    approved_at = models.DateTimeField(null=True)
    shipped_at = models.DateTimeField(null=True)
    canceled_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    payment: RelatedManager[Payment]
    items: RelatedManager[OrderItem]

    class Meta:
        db_table = 'store_orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self) -> str:
        return f'{self.id} - {self.user}'

    def get_absolute_url(self) -> str:
        return reverse('store:order-detail', kwargs={'order_id': self.id})

    def get_total(self) -> Decimal:
        return Decimal(sum(item.sub_total() for item in self.items.all()))

    def address_as_list(self) -> list[str]:
        return self.address.split('\n')


class OrderItem(TimestampModel):
    id: int
    order = models.ForeignKey['Order'](
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey['Product'](
        'store.Product',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)
    price_on_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'store_order_items'
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

        # https://docs.djangoproject.com/en/5.0/ref/models/options/#unique-together
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=('order', 'product'),
                name='unique_order_item',
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name='order_item_quantity_gte_1',
            ),
        ]
        # https://docs.djangoproject.com/en/5.0/ref/models/options/#constraints

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.price_on_purchase = self.product.price
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.order} - {self.product}'

    def sub_total(self) -> Decimal:
        return Decimal(self.product.price * self.quantity)
