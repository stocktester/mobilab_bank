from django_filters import rest_framework as filters
from .models import Transaction, BankAccount, BankCustomer


class TransactionFilter(filters.FilterSet):
    created = filters.DateTimeFromToRangeFilter()
    order = filters.OrderingFilter(
        fields={
            ('from_account', 'from_account'),
            ('to_account', 'to_account'),
            ('currency', 'currency'),
            ('created', 'created')
        }
    )

    class Meta:
        model = Transaction
        fields = ['from_account', 'to_account', 'currency']


class AccountFilter(filters.FilterSet):

    account_name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    created = filters.DateTimeFromToRangeFilter()
    modified = filters.DateTimeFromToRangeFilter()
    is_closed = filters.BooleanFilter(method='filter_closed')

    class Meta:
        model = BankAccount
        fields = ["owner", "currency", "id"]

    @staticmethod
    def filter_closed(qs, name, value):

        assert name == "is_closed"
        return qs.filter(closed__isnull=(not value))


class CustomerFilter(filters.FilterSet):

    email = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    register = filters.DateTimeFromToRangeFilter(field_name="register_datetime")
    modified = filters.DateTimeFromToRangeFilter()


    class Meta:
        model = BankCustomer
        fields = ["id", "name", "email"]

