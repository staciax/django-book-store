from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from app.settings import env

from store.core.routers import render
from store.metadata import metadata
from store.models import Order


@login_required(login_url='/login')
@metadata(title='ชำระเงินคำสั่งซื้อ')
def page(request: HttpRequest, order_id: int) -> HttpResponse:
    """order-payment"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:  # noqa: TRY203
        raise

    shipping = Decimal(50)

    final_total = order.get_total() + shipping

    context = {
        'promptpay_id': env('PROMPTPAY_ID'),
        'order': order,
        'final_total': final_total,
    }

    return render(request, __file__, context)
