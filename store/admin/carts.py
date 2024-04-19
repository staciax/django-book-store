from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:
    from ..models import Cart


class CartAdmin(admin.ModelAdmin['Cart']):
    actions = None
    list_display = (
        'id',
        'user',
        'product',
        'quantity',
    )
    list_editable = ('quantity',)
    list_per_page = 10
