from django.contrib import admin
from .models import BankAccount
from .models import employee , Client
admin.site.register(employee)
admin.site.register(BankAccount)
admin.site.register(Client)
# Register your models here.
