from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from store.core.routers import render
from store.metadata import metadata
from store.models import Cart
from store.utils.carts import refresh_cart_item_quantity


@login_required(login_url='/login')
@metadata(title='ตะกร้าสินค้า')
def page(request: HttpRequest) -> HttpResponse:
    """cart"""
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at').all()

    refresh_cart_item_quantity(cart_items)

    # TODO: custom tag for sum of cart
    context = {
        'cart_items': cart_items,
        'total': sum(item.sub_total() for item in cart_items if item.product.quantity > 0),
    }
    return render(request, __file__, context)
