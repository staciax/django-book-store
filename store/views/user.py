from __future__ import annotations

import contextlib
from http import HTTPMethod
from typing import TYPE_CHECKING

from django.shortcuts import redirect

from store.core.views import post
from store.forms.account import UpdateAccountForm

if TYPE_CHECKING:
    from django.http.response import HttpResponse

    from store.request import AuthenticatedHttpRequest


@post(
    'update-account',
    name='update-account',
    login_required=True,
)
def update_account(request: AuthenticatedHttpRequest) -> HttpResponse:
    form = UpdateAccountForm(request.POST or None)
    if request.method == HTTPMethod.POST and form.is_valid():
        # TODO: support email update
        with contextlib.suppress(KeyError):
            form.cleaned_data.pop('email')
        account = request.user
        account.first_name = form.cleaned_data.get('first_name', account.first_name)
        account.last_name = form.cleaned_data.get('last_name', account.last_name)
        account.phone_number = form.cleaned_data.get('phone_number', account.phone_number)
        account.save()

    return redirect('store:account')
