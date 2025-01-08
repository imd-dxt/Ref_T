from rest_framework import viewsets
from .models import Client, Bankaccount, Transaction, RequestLog
from api.serializers import ClientSerializer, BankaccountSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from grpc_client import scan_url
from api.serializers import RequestLogSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class BankaccountViewSet(viewsets.ModelViewSet):
    queryset = Bankaccount.objects.all()
    serializer_class = BankaccountSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class RequestLogViewSet(viewsets.ModelViewSet):
    queryset = RequestLog.objects.all()
    serializer_class = RequestLogSerializer
    permission_classes = [IsAdminUser]

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_permissions(request):
    permissions = []
    for perm in request.user.get_all_permissions():
        app_label, codename = perm.split('.')
        if app_label == 'RBAC':
            permissions.append(codename)
    return Response(permissions)
@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def scan_url_view(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({'detail': 'CORS preflight'})
        response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        if url:
            status, report = scan_url(url)
            response = JsonResponse({'status': status, 'report': report})
            response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            return response
        else:
            response = JsonResponse({'error': 'URL is required'}, status=400)
            response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            return response

    response = JsonResponse({'error': 'Invalid request method'}, status=405)
    response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    return response
