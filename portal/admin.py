import csv
import json
import io

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from .models import GroundwaterData

@admin.register(GroundwaterData)
class GroundwaterDataAdmin(admin.ModelAdmin):
    # Display key metrics for quick oversight
    list_display = ('district', 'state', 'status_category', 'extraction_percentage', 'is_active_alert', 'created_at')
    
    # Enable filtering by status and state for admin management
    list_filter = ('status_category', 'state', 'is_active_alert')
    
    # Search by location or description 
    search_fields = ('district', 'state', 'description')

    change_list_template = 'admin/portal/groundwaterdata/change_list.html'

    def get_urls(self):
        custom_urls = [
            path('import-data/', self.admin_site.admin_view(self.import_data), name='import_groundwater_data'),
        ]
        return custom_urls + super().get_urls()

    def import_data(self, request):
        if request.method == 'POST' and request.FILES.get('data_file'):
            uploaded = request.FILES['data_file']
            filename = uploaded.name.lower()
            created_count = 0

            try:
                content = uploaded.read().decode('utf-8')

                if filename.endswith('.json'):
                    rows = json.loads(content)
                    for item in rows:
                        # Support both flat dict and fixture format
                        fields = item.get('fields', item)
                        created_count += self._upsert_entry(fields)

                elif filename.endswith('.csv'):
                    reader = csv.DictReader(io.StringIO(content))
                    for row in reader:
                        created_count += self._upsert_entry(row)

                messages.success(request, f'Successfully imported {created_count} new groundwater record(s).')
            except Exception as e:
                messages.error(request, f'Import failed: {e}')

        return HttpResponseRedirect('../')

    def _upsert_entry(self, fields):
        """Create or update a single GroundwaterData entry from a dict."""
        district = fields.get('district', '').strip()
        state = fields.get('state', '').strip()
        if not district or not state:
            return 0

        status = fields.get('status_category', fields.get('status', 'Safe')).strip()
        extraction = float(fields.get('extraction_percentage', fields.get('extract', 0)))
        recharge = float(fields.get('recharge_value', fields.get('recharge', 0)))
        lat = fields.get('latitude', fields.get('lat'))
        lon = fields.get('longitude', fields.get('lon'))
        year = fields.get('assessment_year', 2023)
        desc = fields.get('description', f"Groundwater assessment for {district}. Status: {status}.")

        defaults = {
            'status_category': status,
            'extraction_percentage': extraction,
            'recharge_value': recharge,
            'description': desc,
            'is_active_alert': status in ('Critical', 'Over-Exploited'),
            'assessment_year': int(year),
        }
        if lat is not None and lat != '':
            defaults['latitude'] = float(lat)
        if lon is not None and lon != '':
            defaults['longitude'] = float(lon)

        _, created = GroundwaterData.objects.update_or_create(
            district=district,
            state=state,
            defaults=defaults
        )
        return 1 if created else 0

    # Highlight critical areas in the admin view
    def get_risk_status(self, obj):
        if obj.status_category == 'Over-Exploited':
            return "Critical Action Required"
        return obj.status_category