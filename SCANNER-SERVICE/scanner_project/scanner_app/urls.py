from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.scan_url, name='submit-scan'),
    path('results/<int:pk>/', views.scan_results, name='scan-results'),
]