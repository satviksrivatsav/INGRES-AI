from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # The JSON endpoint for AJAX calls (used by mini-bot and dashboard widgets)
    path('query/', views.chatbot_query, name='query'),
    
    # The dedicated full-page AI Assistant for the Public Dashboard
    path('assistant/', views.full_chat_view, name='public_assistant'),
    
    # Placeholder for Official Policy Bot (implemented in later phase)
    # path('policy-advisor/', views.official_chat_view, name='official_assistant'),
]