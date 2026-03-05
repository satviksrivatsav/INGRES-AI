from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def technical_reference_view(request):
    """
    FR-4.1 & 4.2: Explains groundwater parameters and status categories
    using simplified terminology for the public and researchers.
    """
    definitions = [
        {"term": "Safe", "desc": "Groundwater draft is less than 70% of recharge.", "color": "green"},
        {"term": "Semi-Critical", "desc": "Draft is between 70% and 90% of recharge.", "color": "amber"},
        {"term": "Critical", "desc": "Draft is between 90% and 100% of recharge.", "color": "orange"},
        {"term": "Over-Exploited", "desc": "Draft exceeds 100% of annual recharge.", "color": "red"},
    ]
    return render(request, 'tools/reference.html', {'definitions': definitions})