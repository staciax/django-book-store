from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from .base_model import TimestampModel
from store.utils import build_media_filename

if TYPE_CHECKING:
    from .orders import Order


def get_receipt_path(instance: Payment, filename: str) -> str:
    filename = build_media_filename(filename, prefix=str(instance.order.id))
    return f'receipt/{filename}'


class Payment(TimestampModel):
    order_id: int
    order = models.OneToOneField['Order'](
        'store.Order',
        on_delete=models.CASCADE,
        related_name='payment',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=128)
    paid_at = models.DateTimeField(null=True, blank=True)
    receipt = models.ImageField(
        upload_to=get_receipt_path,  # type: ignore[arg-type]
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'store_payments'
        verbose_name = 'payment'
        verbose_name_plural = 'payments'

    def __str__(self) -> str:
        return f'Payment for {self.order}'
