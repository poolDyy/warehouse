from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Админка пользователя."""

    search_fields = [
        'email',
    ]


admin.site.register(User, UserAdmin)
