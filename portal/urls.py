from django.urls import path
from . import views
from schemes.views import schemes_directory_view

app_name = 'portal'

urlpatterns = [
    # Main Public Dashboard Home
    path('dashboard/public/', views.public_dashboard_view, name='public_dashboard'),
    # path('dashboard/researcher/', views.researcher_dashboard_view, name='researcher_dashboard'),
    path('dashboard/official/', views.official_dashboard_view, name='official_dashboard'),
    
    # Profile & Location Settings
    path('profile/', views.profile_settings_view, name='profile'),
    path('planner/', views.water_planner_view, name='water_planner'),
    path('safety-checker/', views.safety_checker_view, name='safety_checker'),
    path('interactive-map/', views.map_view, name='map_view'),
    path('update-location/', views.update_location_view, name='update_location'),
    path('schemes/', schemes_directory_view, name='schemes_directory'),
    path('advisor/', views.conservation_advisor_view, name='conservation_advisor'),
    
    # Placeholder for Official Dashboard (Phase-2)
    # path('official/', views.official_dashboard_view, name='official_dashboard'),
] 