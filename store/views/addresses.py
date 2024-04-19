from __future__ import annotations

import contextlib
from http import HTTPMethod
from typing import TYPE_CHECKING

from django.shortcuts import redirect, render
from django.urls import reverse

from store.core.views import post, view
from store.forms.addresses import CreateAddressForm, UpdateAddressForm
from store.models import Address

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponse


@post(
    'create-address/',
    name='create-address',
    login_required=True,
)
def create_address(request: HttpRequest) -> HttpResponse:
    addresses = Address.objects.filter(user=request.user)
    if addresses.count() >= 5:
        return redirect('store:account-address')

    form = CreateAddressForm(request.POST or None)
    if request.method == HTTPMethod.POST and form.is_valid():
        address = Address.objects.create(
            user=request.user,
            **form.cleaned_data,
        )
        address.save()

        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)

    return redirect('store:account-address')


@post(
    'delete-address/<int:address_id>/',
    name='delete-address',
    login_required=True,
)
def delete_address(request: HttpRequest, address_id: int) -> HttpResponse:
    with contextlib.suppress(Address.DoesNotExist):
        cart_item = Address.objects.get(id=address_id, user=request.user)
        cart_item.delete()

    return redirect('store:account-address')


@post(
    'update-address/<int:address_id>/',
    name='update-address',
    login_required=True,
)
def update_address(request: HttpRequest, address_id: int) -> HttpResponse:
    form = UpdateAddressForm(request.POST or None)
    if request.method == HTTPMethod.POST and form.is_valid():
        with contextlib.suppress(Address.DoesNotExist):
            address = Address.objects.get(user=request.user, id=address_id)
            for key, value in form.cleaned_data.items():
                setattr(address, key, value)
            address.save()
    return redirect('store:account-address')


@view(
    'add-address-from-checkout/',
    name='add-address-from-checkout',
    login_required=True,
)
def add_address_from_checkout(request: HttpRequest) -> HttpResponse:
    context = {
        'form_action': reverse(
            'store:create-address',
        ),
        'next': 'store:cart-checkout',
    }
    return render(
        request,
        'store/account/address/_components/add-address.html',
        context,
    )
