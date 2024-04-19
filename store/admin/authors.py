from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:
    from ..models import Author


class AuthorAdmin(admin.ModelAdmin['Author']):
    actions = None
    list_display = (
        'id',
        'name',
    )
    list_display_links = (
        'id',
        'name',
    )
