from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:
    from ..models import Address


class AddressAdmin(admin.ModelAdmin['Address']):
    actions = None
    list_display = (
        'id',
        'user',
        'full_name',
    )
    list_per_page = 10
