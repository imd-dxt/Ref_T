from rest_framework import viewsets
from .models import employee, BankAccount, Client
from .serializers import EmployeeSerializer, BankAccountSerializer, ClientSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = employee.objects.all()
    serializer_class = EmployeeSerializer


    def get_queryset(self):
        queryset = employee.objects.all()
        name = self.request.query_params.get('name')
        userID = self.request.query_params.get('userID')
        organizationID = self.request.query_params.get('organizationID')
        role = self.request.query_params.get('role')
        if name is not None:
            queryset = queryset.filter(name=name)
        if userID is not None:
            queryset = queryset.filter(userID=userID)
        if organizationID is not None:
            queryset = queryset.filter(organizationID=organizationID)
        if role is not None:
            queryset = queryset.filter(role=role)
        return queryset

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()

    serializer_class = BankAccountSerializer

    def get_queryset(self):
        queryset = BankAccount.objects.all()
        account_number = self.request.query_params.get('account_number')
        account_holder = self.request.query_params.get('account_holder')
        account_type = self.request.query_params.get('account_type')
        balance = self.request.query_params.get('balance')
        if account_number is not None:
            queryset = queryset.filter(account_number=account_number)
        if account_holder is not None:
            queryset = queryset.filter(account_holder=account_holder)
        if account_type is not None:
            queryset = queryset.filter(account_type=account_type)
        if balance is not None:
            queryset = queryset.filter(balance=balance)
        return queryset

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    def get_queryset(self):
        queryset = Client.objects.all()
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')
        phone = self.request.query_params.get('phone')
        subscription_date = self.request.query_params.get('subscription_date')
        if name is not None:
            queryset = queryset.filter(name=name)
        if email is not None:
            queryset = queryset.filter(email=email)
        if phone is not None:
            queryset = queryset.filter(phone=phone)
        if subscription_date is not None:
            queryset = queryset.filter(subscription_date=subscription_date)
        return queryset
