from rest_framework import serializers
from .models import employee
from .models import BankAccount, Client

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('account_number', 'account_holder', 'account_type', 'balance', 'created_at', 'updated_at')

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = ('name', 'userID', 'organizationID', 'role')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'subscription_date')