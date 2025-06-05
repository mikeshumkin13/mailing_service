from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_active', 'is_manager', 'is_staff')
    list_filter = ('is_manager', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_manager',)}),
    )

