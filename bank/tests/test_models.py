from django.test import TestCase
from django.test import tag
from bank import models


class ModelTests(TestCase):

    @tag("model", "unit")
    def test_account_balance(self):

        customer = models.BankCustomer()
        customer.save()
        account1 = models.BankAccount(owner=customer)
        account2 = models.BankAccount(owner=customer)
        account1.save()
        account2.save()

        for _ in range(10):
            transaction = models.Transaction(from_account=account1, to_account=account2, amount=1000)
            transaction.save()
            models.TransactionExtra(from_amount=1000, to_amount=1000, transaction=transaction).save()

        self.assertEqual(account1.balance, -10000)
        self.assertEqual(account2.balance, 10000)
