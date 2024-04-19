from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from store.core.routers import render
from store.metadata import metadata
from store.models import Order


@login_required(login_url='/login')
@metadata(title='คำสั่งซื้อของฉัน')
def page(request: HttpRequest) -> HttpResponse:
    """account-orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at').all()
    context = {
        'orders': orders,
    }
    return render(request, __file__, context)
