from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # null = categoría global
    name = models.CharField(max_length=80)
    kind = models.CharField(choices=[("expense", "Gasto"), ("income", "Ingreso")], max_length=10)
    
    def __str__(self):
        return f'{self.user} - {self.name}'