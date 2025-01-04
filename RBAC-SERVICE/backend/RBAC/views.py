from rest_framework import viewsets
from .models import Client, Bankaccount, Transaction, RequestLog
from api.serializers import ClientSerializer, BankaccountSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from grpc_client import scan_url
from api.serializers import RequestLogSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class BankaccountViewSet(viewsets.ModelViewSet):
    queryset = Bankaccount.objects.all()
    serializer_class = BankaccountSerializer
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

class RequestLogViewSet(viewsets.ModelViewSet):
    queryset = RequestLog.objects.all()
    serializer_class = RequestLogSerializer
    permission_classes = [IsAdminUser]
    
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
