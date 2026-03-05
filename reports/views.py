import csv
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from portal.models import GroundwaterData
from .models import GroundwaterReport  # Fixed the model name

@login_required
def report_trends_view(request):
    """
    FR-7.1: Graphical visualizations for multi-year data.
    FR-3.3: Summarize observed trends.
    """
    # Get district from profile or query param
    user_profile = getattr(request.user, 'profile', None)
    target_district = request.GET.get('district', user_profile.district if user_profile else "Guntur")

    # Fetch data history for this district
    data_history = GroundwaterData.objects.filter(district__iexact=target_district).order_by('created_at')

    # Prep data for the template
    chart_labels = [d.created_at.strftime('%Y') for d in data_history]
    chart_extraction = [d.extraction_percentage for d in data_history]
    chart_recharge = [d.recharge_value for d in data_history]

    # LOGGING/SNAPSHOT LOGIC:
    # We save a snapshot of this analysis into the GroundwaterReport model
    if data_history.exists():
        GroundwaterReport.objects.create(
            user=request.user,
            title=f"{target_district} Multi-Year Analysis",
            report_type='trend',
            district=target_district,
            data_payload={
                'labels': chart_labels,
                'extraction': chart_extraction,
                'recharge': chart_recharge
            },
            summary_notes=f"Automated trend report generated for {target_district}."
        )

    context = {
        'district': target_district,
        'history': data_history,
        'labels_js': json.dumps(chart_labels),
        'extraction_js': json.dumps(chart_extraction),
        'recharge_js': json.dumps(chart_recharge),
        'page_title': f"INGRES Trend Report: {target_district}"
    }
    return render(request, 'reports/trend_report.html', context)

@login_required
def export_csv_view(request):
    """Generates a raw CSV file for research use."""
    district = request.GET.get('district', 'All')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="INGRES_{district}_Report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Year', 'District', 'State', 'Status', 'Extraction %', 'Recharge (MCM)'])

    queryset = GroundwaterData.objects.all()
    if district != 'All':
        queryset = queryset.filter(district__iexact=district)

    for data in queryset:
        writer.writerow([
            data.created_at.year, 
            data.district, 
            data.state, 
            data.status_category, 
            data.extraction_percentage, 
            data.recharge_value
        ])

    return response