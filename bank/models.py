from django.db import models
from .currency_data import CURRENCY
import logging

logger = logging.getLogger(__name__)


class BankCustomer(models.Model):

    name = models.CharField(max_length=100, default="John")
    phone = models.CharField(max_length=100, default="0000")
    email = models.CharField(max_length=100, default="def@ault.default")
    address = models.CharField(max_length=250, default="Simple Address")
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

        sum_in = self.in_transactions.aggregate(value=models.Sum("extra__to_amount")).get("value")
        sum_out = self.out_transactions.aggregate(value=models.Sum("extra__from_amount")).get("value")

        sum_in = sum_in if sum_in else 0
        sum_out = sum_out if sum_out else 0
        return sum_in - sum_out


class Transaction(models.Model):

    class Meta:
        ordering = ['created']

    from_account = models.ForeignKey(BankAccount, null=True, on_delete=models.SET_NULL, related_name='out_transactions')
    to_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='in_transactions')
    amount = models.FloatField()
    currency = models.CharField(max_length=100, choices=CURRENCY, default="EUR")  # By default, from_account.currency
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, default="A simple transaction.")


class TransactionExtra(models.Model):

    from_amount = models.FloatField()
    to_amount = models.FloatField()
    transaction = models.OneToOneField(Transaction,
                                       on_delete=models.CASCADE,
                                       primary_key=True,
                                       related_name="extra")

