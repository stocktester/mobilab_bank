import datetime
import logging

from django.conf import settings
from django.test import TestCase, tag
from bank import utils
from bank import models
from unittest.mock import Mock
from rest_framework import serializers, generics
from django.shortcuts import reverse
from bank.currency_data import INPLACE_RATES, ChoiceDict


class UtilityTests(TestCase):

    @tag("utility", "serializer", "unit")
    def test_costume_model_serializer_get_ref(self):

        class TestSerializer(utils.SchemeHostModelSerializer):
            ref = serializers.SerializerMethodField("get_ref")

            class Meta:
                model = models.BankCustomer
                fields = '__all__'
                path_name = "bank:customer_detail"

        customer = models.BankCustomer()
        customer.save()
        serialized = TestSerializer(customer, context={
            "request": Mock(_current_scheme_host="http://test_url.test")
        })
        reverse_ = reverse("bank:customer_detail", kwargs={
            'pk': customer.id
        })
        self.assertEqual(serialized.data["ref"], f"http://test_url.test"
                                                 f"{reverse_}")

    @tag("utility", "view_mixin", "unit")
    def test_two_serializer_mixin_pass(self):

        class TestMixin(utils.TwoSerializerListMixin,
                        generics.GenericAPIView):

            pass

        view_test = TestMixin(format_kwarg=None)
        view_test.serializer_class = {'GET': object, 'POST': dict}
        view_test.request = Mock(method="GET")
        self.assertEqual(view_test.get_serializer_class(), object)
        view_test.request = Mock(method="POST")
        self.assertEqual(view_test.get_serializer_class(), dict)

    @tag("utility", "view_mixin", "unit")
    def test_two_serializer_mixin_fail(self):

        class TestMixin(utils.TwoSerializerListMixin,
                        generics.GenericAPIView):
            pass

        view_test = TestMixin(format_kwarg=None)
        view_test.serializer_class = object
        view_test.request = Mock(method="GET")
        self.assertRaisesRegex(AssertionError,
                               "`serializer_class` attribute when using"
                               " TwoSerializerListMixin should be a"
                               " dictionary", view_test.get_serializer_class)

        view_test.serializer_class = dict()
        view_test.request = Mock(method="GET")
        self.assertRaisesMessage(AssertionError,
                                 "There is no GET key in "
                                 "`serializer_class` attribute",
                                 view_test.get_serializer_class)

    @tag("utility", "unit")
    def test_get_rates_type(self):

        rates = utils.get_rates()
        self.assertIsInstance(rates, dict)

    @tag("utility", "unit")
    def test_get_rates_cached(self):

        utils.cached_data = None
        utils.cache_time = None

        rates1 = utils.get_rates()
        self.assertIsInstance(utils.cached_data, dict)
        self.assertIsInstance(utils.cache_time, datetime.datetime)
        rates2 = utils.get_rates()
        self.assertEqual(rates1, rates2)

    @tag("utility", "unit")
    def test_get_rates_api_error(self):

        hold_it = settings.BANK["API_URL"]
        settings.BANK["API_URL"] = "http://mmm.nnn"
        self.assertEqual(utils.get_rates(), INPLACE_RATES)
        settings.BANK["API_URL"] = "https://google.com"
        self.assertEqual(utils.get_rates(), INPLACE_RATES)
        settings.BANK.pop("API_URL")
        self.assertEqual(utils.get_rates(), INPLACE_RATES)
        settings.BANK["API_URL"] = hold_it

    @tag("utility", "unit")
    def test_choice_dict(self):

        test_dict = ChoiceDict(((1, "one"), (2, "two")))
        self.assertEqual(test_dict[1], "one")
        self.assertEqual(test_dict[2], "two")
        self.assertEqual(test_dict["one"], 1)
        self.assertEqual(test_dict["two"], 2)

        test_dict[3] = "three"
        self.assertEqual(test_dict[3], "three")
        self.assertEqual(test_dict["three"], 3)

        test_dict[4] = "two"
        self.assertNotIn(2, test_dict)
        self.assertIn("two", test_dict)
        test_dict[3] = "six"
        self.assertNotIn("three", test_dict)
        self.assertIn(3, test_dict)

        del test_dict[4]
        self.assertRaises(KeyError, lambda: test_dict["two"])

        three_num, six_char = test_dict.pop(3)
        self.assertRaises(KeyError, lambda: test_dict["six"])
        self.assertRaises(KeyError, lambda: test_dict[3])
        self.assertEqual(six_char, "six")
        self.assertEqual(three_num, 3)

        self.assertEqual(len(test_dict), 1)

    @tag("utility", "unit")
    def test_log_update(self):

        obj = "Model"
        pk = 10
        request = Mock(data=dict(a=1, b=2, t=7))
        serializer = Mock(data=dict(a=5, b=2, c=7))

        with self.assertLogs('bank', level="INFO") as log_stream:
            utils.log_update(obj, pk, request, serializer)
            self.assertEqual(log_stream.output[0]
                             .split('INFO:bank.utils:')[1],
                             "Model 10 modified: a => 1,b => 2")
