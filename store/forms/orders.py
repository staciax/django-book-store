from django import forms


class CreateOrderForm(forms.Form):
    address_id = forms.IntegerField()
    payment_method = forms.CharField()
