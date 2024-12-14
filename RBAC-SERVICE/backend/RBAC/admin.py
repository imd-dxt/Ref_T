from django.contrib import admin
from .models import Client, Bankaccount, Transaction, Employee
admin.site.register(Client)
admin.site.register(Bankaccount)
admin.site.register(Transaction)
admin .site.register(Employee)
# Register your models here.
