from django.db import models
class employee(models.Model):
    name = models.CharField(max_length=200)
    userID = models.CharField(max_length=10)
    organizationID = models.CharField(max_length=10)
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True) 
    account_holder = models.CharField(max_length=100)  
    account_type = models.CharField(
        max_length=20,
        choices=[('savings', 'Savings'), ('current', 'Current')],
        default='savings',
    ) 
    balance = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.account_holder} - {self.account_number}"


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    subscription_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
