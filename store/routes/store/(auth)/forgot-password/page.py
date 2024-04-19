from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect

from store.core.routers import render
from store.metadata import metadata


@metadata(title='ลืมรหัสผ่าน')
def page(request: HttpRequest) -> HttpResponse:
    """forgot-password"""

    if request.user.is_authenticated:
        return redirect('store:home')

    return render(request, __file__)
