from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from store.core.routers import render
from store.metadata import metadata
from store.models import Product


@metadata(
    title='{product.title}',
    og_title='{product.title}',
    og_description='{product.description}',
)
def page(request: HttpRequest, slug: str) -> HttpResponse:
    """product-detail"""
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
    }
    return render(request, __file__, context)
