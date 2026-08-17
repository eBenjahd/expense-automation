from django.contrib import admin
from finance.models import Account, Transaction, Budget, Category

# Register your models here.
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Category)