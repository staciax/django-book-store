from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse

from .base_model import TimestampModel

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from .products import Product


class Publisher(TimestampModel):
    name = models.CharField(max_length=256)

    product_set: RelatedManager[Product]

    class Meta:
        db_table = 'store_publishers'
        verbose_name = 'publisher'
        verbose_name_plural = 'publishers'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        # TODO: url with slug
        return reverse('store:publisher', kwargs={'publisher_id': self.id})
