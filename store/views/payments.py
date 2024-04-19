from __future__ import annotations

from http import HTTPMethod
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404, redirect

from store.core.views import post
from store.models import Order, Payment
from store.models.orders import OrderStatus

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponse


# class PaymentForm(forms.Form):
#     file_input = fields.FileField()


@post(
    'payment/<int:order_id>',
    name='payment',
    login_required=True,
)
def payment(request: HttpRequest, order_id: int) -> HttpResponse:
    if request.method == HTTPMethod.POST:
        receipt_file = request.FILES['file_input']

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user,
        )

        order.status = OrderStatus.PAID
        order.save()

        # if order.payment:
        #     return redirect(order.get_absolute_url())

        payment = Payment.objects.create(
            method='qr-promptpay',
            order=order,
            amount=order.get_total(),
            receipt=receipt_file,
        )

        return redirect(payment.order.get_absolute_url())

    return redirect('store:home')
