from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:
    from ..models import Publisher


class PublisherAdmin(admin.ModelAdmin['Publisher']):
    actions = None
    list_display = (
        'id',
        'name',
    )
    list_display_links = (
        'id',
        'name',
    )
    list_per_page = 10
