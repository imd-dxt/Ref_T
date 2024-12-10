from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, BankAccountViewSet, ClientViewSet


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'bankaccounts', BankAccountViewSet)
router.register(r'clients', ClientViewSet)
urlpatterns = [
    path('', include(router.urls)),
]