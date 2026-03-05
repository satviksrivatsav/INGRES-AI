from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from portal.models import GroundwaterData

@login_required
def interactive_map_view(request):
    """
    FR-6.1: Map-based visualization for Andhra Pradesh (POC).
    FR-6.3: Assessment year selection supported.
    """

    # Get selected year (default latest year in dataset)
    selected_year = request.GET.get('year')

    if not selected_year:
        selected_year = 2023
    else:
        selected_year = int(selected_year)

    # Filter by state + selected year
    ap_data = GroundwaterData.objects.filter(
        state__icontains="Andhra Pradesh",
        assessment_year=selected_year
    ).exclude(latitude__isnull=True)

    context = {
        'map_points': ap_data,
        'selected_year': selected_year,
        'page_title': "Andhra Pradesh Intelligence Map"
    }

    return render(request, 'maps/interactive_map.html', context)
