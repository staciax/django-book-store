from django.contrib import admin

from ..models import (
    Address,
    Author,
    Cart,
    Genre,
    Order,
    OrderItem,
    Payment,
    Product,
    ProductAuthor,
    ProductImage,
    ProductTagging,
    Publisher,
    Tag,
)
from .addresses import AddressAdmin
from .authors import AuthorAdmin
from .carts import CartAdmin
from .genres import GenreAdmin
from .orders import OrderAdmin, OrderItemAdmin
from .payments import PaymentAdmin
from .products import ProductAdmin, ProductAuthorAdmin, ProductImageAdmin, ProductTaggingAdmin
from .publishers import PublisherAdmin
from .tags import TagAdmin

admin.site.register(Address, AddressAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductTagging, ProductTaggingAdmin)
admin.site.register(ProductAuthor, ProductAuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Tag, TagAdmin)
