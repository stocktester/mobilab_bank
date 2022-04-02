from django_filters import rest_framework as filters
from .models import Transaction


class TransactionFilter(filters.FilterSet):
    created = filters.DateTimeFromToRangeFilter(field_name="created")
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
