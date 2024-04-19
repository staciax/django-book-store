from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse

from .base_model import TimestampModel

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from .products import Product


class Genre(TimestampModel):
    name = models.CharField(max_length=128, unique=True)

    products: RelatedManager[Product]

    class Meta:
        db_table = 'store_genres'
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        # TODO: url with slug
        return reverse('store:genre', kwargs={'genre_id': self.id})
