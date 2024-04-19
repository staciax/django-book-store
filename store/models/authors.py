from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse

from .base_model import TimestampModel

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from .products import Product


class Author(TimestampModel):
    name = models.CharField(max_length=128, unique=True)
    product_set: RelatedManager[Product]

    class Meta:
        db_table = 'store_authors'
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        # TODO: url with slug
        return reverse('store:author', kwargs={'author_id': self.id})
