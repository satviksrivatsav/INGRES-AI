from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import WaterScheme

@login_required
def schemes_directory_view(request):
    """
    Searchable database for government water schemes.
    Filters based on user's current region and search query.
    """
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    
    # Get user region from profile
    user_profile = getattr(request.user, 'profile', None)
    user_state = user_profile.state if user_profile else ""

    # Logic: Show National (empty state) OR User's specific state
    schemes = WaterScheme.objects.filter(
        Q(state_specific=user_state) | Q(state_specific='')
    )

    # Apply search query
    if query:
        schemes = schemes.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    # Apply category filter
    if category_filter:
        schemes = schemes.filter(category=category_filter)

    context = {
        'schemes': schemes,
        'query': query,
        'selected_cat': category_filter,
        'categories': WaterScheme.CATEGORY_CHOICES,
        'page_title': "Gov Schemes Directory"
    }
    return render(request, 'schemes/directory.html', context)