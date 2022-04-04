from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from ..models import BankCustomer
from ..serializers import CustomerSerializer, CustomerSmallSerializer
from ..utils import log_update, TwoSerializerListMixin
from ..filters import CustomerFilter
import logging
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from .docs import customer

logger = logging.getLogger(__name__)


@method_decorator(name="get", decorator=swagger_auto_schema(**customer.list_get))
@method_decorator(name="post", decorator=swagger_auto_schema(**customer.post))
class CustomerListView(TwoSerializerListMixin, ListCreateAPIView):

    queryset = BankCustomer.objects.all()
    serializer_class = {
        "GET": CustomerSmallSerializer,
        "POST": CustomerSerializer
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerFilter

    def perform_create(self, serializer):

        serializer.save()
        keys = ["id", "name", "email", "phone", "address"]
        logger.info(f"Created user { {x: serializer.data[x] for x in keys} }.")


@method_decorator(name="get", decorator=swagger_auto_schema(**customer.detail_get))
@method_decorator(name="patch", decorator=swagger_auto_schema(**customer.patch))
@method_decorator(name="put", decorator=swagger_auto_schema(**customer.put))
@method_decorator(name="delete", decorator=swagger_auto_schema(**customer.delete))
class CustomerDetailView(RetrieveUpdateDestroyAPIView):

    queryset = BankCustomer.objects.all()
    serializer_class = CustomerSerializer

    def perform_update(self, serializer):

        serializer.save()
        log_update("Customer", serializer.data["id"], self.request, serializer)

    def perform_destroy(self, instance):

        account_list = ",".join([str(x.id) for x in instance.accounts.all()])
        idx = instance.id
        instance.delete()
        if account_list:

            logger.info(f'Customer {idx} deleted. Accounts {account_list} deleted.')

        else:

            logger.info(f'Customer {idx} deleted.')
