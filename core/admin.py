from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_superuser")
    
    fieldsets = (
        ("Basic Info", {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        ("username", {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "first_name", "last_name", "is_staff", "is_superuser"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)

    def save_model(self, request, obj, form, change):
        """Ensure username is set to email before saving"""
        if not obj.username:
            obj.username = obj.email
        obj.save()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
