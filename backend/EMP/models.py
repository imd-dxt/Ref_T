from django.db import models
class employee(models.Model):
    name = models.CharField(max_length=200)
    userID = models.CharField(max_length=10)
    organizationID = models.CharField(max_length=10)
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.name

