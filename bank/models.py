from django.db import models
from .exchange_settings import CURRENCY


class BankCustomer(models.Model):

    name = models.CharField(max_length=100, default="John")
    phone = models.CharField(max_length=100, default="0000")
    email = models.CharField(max_length=100, default="def@ault.default")
    register_datetime = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class BankAccount(models.Model):

    owner = models.ForeignKey(BankCustomer, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=100, choices=CURRENCY, default="EUR")
    closed = models.DateTimeField(null=True)

    @property
    def balance(self):
        return 0
