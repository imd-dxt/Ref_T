from rest_framework import viewsets
from .models import Client, Bankaccount, Transaction
from api.serializers import ClientSerializer, BankaccountSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from grpc_client import scan_url

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

@csrf_exempt
def scan_url_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        if url:
            status, report = scan_url(url)
            return JsonResponse({'status': status, 'report': report})
        else:
            return JsonResponse({'error': 'URL is required'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
