from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from store.core.routers import render
from store.metadata import metadata
from store.models import Order


@login_required(login_url='/login')
@metadata(title='รายละเอียดคำสั่งซื้อ')
def page(request: HttpRequest, order_id: int) -> HttpResponse:
    """order-detail"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:  # noqa: TRY203
        raise

    shipping = Decimal(50)

    final_total = order.get_total() + shipping

    context = {
        'order': order,
        'shipping': shipping,
        'final_total': final_total,
    }
    return render(request, __file__, context)
