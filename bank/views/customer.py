from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import BankCustomer
from ..serializers import CustomerSerializer, CustomerSmallSerializer
from ..utils import log_update, TwoSerializerListMixin
import logging

logger = logging.getLogger(__name__)


class CustomerListView(TwoSerializerListMixin, ListCreateAPIView):

    queryset = BankCustomer.objects.all()
    serializer_class = {
        "GET": CustomerSmallSerializer,
        "POST": CustomerSerializer
    }

    def perform_create(self, serializer):

        serializer.save()
        keys = ["id", "name", "email", "phone", "address"]
        logger.info(f"Created user { {x: serializer.data[x] for x in keys} }.")


class CustomerDetailView(RetrieveUpdateDestroyAPIView):

    queryset = BankCustomer.objects.all()
    serializer_class = CustomerSerializer

    def perform_update(self, serializer):

        serializer.save()
        log_update("Customer", serializer.data["id"], self.request, serializer)

    def perform_destroy(self, instance):

        account_list = ",".join([str(x.id) for x in instance.accounts])
        idx = instance.id
        instance.delete()
        if account_list:

            logger.info(f'Customer {idx} deleted. Accounts {account_list} deleted.')

        else:

            logger.info(f'Customer {idx} deleted.')
