from django.urls import path
from .views import scan_url_view

urlpatterns = [
    path('scan-url/', scan_url_view, name='scan_url'),
]