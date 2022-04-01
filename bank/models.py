from django.db import models
from .transaction_settings import CURRENCY
from .utils import convert_currency
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
    def balance_eur(self):

        all_in = self.in_transactions.aggregate(models.Sum('amount')).get("amount__sum", 0)
        all_out = self.out_transactions.aggregate(models.Sum('amount')).get("amount__sum", 0)
        all_in = all_in if all_in else 0
        all_out = all_out if all_out else 0

        result = all_in - all_out
        if result < 0:
            logger.error(f'Account {self.id} has negative balance.')

        return result

    @property
    def balance(self):

        result = self.balance_eur
        if result:
            result = convert_currency(src='EUR', dst=self.currency, amount=result)
        return result


class Transaction(models.Model):

    from_account = models.ForeignKey(BankAccount, null=True, on_delete=models.SET_NULL, related_name='out_transactions')
    to_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='in_transactions')
    amount = models.FloatField()  # amount will always store as EUR
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250, default="0 EUR")


