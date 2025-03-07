from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect

from store.core.routers import render
from store.metadata import metadata
from store.models import Address, Cart


@login_required(login_url='/login')
@metadata(title='เช็คเอาท์')
def page(request: HttpRequest) -> HttpResponse:
    """cart-checkout"""
    cart_items = Cart.objects.filter(
        user=request.user,
        product__quantity__gt=0,
        product__is_available=True,
    ).order_by('created_at')

    # TODO: refresh cart item quantity before checkout

    if cart_items.count() <= 0:
        return redirect('store:cart')

    addresses = Address.objects.filter(user=request.user).order_by('created_at')

    total = sum(item.sub_total() for item in cart_items)  # if item.product.quantity > 0

    shipping = Decimal(50)

    final_total = total + shipping

    context = {
        'user': request.user,
        'addresses': addresses,
        'cart_items': cart_items,
        'total': total,
        'shipping': shipping,
        'final_total': final_total,
    }
    return render(request, context)
