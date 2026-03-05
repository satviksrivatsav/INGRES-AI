from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('trends/', views.report_trends_view, name='trend_analysis'),
    path('export/csv/', views.export_csv_view, name='export_csv'),
]