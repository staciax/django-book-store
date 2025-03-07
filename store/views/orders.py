from __future__ import annotations

from http import HTTPMethod
from typing import TYPE_CHECKING

from django.shortcuts import redirect
from django.urls import reverse

from store.core.views import post
from store.forms import CreateOrderForm
from store.models import Address, Cart, Order, OrderItem

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponse


@post(
    'create-order/',
    name='create-order',
    login_required=True,
)
def create_order(request: HttpRequest) -> HttpResponse:  # noqa: PLR0911
    cart_items = Cart.objects.filter(
        user=request.user,
        product__quantity__gt=0,
        product__is_available=True,
    ).order_by('created_at')
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store:home')

    if request.method == HTTPMethod.POST:
        form = CreateOrderForm(request.POST)
        if not form.is_valid():
            return redirect('store:cart-checkout')

        address_id = form.cleaned_data['address_id']
        if not address_id:
            return redirect('store:cart-checkout')

        payment_method = form.cleaned_data['payment_method']
        if not payment_method:
            return redirect('store:cart-checkout')

        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return redirect('store:cart-checkout')

        order = Order.objects.create(
            user=request.user,
            address='\n'.join(address.to_list()),
        )

        # TODO: check item quantity more than product quantity or product quantity less than 0
        for item in cart_items.all():
            item.product.quantity -= item.quantity
            item.product.save()

            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_on_purchase=item.product.price,
            )
            order_item.save()

        cart_items.delete()

        return redirect(
            reverse(
                'store:order-payment',
                kwargs={
                    'order_id': order.id,
                },
            ),
        )
        # return redirect(order.get_absolute_url())

    return redirect('store:cart-checkout')
