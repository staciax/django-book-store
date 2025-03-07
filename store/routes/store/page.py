from django.http.request import HttpRequest
from django.http.response import HttpResponse

from store.core.metadata import Metadata
from store.core.routers import render
from store.models import Product


def page(request: HttpRequest) -> HttpResponse:
    """home"""
    products = Product.objects.all()

    search = request.GET.get('search')
    if search is not None:
        filter_products = products.filter(title__icontains=search)
        context = {
            'search': search,
            'products': filter_products,
        }
        return render(
            request,
            __file__,
            context,
            filename='_components/search.html',
            metadata=Metadata(title=f'ค้นหา - {search}'),
        )

    context = {
        'recommended_products': products[:12],
    }

    return render(request, __file__, context)
