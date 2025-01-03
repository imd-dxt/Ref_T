from django.urls import path
from .views import scan_view, scan_results_view

urlpatterns = [
    path('scan/', scan_view, name='scan'),
    path('scan/results/<int:scan_id>/', scan_results_view, name='scan_results'),
]
