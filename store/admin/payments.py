from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:
    from ..models import Payment


class PaymentAdmin(admin.ModelAdmin['Payment']):
    actions = None
