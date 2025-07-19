from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser

class CustomUserAdmin(UserAdmin):
    model = AppUser
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

admin.site.register(AppUser, CustomUserAdmin)