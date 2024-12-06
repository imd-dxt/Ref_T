from django.db import models
class employee(models.Model):
    name = models.CharField(max_length=200)
    userID = models.CharField(max_length=10)
    organizationID = models.CharField(max_length=10)
    role = models.CharField(max_length=200)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name

