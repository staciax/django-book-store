from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from store.core.routers import render
from store.metadata import metadata
from store.models import Tag


@metadata(title='{tag.name}')
def page(request: HttpRequest, tag_id: int) -> HttpResponse:
    """tag"""
    tag = get_object_or_404(Tag, id=tag_id)

    context = {
        'tag': tag,
    }

    return render(request, context)
