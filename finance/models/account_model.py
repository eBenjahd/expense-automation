from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # "Efectivo", "BCP", "Yape"

    def __str__(self):
        return f"{self.user} - {self.name}"#metodo de pago