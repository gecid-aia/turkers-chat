from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "user_type"),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
