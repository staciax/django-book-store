from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db import models
from django.urls import reverse

from .base_model import BaseModel, TimestampModel
from store.utils import build_media_filename, to_thai_slug

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from .authors import Author
    from .genres import Genre
    from .publishers import Publisher
    from .tags import Tag


def get_product_image_path(instance: ProductImage, filename: str) -> str:
    filename = build_media_filename(filename, prefix=str(instance.product.id))
    return f'product/{filename}'


class Product(TimestampModel):
    title = models.CharField(max_length=256)
    description = models.TextField(default='', blank=True)
    published_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(max_length=256)

    author = models.ManyToManyField['Author', 'ProductAuthor'](
        'store.Author',
        through='store.ProductAuthor',
    )

    publisher_id: int
    publisher = models.ForeignKey['Publisher'](
        'store.Publisher',
        on_delete=models.CASCADE,
        null=True,
    )

    genre_id: int
    genre = models.ForeignKey['Genre'](
        'store.Genre',
        on_delete=models.CASCADE,
        related_name='products',
    )

    tags = models.ManyToManyField['Tag', 'ProductTagging'](
        'store.Tag',
        through='store.ProductTagging',
    )

    images: RelatedManager[ProductImage]

    class Meta:
        db_table = 'store_products'
        verbose_name = 'product'
        verbose_name_plural = 'products'

        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name='product_price_gte_0',
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='product_quantity_gte_0',
            ),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            slug = to_thai_slug(self.title)
            unique_slug = slug
            counter = 2
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{slug}-{counter}'
                counter += 1

            self.slug = unique_slug

        # else:
        # TODO: update slug when update title
        # slug = to_thai_slug(self.title)
        # unique_slug = slug
        # products = Product.objects.filter(slug=slug)
        # slug_exits = next((product for product in products if product.id != self.id), None)
        # if slug_exits is not None:
        #     while products.filter(slug=slug).exists():
        #         unique_slug = f'{slug}-{counter}'
        #         counter += 1

        # self.is_available = self.quantity > 0

        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('store:product-detail', kwargs={'slug': self.slug})

    @property
    def first_image(self) -> ProductImage | None:
        return self.images.first()

    # TODO: dummy image


class ProductImage(TimestampModel):
    product_id: int
    product = models.ForeignKey['Product'](
        Product,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        upload_to=get_product_image_path,  # pyright: ignore[reportArgumentType]
        blank=True,
        default='',
    )

    class Meta:
        db_table = 'store_product_images'
        verbose_name = 'product image'
        verbose_name_plural = 'product images'

        # permissions = [
        #     ('view_all_product_images', 'Can view all product images'),
        # ]

    def __str__(self) -> str:
        return str(self.image)


class ProductAuthor(BaseModel):
    product_id: int
    product = models.ForeignKey['Product'](
        'store.Product',
        on_delete=models.CASCADE,
        related_name='authors',
    )
    author_id: int
    author = models.ForeignKey['Author'](
        'store.Author',
        on_delete=models.CASCADE,
        related_name='products',
    )

    class Meta:
        db_table = 'store_product_author'
        verbose_name = 'product author'
        verbose_name_plural = 'product authors'

        constraints = [
            models.UniqueConstraint(
                fields=('product', 'author'),
                name='unique_product_author',
            ),
        ]

    def __str__(self) -> str:
        return str(self.author)


class ProductTagging(BaseModel):
    product_id: int
    product = models.ForeignKey['Product']('store.Product', on_delete=models.CASCADE)
    tag_id: int
    tag = models.ForeignKey['Tag']('store.Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'store_product_tagging'
        verbose_name = 'product tagging'
        verbose_name_plural = 'product taggings'

        constraints = [
            models.UniqueConstraint(
                fields=('product', 'tag'),
                name='unique_product_tag',
            ),
        ]
        # https://docs.djangoproject.com/en/5.0/ref/models/constraints/#fields

    def __str__(self) -> str:
        return str(self.tag)
