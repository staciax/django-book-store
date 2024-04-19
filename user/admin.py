from typing import Any

from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin[User]):
    exclude = ('password',)
    readonly_fields = ('last_login',)

    def save_model(self, request: Any, obj: User, form: Any, change: Any) -> None:
        new_password = request.data.get('password')
        if obj.check_password(new_password):
            obj.set_password(new_password)
        else:
            obj.set_password(obj.password)
        return super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
