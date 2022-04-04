from django.test import TestCase, tag
from bank import serializers, models
from unittest.mock import Mock
from rest_framework.exceptions import ValidationError
import copy


class SerializerTests(TestCase):

    @tag("serializer", "unit")
    def test_customer_serializer_representation(self):

        customer = models.BankCustomer()
        customer.save()
        context = {
            "request": Mock(_current_scheme_host="http://test_url.test")
        }
        for _ in range(5):
            account = models.BankAccount(owner=customer, currency="IRR")
            account.save()

        serializer = serializers.CustomerSerializer(customer,
                                                    context=context)
        response = serializer.to_representation(customer)
        self.assertEqual(len(response["accounts"]), 5)
        self.assertEqual(response["accounts"][0]["balance"], "0 IRR")
        self.assertIn("http://test_url.test", response["accounts"][0]["ref"])

    @tag("serializer", "unit")
    def test_customer_serializer_validation(self):

        customer = models.BankCustomer()
        data = customer.__dict__

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

