from django.contrib import admin
from .models import GroundwaterData

@admin.register(GroundwaterData)
class GroundwaterDataAdmin(admin.ModelAdmin):
    # Display key metrics for quick oversight [cite: 85, 86]
    list_display = ('district', 'state', 'status_category', 'extraction_percentage', 'is_active_alert', 'created_at')
    
    # Enable filtering by status and state for admin management [cite: 187]
    list_filter = ('status_category', 'state', 'is_active_alert')
    
    # Search by location or description 
    search_fields = ('district', 'state', 'description')
    
    # Highlight critical areas in the admin view [cite: 85, 923]
    def get_risk_status(self, obj):
        if obj.status_category == 'Over-Exploited':
            return "Critical Action Required"
        return obj.status_category