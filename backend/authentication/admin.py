from django.contrib import admin
from .models import User, role
admin.site.register(role)
admin.site.register(User)