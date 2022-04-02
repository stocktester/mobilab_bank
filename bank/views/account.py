from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import BankAccount
from ..serializers import AccountSerializer, AccountSmallSerializer
from ..utils import log_update, TwoSerializerListMixin
import logging

logger = logging.getLogger(__name__)


class AccountListView(TwoSerializerListMixin, ListCreateAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = {
        "GET": AccountSmallSerializer,
        "POST": AccountSerializer
    }

    def perform_create(self, serializer):
        serializer.save()
        keys = ["id", "owner", "currency", "account_name"]
        log_data = {x: serializer.data[x] for x in keys}
        log_data["owner"] = serializer.data["owner"]["id"]
        log_data["currency"] = serializer.data["currency"]["code"]
        logger.info(f"Created account {log_data}.")


class AccountDetailView(RetrieveUpdateDestroyAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = AccountSerializer

    def perform_update(self, serializer):
        serializer.save()
        log_update("Account", serializer.data["id"], self.request, serializer)

    def perform_destroy(self, instance):
        idx = instance.id
        instance.delete()
        logger.info(f"Account {idx} deleted.")



