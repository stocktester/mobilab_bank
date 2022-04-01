from django.db import models
from .transaction_settings import CURRENCY
import logging

logger = logging.getLogger(__name__)


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

        result = 0
        return result


class Transaction(models.Model):

    from_account = models.ForeignKey(BankAccount, null=True, on_delete=models.SET_NULL, related_name='out_transactions')
    to_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='in_transactions')
    amount = models.FloatField()
    currency = models.CharField(max_length=100, choices=CURRENCY, default="EUR")  # By default, from_account.currency
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, default="A simple transaction.")


class TransactionExtra(models.Model):

    from_amount = models.FloatField()
    to_amount = models.FloatField()
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True)

