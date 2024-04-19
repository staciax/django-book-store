from http import HTTPMethod

from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from store.core.routers import render
from store.metadata import metadata


@login_required(login_url='/login')
@metadata(title='บัญชีของฉัน')
def page(request: HttpRequest) -> HttpResponse:
    """account"""
    if request.method == HTTPMethod.POST:
        return render(
            request,
            __file__,
            {'user': request.user},
            filename='_components/edit-account.html',
        )
    return render(request, __file__)
