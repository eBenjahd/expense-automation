from django.db import models
from django.contrib.auth.models import User
from .category_model import Category

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="PEN")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "currency"],
                name="unique_budget_per_user_category_currency"
            )
        ]

    def __str__(self):
        return f"{self.category.name}: {self.monthly_limit} {self.currency}"