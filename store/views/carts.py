from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import redirect

from store.core.views import post, view
from store.models import Cart, Product

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponse


@view(
    'cart-add-product/<int:product_id>/<int:quantity>/',
    name='cart-add-product',
    login_required=True,
)
def add_product_to_cart(request: HttpRequest, product_id: int, quantity: int) -> HttpResponse:
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:  # noqa: TRY203
        raise
    else:
        # if product.quantity <= 0:
        #     raise

        # if product.quantity < quantity:
        #     raise

        try:
            cart_item = Cart.objects.get(product=product, user=request.user)
            new_quantity = cart_item.quantity + quantity
            new_quantity = min(product.quantity, new_quantity)
            cart_item.quantity = min(new_quantity, 10)
            cart_item.save()
        except Cart.DoesNotExist:
            # carts = Cart.objects.filter(user=request.user)
            # if carts.count() >= 10:
            #     return redirect('store:cart')
            quantity = min(product.quantity, quantity)
            cart_item = Cart.objects.create(
                user=request.user,
                product=product,
                quantity=min(quantity, 10),
            )
            cart_item.save()

    referer = request.META.get('HTTP_REFERER')

    if not referer:
        return redirect('store:product-detail', slug=product.slug)

    # next_url = redirect(reverse('store:product-detail', kwargs={'slug': product.slug}) + f'#{product.id}')
    # next_url = redirect(reverse('store:home') + f'#{product.id}')

    referer += f'#{product.id}'

    return redirect(referer)


@post(
    'cart-add/<int:cart_id>/',
    name='cart-add',
    login_required=True,
)
def add_to_cart(request: HttpRequest, cart_id: int) -> HttpResponse:
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        new_quantity = cart_item.quantity + 1
        new_quantity = min(cart_item.product.quantity, new_quantity)
        cart_item.quantity = min(new_quantity, 10)
        cart_item.save()
    except Cart.DoesNotExist:
        pass
    return redirect('store:cart')
    # return redirect(reverse('store:cart') + f'#{cart_id}')


@post(
    'cart-subtract/<int:cart_id>/',
    name='cart-subtract',
    login_required=True,
)
def subtract_from_cart(request: HttpRequest, cart_id: int) -> HttpResponse:
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        new_quantity = cart_item.quantity - 1
        if new_quantity <= 0:
            new_quantity = 1
        new_quantity = min(cart_item.product.quantity, new_quantity)
        cart_item.quantity = new_quantity
        cart_item.save()
    except Cart.DoesNotExist:
        pass
    return redirect('store:cart')


@post(
    'cart-delete/<int:cart_id>/',
    name='cart-delete',
    login_required=True,
)
def delete_from_cart(request: HttpRequest, cart_id: int) -> HttpResponse:
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('store:cart')
