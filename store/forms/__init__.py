from .account import UpdateAccountForm
from .addresses import CreateAddressForm, UpdateAddressForm
from .auth import ForgotPasswordForm, LoginForm, RegisterForm
from .orders import CreateOrderForm

__all__ = (
    'CreateAddressForm',
    'CreateOrderForm',
    'ForgotPasswordForm',
    'LoginForm',
    'RegisterForm',
    'UpdateAccountForm',
    'UpdateAddressForm',
)
