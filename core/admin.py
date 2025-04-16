from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "is_active", "cpf",)
    
    fieldsets = (
        ("Basic Info", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "cpf")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        ("username", {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "is_staff", "is_superuser"),
        }),
    )

    ordering = ("-id", )
    search_fields = ("email",)

admin.site.register(User, CustomUserAdmin)
