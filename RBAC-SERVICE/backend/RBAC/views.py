from django.shortcuts import render
from rest_framework import viewsets
from .models import Client, Bankaccount, Transaction
from api.serializers import ClientSerializer, BankaccountSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated

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
# Create your views here.
