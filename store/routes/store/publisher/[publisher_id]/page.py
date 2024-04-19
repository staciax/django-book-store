from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from store.core.routers import render
from store.metadata import metadata
from store.models import Publisher


@metadata(title='{publisher.name}')
def page(request: HttpRequest, publisher_id: int) -> HttpResponse:
    """publisher"""
    publisher = get_object_or_404(Publisher, id=publisher_id)

    context = {
        'publisher': publisher,
    }
    return render(request, __file__, context)
