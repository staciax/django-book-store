from django.http import HttpRequest

from store.models.user import User


class AuthenticatedHttpRequest(HttpRequest):
    user: User
