from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from store.core.routers import render
from store.metadata import metadata
from store.models import Genre


@metadata(title='{genre.name}')
def page(request: HttpRequest, genre_id: int) -> HttpResponse:
    """genre"""
    genre = get_object_or_404(Genre, id=genre_id)

    context = {
        'genre': genre,
    }

    return render(request, context)
