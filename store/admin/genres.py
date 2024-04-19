from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:
    from ..models import Genre


class GenreAdmin(admin.ModelAdmin['Genre']):
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
