from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("avatar", "role", "bio")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Дополнительно",
            {
                "classes": ("wide",),
                "fields": ("email", "role"),
            },
        ),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
