import csv
import json
import io

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import path
from django.http import HttpResponseRedirect
from .models import ResearchDomainWhitelist

User = get_user_model()

@admin.register(ResearchDomainWhitelist)
class ResearchDomainWhitelistAdmin(admin.ModelAdmin):
    list_display = ('domain',)
    search_fields = ('domain',)
    change_list_template = 'admin/accounts/researchdomainwhitelist/change_list.html'

    def get_urls(self):
        custom_urls = [
            path('import-domains/', self.admin_site.admin_view(self.import_domains), name='import_domains'),
        ]
        return custom_urls + super().get_urls()

    def import_domains(self, request):
        if request.method == 'POST' and request.FILES.get('domain_file'):
            uploaded = request.FILES['domain_file']
            filename = uploaded.name.lower()
            created_count = 0

            try:
                content = uploaded.read().decode('utf-8')

                if filename.endswith('.json'):
                    data = json.loads(content)
                    for entry in data:
                        domain = entry.get('fields', {}).get('domain', '').strip()
                        if domain:
                            _, created = ResearchDomainWhitelist.objects.get_or_create(domain=domain)
                            if created:
                                created_count += 1

                elif filename.endswith('.csv'):
                    reader = csv.reader(io.StringIO(content))
                    for row in reader:
                        if row:
                            domain = row[0].strip()
                            if domain and domain != 'domain':  # skip header
                                _, created = ResearchDomainWhitelist.objects.get_or_create(domain=domain)
                                if created:
                                    created_count += 1

                else:  # plain text: one domain per line
                    for line in content.splitlines():
                        domain = line.strip()
                        if domain:
                            _, created = ResearchDomainWhitelist.objects.get_or_create(domain=domain)
                            if created:
                                created_count += 1

                messages.success(request, f'Successfully imported {created_count} new domain(s).')
            except Exception as e:
                messages.error(request, f'Import failed: {e}')

        return HttpResponseRedirect('../')

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
