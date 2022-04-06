import random
from decimal import Decimal, getcontext
from django.test import TestCase, tag
from bank.currency_data import CUR_DICT
from bank import serializers, models
from unittest.mock import Mock
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import SerializerMethodField
from bank import utils
from django.shortcuts import reverse
from collections import deque
from django.utils import timezone


class SerializerTests(TestCase):

    def setUp(self):

        self.context = {
            "request": Mock(_current_scheme_host="http://test_url.test")
        }

    @property
    def customer(self):

        if not getattr(self, "_customer", None):
            self._customer = models.BankCustomer()
            self._customer.save()
        
        return self._customer

    @property
    def accounts(self):

        if not self.customer.accounts.all():
            for _ in range(5):
                account = models.BankAccount(owner=self.customer, currency="IRR")
                account.save()

        return self.customer.accounts.all()

    @property
    def transactions(self):

        if not getattr(self, "_transactions", None):

            transactions = list()

            for account in self.accounts:

                transaction = models.Transaction(
                    to_account=account,
                    amount=1000,
                    currency="IRR"
                )
                transaction.save()

                extra = models.TransactionExtra(
                    to_amount=1000,
                    from_amount=1000,
                    transaction=transaction
                )
                extra.save()

                transactions.append(transaction.id)

            account_list = deque(self.accounts)
            account_list.rotate(1)
            for from_account, to_account in zip(self.accounts, account_list):

                amount = 500 + random.randint(1001, 10000) / 10000
                transaction = models.Transaction(
                    to_account=to_account,
                    from_account=from_account,
                    amount=amount,
                    currency="IRR"
                )

                transaction.save()
                extra = models.TransactionExtra(
                    to_amount=amount,
                    from_amount=amount,
                    transaction=transaction
                )
                extra.save()

                transactions.append(transaction.id)

            self._transactions = models.Transaction.objects.filter(pk__in=transactions)

        return self._transactions

    @tag("serializer", "unit")
    def test_costume_model_serializer_get_ref(self):

        class TestSerializer(utils.SchemeHostModelSerializer):
            ref = SerializerMethodField("get_ref")

            class Meta:
                model = models.BankCustomer
                fields = '__all__'
                path_name = "bank:customer_detail"

        serialized = TestSerializer(self.customer, context=self.context)
        reverse_ = reverse("bank:customer_detail", kwargs={
            'pk': self.customer.id
        })
        self.assertEqual(serialized.data["ref"], f"http://test_url.test"
                                                 f"{reverse_}")

    @tag("serializer", "integration")
    def test_customer_serializer_representation(self):

        serializer = serializers.CustomerSerializer(self.customer)

        self.assertCountEqual(self.accounts, self.accounts)
        response = serializer.to_representation(self.customer)
        self.assertEqual(len(response["accounts"]), 5)
        self.assertEqual(response["accounts"][0]["balance"], "0 IRR")

    @tag("serializer", "unit")
    def test_customer_serializer_validation(self):

        data = models.BankCustomer().__dict__

        serializer = serializers.CustomerSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            self.fail("Serializer did not validate data.")

        data["phone"] = "abcdefgh"
        serializer = serializers.CustomerSerializer(data=data)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

        data["phone"] = "+123456"
        data["email"] = "123456"
        serializer = serializers.CustomerSerializer(data=data)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

    @tag("serializer", "integration")
    def test_account_serializer_create(self):

        account_data = {
            "owner": self.customer.id,
            "deposit": 5000,
            "close": True,
            "open": False
        }
        serializer = serializers.AccountSerializer(data=account_data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            self.fail("Serializer did not validate data.")

        response = serializer.create(serializer.validated_data)
        self.assertEqual(serializer.validated_data['deposit'], 5000)
        self.assertTrue(serializer.validated_data['close'])
        self.assertFalse(serializer.validated_data['open'])
        self.assertIsInstance(response, models.BankAccount)
        response.delete()

    @tag("serializer", "integration")
    def test_account_serializer_representation(self):

        serializer = serializers.AccountSerializer()
        response = serializer.to_representation(self.accounts.first())

        self.assertIsInstance(response["owner"], dict)
        self.assertIsInstance(response["currency"], dict)
        self.assertIn("code", response["currency"])
        self.assertIn("name", response["currency"])
        self.assertEqual(response["currency"]["code"], "IRR")
        self.assertEqual(response["currency"]["name"], CUR_DICT["IRR"])

    @tag("serializer", "integration")
    def test_account_serializer_status(self):

        serializer = serializers.AccountSerializer()

        account_closed = self.accounts.first()
        account_closed.closed = timezone.now()
        account_closed.save()

        self.assertEqual(serializer.get_status(account_closed), "closed")

        account_closed.closed = None
        account_closed.save()

        self.assertEqual(serializer.get_status(account_closed), "open")

    @tag("serializer", "integration")
    def test_account_serializer_balance(self):

        serializer = serializers.AccountSerializer()
        account = self.accounts.first()

        self.assertEqual(self.transactions, self.transactions)
        balance = serializer.get_balance(account)
        self.assertEqual(len(str(balance).split('.')[1]), 2)
        self.assertEqual(balance, round(account.balance, 2))

    @tag("serializer", "integration")
    def test_account_serializer_validate_open_close(self):

        data = dict(
            open=True,
            close=True
        )
        serializer = serializers.AccountSerializer(self.accounts.first(), data=data, partial=True)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

    @tag("serializer", "integration")
    def test_transaction_serializer_representation(self):

        serializer = serializers.TransactionSerializer()

        with_from = self.transactions.filter(from_account__isnull=False).first()
        null_from = self.transactions.filter(from_account__isnull=True).first()

        response_from = serializer.to_representation(with_from)
        response_null = serializer.to_representation(null_from)

        self.assertIn("from", response_from)
        self.assertIn("to", response_from)
        self.assertIsNone(response_null["from"])
        self.assertIsNotNone(response_from["from"])
        self.assertNotIn("balance", response_from["to"])
        self.assertNotIn("balance", response_from["from"])

    @tag("serializer", "integration")
    def test_transaction_serializer_validate_to_account(self):

        from_account = self.accounts.first()
        to_account = self.accounts.last()
        to_account.closed = timezone.now()
        to_account.save()

        data = {
            "from_account": from_account.id,
            "to_account": from_account.id,
            "amount": 100
        }

        serializer = serializers.TransactionSerializer(data=data)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

        data["to_account"] = to_account.id
        serializer = serializers.TransactionSerializer(data=data)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

        to_account.closed = None
        to_account.save()

    @tag("serializer", "integration")
    def test_transaction_serializer_validate_from_account(self):

        from_account = self.accounts.first()
        to_account = self.accounts.last()
        from_account.closed = timezone.now()
        from_account.save()

        data = {
            "from_account": from_account.id,
            "to_account": to_account.id,
            "amount": 200
        }

        serializer = serializers.TransactionSerializer(data=data)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

    @tag("serializer", "unit")
    def test_transaction_small_serializer_get_amount(self):

        serializer = serializers.TransactionSmallSerializer()
        transaction = models.Transaction(amount=1000.2, currency="BTC")

        self.assertEqual(serializer.get_amount(transaction), "1000.2 BTC")
