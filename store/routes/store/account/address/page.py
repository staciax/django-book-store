from http import HTTPMethod

from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse

from store.core.metadata import Metadata
from store.core.routers import render
from store.metadata import metadata
from store.models import Address


@login_required(login_url='/login')
@metadata(title='ที่อยู่ของฉัน')
def page(request: HttpRequest) -> HttpResponse:
    """account-address"""
    if request.method == HTTPMethod.POST:
        metadata = Metadata(title='เพิ่มที่อยู่')
        return render(
            request,
            __file__,
            {'form_action': reverse('store:create-address')},
            filename='_components/add-address.html',
            metadata=metadata,
        )

    addresses = Address.objects.filter(user=request.user).order_by('created_at').all()
    address_count = addresses.count()
    context = {
        'addresses': addresses,
        'address_is_full': address_count >= 5,
    }
    return render(request, __file__, context)
