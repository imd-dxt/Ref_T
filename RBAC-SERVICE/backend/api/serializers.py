# filepath: /d:/ZERO-TRUST/RBAC-SERVICE/backend/api/serializers.py
from rest_framework import serializers
from RBAC.models import Client, Bankaccount, Transaction

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class BankaccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bankaccount
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'