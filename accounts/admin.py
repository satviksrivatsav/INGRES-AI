from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import ResearchDomainWhitelist

User = get_user_model()

@admin.register(ResearchDomainWhitelist)
class ResearchDomainWhitelistAdmin(admin.ModelAdmin):
    list_display = ('domain',)
    search_fields = ('domain',)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'email',
        'role',
        'is_active',
        'is_verified',
        'is_staff',
        'login_count',
    )

    list_filter = (
        'role',
        'is_active',
        'is_verified',
        'is_staff',
    )

    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_verified',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
