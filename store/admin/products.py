from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.utils.safestring import mark_safe

from ..models import ProductAuthor, ProductImage, ProductTagging

if TYPE_CHECKING:
    from django.db.models.fields.files import ImageFieldFile

    from ..models import Product

# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#working-with-many-to-many-intermediary-models


def image_preview_tag(image_field: ImageFieldFile) -> str:
    return mark_safe(f'<img src="{image_field.url}" style="max-width:100px; max-height:200px"/>')


class ProductImageInline(admin.TabularInline[ProductImage]):
    model = ProductImage
    extra = 1
    max_num = 10
    verbose_name = 'product image inline'
    verbose_name_plural = 'product image inlines'
    readonly_fields = ('image_preview',)

    def image_preview(self, product_image: ProductImage) -> str:
        return image_preview_tag(product_image.image)


class ProductTaggingInline(admin.TabularInline[ProductTagging]):
    model = ProductTagging
    extra = 1
    verbose_name = 'product tag inline'
    verbose_name_plural = 'product tag inlines'


class ProductAuthorInline(admin.TabularInline[ProductAuthor]):
    model = ProductAuthor
    extra = 1
    verbose_name = 'product author inline'
    verbose_name_plural = 'product author inlines'


class ProductAdmin(admin.ModelAdmin['Product']):
    actions = None
    inlines = (ProductImageInline, ProductTaggingInline, ProductAuthorInline)
    list_display = (
        'id',
        'title',
        'price',
        'quantity',
        'is_available',
        # 'image_preview',
    )
    list_display_links = (
        'id',
        'title',
    )
    list_editable = (
        'quantity',
        'is_available',
    )
    readonly_fields = ('slug',)
    search_fields = ('title',)
    list_per_page = 10

    def image_preview(self, product: Product) -> str:
        if product.first_image is None:
            return '-'
        return image_preview_tag(product.first_image.image)


class ProductImageAdmin(admin.ModelAdmin['ProductImage']):
    actions = None
    list_display = (
        'id',
        'product',
        'image',
        'image_preview',
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, product_image: ProductImage) -> str:
        return image_preview_tag(product_image.image)


class ProductTaggingAdmin(admin.ModelAdmin['ProductTagging']):
    actions = None
    list_display = (
        'id',
        'product',
        'tag',
    )


class ProductAuthorAdmin(admin.ModelAdmin[ProductAuthor]):
    actions = None
    list_display = (
        'id',
        'product',
        'author',
    )
