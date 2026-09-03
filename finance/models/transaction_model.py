from django.db import models
from django.contrib.auth.models import User
from .account_model import Account
from .category_model import Category

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    kind = models.CharField(choices=[("expense", "Gasto"), ("income", "Ingreso")], max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="PEN")
    description = models.CharField(max_length=255, blank=True)
    raw_text = models.TextField(blank=True)  # el mensaje original de Telegram
    source = models.CharField(default="telegram", max_length=20)
    occurred_at = models.DateTimeField(null=True, blank=True)  # fecha del gasto (puede diferir de created_at)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.kind}"
    
    @property
    def effective_date(self):
        """Fecha real del gasto: occurred_at si existe, sino created_at."""
        return self.occurred_at or self.created_at