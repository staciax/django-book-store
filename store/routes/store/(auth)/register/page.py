from http import HTTPMethod

from django.contrib.auth import login as auth_login
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect

from store.core.routers import render
from store.forms.auth import RegisterForm
from store.metadata import metadata


@metadata(title='สมัครสมาชิก')
def page(request: HttpRequest) -> HttpResponse:
    """register"""

    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == HTTPMethod.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
        return redirect('store:home')

    return render(request)
