from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    path('reference/', views.technical_reference_view, name='reference'),
]