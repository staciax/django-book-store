from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.utils.safestring import SafeString

from ..models import OrderItem
from store.models.orders import Order

if TYPE_CHECKING:
    from decimal import Decimal

    from django.db.models.fields.files import ImageFieldFile

    from ..models import Order


def image_preview_tag(image_field: ImageFieldFile) -> str:
    return SafeString(f'<img src="{image_field.url}" style="max-width:100px; max-height:200px"/>')


class OrderItemInline(admin.TabularInline[OrderItem]):
    model = OrderItem
    extra = 1
    max_num = 10
    verbose_name = 'order item inline'
    verbose_name_plural = 'order item inlines'
    fields = (
        'product',
        'quantity',
        'price',
        'total',
    )
    readonly_fields = (
        'price',
        'total',
    )

    def price(self, order_item: OrderItem) -> Decimal:
        return order_item.product.price

    def total(self, order_item: OrderItem) -> Decimal:
        return order_item.product.price * order_item.quantity


class OrderAdmin(admin.ModelAdmin['Order']):
    actions = None
    list_display = (
        'id',
        'user',
        'created_at',
        'status',
    )
    list_editable = ('status',)
    list_per_page = 10
    inlines = (OrderItemInline,)


class OrderItemAdmin(admin.ModelAdmin[OrderItem]):
    actions = None
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price_on_purchase',
    )
    fields = (
        'order',
        'product',
        'quantity',
        'image_preview',
    )
    list_editable = ('quantity',)
    readonly_fields = ('image_preview',)
    list_per_page = 10

    def image_preview(self, order_item: OrderItem) -> str:
        if order_item.product.first_image is None:
            return '-'
        return image_preview_tag(order_item.product.first_image.image)
