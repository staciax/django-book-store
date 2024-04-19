from django import forms


class CreateAddressForm(forms.Form):
    full_name = forms.CharField(max_length=256)
    phone_number = forms.CharField(max_length=10)
    street_address = forms.CharField(max_length=256)
    province = forms.CharField(max_length=128)
    district = forms.CharField(max_length=128)
    postal_code = forms.CharField(max_length=5)


class UpdateAddressForm(CreateAddressForm):
    pass
