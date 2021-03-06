from django.test import TestCase, tag
from rest_framework.test import APIRequestFactory
from django.shortcuts import reverse
from bank.views import CustomerListView


class CustomerListViewTests(TestCase):

    def setUp(self) -> None:

        self.factory = APIRequestFactory()

    @tag("view")
    def test_getting_list(self) -> None:

        request = self.factory.get(reverse("bank:customer"))
        response = CustomerListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @tag("view")
    def test_making_new_customer(self) -> None:

        new_user = dict(
            name="Test Test",
            phone="+9891123",
            email="test@test.test"
        )

        request = self.factory.post(reverse("bank:customer"), new_user)
        response = CustomerListView.as_view()(request)
        self.assertEqual(response.status_code, 201)

    @tag("view")
    def test_valid_phone(self) -> None:

        new_user = dict(
            name="Test Test",
            phone="Test",
            email="test@test.test"
        )

        request = self.factory.post(reverse("bank:customer"), new_user)
        response = CustomerListView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    @tag("view")
    def test_valid_email(self) -> None:

        new_user = dict(
            name="Test Test",
            phone="+9891123",
            email="testtesttest"
        )

        request = self.factory.post(reverse("bank:customer"), new_user)
        response = CustomerListView.as_view()(request)
        self.assertEqual(response.status_code, 400)

