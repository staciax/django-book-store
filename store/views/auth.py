from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import logout
from django.shortcuts import redirect

from store.core.views import get

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponse


@get('logout/', name='logout')
def sign_out(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('store:home')
