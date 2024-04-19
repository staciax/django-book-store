from django.db import models
from django.urls import reverse

from .base_model import TimestampModel


class Tag(TimestampModel):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = 'store_tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        # TODO: url with slug
        return reverse('store:tag', kwargs={'tag_id': self.id})
