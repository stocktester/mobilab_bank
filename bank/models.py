from django.db import models


class BankCustomer(models.Model):

    name = models.CharField(max_length=100, default="John")
    phone = models.CharField(max_length=100, default="0000")
    email = models.CharField(max_length=100, default="def@ault.default")
    register_datetime = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class BankAccount(models.Model):

    account_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=3, default="EUR")
    balance = models.FloatField(default=0)
    closed = models.DateTimeField(null=True)
