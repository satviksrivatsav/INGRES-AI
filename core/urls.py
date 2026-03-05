from django.contrib import admin
from django.urls import path, include
from core.views import landing_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_view, name='landing'),
    
    # Auth & Role Management
    path('accounts/', include('accounts.urls')),
    
    # Public Dashboard & General Portal
    path('portal/', include('portal.urls', namespace='portal')),
    
    # AI Assistant (Public & Official)
    path('chatbot/', include('chatbot.urls', namespace='chatbot')),
    
    # Specialized Data Modules
    path('maps/', include('maps.urls', namespace='maps')),
    path('tools/', include('tools.urls', namespace='tools')),
    path('schemes/', include('schemes.urls', namespace='schemes')),
    path('reports/', include('reports.urls', namespace='reports')),
]