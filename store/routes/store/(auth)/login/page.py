from http import HTTPMethod

from django.contrib import auth
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from store.core.routers import render
from store.forms.auth import LoginForm
from store.metadata import metadata


@metadata(title='เข้าสู่ระบบ')
def page(request: HttpRequest) -> HttpResponse:
    """login"""

    if request.user.is_authenticated:
        return redirect('store:home')

    context = {
        'next': request.GET.get('next'),
    }

    if request.method == HTTPMethod.POST:
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, __file__, context)

        user = auth.authenticate(
            request,
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )

        if user is None:
            return render(request, __file__, context)

        auth.login(request, user)

        # redirect to the next url
        next_url = request.POST.get('next')
        if next_url and (next_url != reverse('store:account')):
            return redirect(next_url)

        return redirect('store:home')

    return render(request, __file__, context)
