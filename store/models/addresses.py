from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.urls import reverse

from .base_model import TimestampModel

if TYPE_CHECKING:
    from .user import User


class Address(TimestampModel):
    full_name = models.CharField(max_length=128, default='')
    phone_number = models.CharField(max_length=10, default='')
    street_address = models.CharField(max_length=256, default='')
    province = models.CharField(max_length=128, default='')
    district = models.CharField(max_length=128, default='')
    postal_code = models.CharField(max_length=5, default='')
    user_id: int
    user = models.ForeignKey['User'](
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses',
    )

    class Meta:
        db_table = 'store_addresses'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def get_absolute_url(self) -> str:
        return reverse('store:address-edit', kwargs={'address_id': self.id})

    def __str__(self) -> str:
        return f'{self.full_name}'

    def to_list(self) -> list[str]:
        return [
            self.full_name,
            self.street_address,
            self.district + ' ' + self.postal_code,
            self.province,
            self.phone_number,
        ]
