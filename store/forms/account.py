from django import forms


class UpdateAccountForm(forms.Form):
    first_name = forms.CharField(max_length=128, required=False)
    last_name = forms.CharField(max_length=128, required=False)
    phone_number = forms.CharField(max_length=10, required=False)
