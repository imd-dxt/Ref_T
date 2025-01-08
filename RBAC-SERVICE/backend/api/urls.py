from django.urls import path, include
from rest_framework.routers import DefaultRouter
from RBAC.views import ClientViewSet, BankaccountViewSet, TransactionViewSet, RequestLogViewSet, get_user_permissions
from .views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'bankaccounts', BankaccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'logs', RequestLogViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-permissions/', get_user_permissions, name='user-permissions'),
]