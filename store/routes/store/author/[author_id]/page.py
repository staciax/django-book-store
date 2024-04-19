from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from store.core.routers import render
from store.metadata import metadata
from store.models import Author


@metadata(title='{author.name}')
def page(request: HttpRequest, author_id: int) -> HttpResponse:
    """author"""
    author = get_object_or_404(Author, id=author_id)

    context = {
        'author': author,
    }

    return render(request, __file__, context)
