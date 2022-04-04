from django.test import TestCase, tag
from rest_framework.test import APIRequestFactory
from django.shortcuts import reverse
from bank.views import CustomerDetailView
from bank.models import BankCustomer


class CustomerDetailViewTests(TestCase):

    def setUp(self) -> None:

        self.factory = APIRequestFactory()

        user1 = BankCustomer(
            name="Test User 1",
            phone="+98199881",
            email="Test@User1.test"
        )
        user1.save()
        self.user1_id = user1.id

        user2 = BankCustomer(
            name="Test User 2",
            phone="+98199882",
            email="Test@User2.test"
        )
        user2.save()
        self.user2_id = user2.id

        user3 = BankCustomer(
            name="Test User 3",
            phone="+98199883",
            email="Test@User3.test"
        )
        user3.save()
        self.user3_id = user3.id

    @tag("view")
    def check_response_dict_keys(self, response) -> None:

        self.assertIn("name", response.data)
        self.assertIn("email", response.data)
        self.assertIn("phone", response.data)

    @tag("view")
    def edit_response(self, user_id, data):

        request = self.factory.put(reverse("bank:customer_detail", kwargs={'pk': user_id}),
                                   data)
        response = CustomerDetailView.as_view()(request, pk=user_id)

        return response

    @tag("view")
    def test_get_customer(self) -> None:

        request = self.factory.get(reverse("bank:customer_detail", kwargs={'pk': self.user1_id}))
        response = CustomerDetailView.as_view()(request, pk=self.user1_id)

        self.assertEqual(response.status_code, 200)
        self.check_response_dict_keys(response)
        self.assertEqual(response.data["name"], "Test User 1")
        self.assertEqual(response.data["phone"], "+98199881")
        self.assertEqual(response.data["email"], "Test@User1.test")

    @tag("view")
    def test_get_non_existing_customer(self) -> None:

        request = self.factory.get(reverse("bank:customer_detail", kwargs={'pk': 999}))
        response = CustomerDetailView.as_view()(request, pk=999)

        self.assertEqual(response.status_code, 404)

    @tag("view")
    def test_edit_customer(self) -> None:

        new_user_2 = dict(
            name="New User 2",
            phone="+122345",
            email="test@user2.test"
        )

        response = self.edit_response(self.user2_id, new_user_2)

        self.assertEqual(response.status_code, 200)
        self.check_response_dict_keys(response)
        self.assertEqual(response.data["name"], "New User 2")
        self.assertEqual(response.data["phone"], "+122345")
        self.assertEqual(response.data["email"], "test@user2.test")

    @tag("view")
    def test_edit_customer_with_partial_data(self) -> None:

        new_data_2 = dict(
            phone="+12234512345",
        )

        response = self.edit_response(self.user2_id, new_data_2)

        self.assertEqual(response.status_code, 200)
        self.check_response_dict_keys(response)
        self.assertEqual(response.data["phone"], "+12234512345")

        new_data_2 = dict(
            email="test@test.org",
        )

        response = self.edit_response(self.user2_id, new_data_2)
        self.assertEqual(response.status_code, 200)
        self.check_response_dict_keys(response)
        self.assertEqual(response.data["email"], "test@test.org")

    @tag("view")
    def test_edit_customer_invalid(self) -> None:

        new_data_email = dict(
            email="test_user2.test"
        )

        new_data_phone = dict(
            phone="abcdefg12345"
        )

        response = self.edit_response(self.user2_id, new_data_email)

        self.assertEqual(response.status_code, 400)

        response = self.edit_response(self.user2_id, new_data_phone)

        self.assertEqual(response.status_code, 400)

    @tag("view")
    def test_edit_non_existing_customer(self) -> None:

        new_data = dict(
            email="test@test.org"
        )

        response = self.edit_response(999, new_data)

        self.assertEqual(response.status_code, 404)

    @tag("view")
    def test_delete_customer(self) -> None:

        request = self.factory.delete(reverse("bank:customer_detail", kwargs={'pk': self.user3_id}))
        response = CustomerDetailView.as_view()(request, pk=self.user3_id)

        self.assertEqual(response.status_code, 204)

        request = self.factory.get(reverse("bank:customer_detail", kwargs={'pk': self.user3_id}))
        response = CustomerDetailView.as_view()(request, pk=self.user3_id)

        self.assertEqual(response.status_code, 404)

    @tag("view")
    def test_delete_non_existing_customer(self) -> None:

        request = self.factory.delete(reverse("bank:customer_detail", kwargs={'pk': 999}))
        response = CustomerDetailView.as_view()(request, pk=999)

        self.assertEqual(response.status_code, 404)



