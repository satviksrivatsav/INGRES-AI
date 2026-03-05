from django.urls import path
from . import views

app_name = 'schemes'

urlpatterns = [
    # Main searchable directory
    path('directory/', views.schemes_directory_view, name='directory'),
]