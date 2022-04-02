from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.utils import timezone
from ..models import BankAccount, Transaction, TransactionExtra
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

        # log data

        keys = ["id", "owner", "currency", "account_name"]
        log_data = {x: serializer.data[x] for x in keys}
        log_data["owner"] = serializer.data["owner"]["id"]
        log_data["currency"] = serializer.data["currency"]["code"]

        # Check if deposit provided

        deposit = serializer.validated_data.get("deposit")
        if deposit:

            log_data["deposit"] = deposit
            transaction = Transaction(
                to_account=serializer.instance,
                amount=deposit
            )

            transaction.save()

            extra = TransactionExtra(
                from_amount=deposit,
                to_amount=deposit,
                transaction=transaction
            )

            extra.save()

            serializer._data["balance"] = serializer.instance.balance

        # log

        logger.info(f"Created account {log_data}.")


class AccountDetailView(RetrieveUpdateDestroyAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = AccountSerializer

    def perform_update(self, serializer):

        if serializer.validated_data.get("close", False) and not serializer.instance.closed:
            serializer.save(closed=timezone.now())
            logger.critical(f"Account {serializer.instance.id} closed.")
        elif serializer.validated_data.get("open", False) and serializer.instance.closed:
            serializer.save(closed=None)
            logger.info(f"Account {serializer.instance.id} opened again.")
        else:
            serializer.save()
            log_update("Account", serializer.instance.id, self.request, serializer)

    def perform_destroy(self, instance):
        idx = instance.id
        instance.delete()
        logger.info(f"Account {idx} deleted.")



