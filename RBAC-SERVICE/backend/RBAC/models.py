from django.db import models
from django.db.models import F
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class RequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.method} {self.endpoint} at {self.timestamp}"

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits')]
    )
    IDnumber = models.CharField(max_length=8)
    def __str__(self):
        return self.full_name

class Bankaccount(models.Model):
    account_number = models.CharField(max_length=10)
    account_type = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  f"{self.account_type} Account - {self.account_number}"

class Transaction(models.Model):
    DEPOSIT = 'deposit'
    RETRIEVE = 'retrieve'
    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (RETRIEVE, 'Retrieve'),
    ]

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        default=DEPOSIT,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    sender = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sender', default=None)
    receiving_account = models.ForeignKey(Bankaccount, on_delete=models.CASCADE, related_name='receiving_account')
    transaction_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
    
    def save(self, *args, **kwargs):
        if self.transaction_type == self.DEPOSIT:
            self.receiving_account.balance = F('balance') + self.amount
        elif self.transaction_type == self.RETRIEVE:
            self.receiving_account.balance = F('balance') - self.amount
        self.receiving_account.save()
        super().save(*args, **kwargs)

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    date_hired = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"