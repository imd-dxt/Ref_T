from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
#Create your models here...
class role(models.Model):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('sys_admin', 'System Administrator'),
        ('engineer', 'Engineer'),
        ('manager', 'Manager'),
    ]
    name = models.CharField(max_length=100, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class User (AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email
