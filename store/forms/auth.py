from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import User


class ForgotPasswordForm(forms.Form): ...


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=256, required=True)
    password = forms.CharField(max_length=256, required=True)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=128, required=True)
    last_name = forms.CharField(max_length=128, required=True)
    email = forms.EmailField(max_length=256, required=True)
    password1 = forms.CharField(strip=False)
    password2 = forms.CharField(strip=False)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user  # type: ignore[no-any-return]
