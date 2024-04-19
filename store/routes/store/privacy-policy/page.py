from django.http.request import HttpRequest
from django.http.response import HttpResponse

from store.core.routers import render
from store.metadata import metadata


@metadata(title='นโยบายความเป็นส่วนตัว')
def page(request: HttpRequest) -> HttpResponse:
    """privacy-policy"""
    context = {}
    return render(request, __file__, context)
