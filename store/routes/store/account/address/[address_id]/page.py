from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse

from store.core.routers import render
from store.metadata import metadata
from store.models import Address


@login_required(login_url='/login')
@metadata(title='แก้ไขที่อยู่')
def page(request: HttpRequest, address_id: int) -> HttpResponse:
    """address-edit"""
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:  # noqa: TRY203
        raise

    context = {
        'address': address,
        'form_action': reverse(
            'store:update-address',
            kwargs={'address_id': address.id},
        ),
    }
    return render(request, context)
