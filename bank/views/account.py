from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import BankAccount
from ..serializers import AccountSerializer
from ..utils import log_update
import logging

logger = logging.getLogger(__name__)


class AccountListView(ListCreateAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:

            keys = ["id", "owner", "currency", "account_name"]
            log_data = {x: response.data[x] for x in keys}
            log_data["owner"] = response.data["owner"]["id"]
            log_data["currency"] = response.data["currency"]["code"]
            logger.info(f"Created account {log_data}.")
        return response


class AccountDetailView(RetrieveUpdateDestroyAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = AccountSerializer

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            log_update("Account", kwargs['pk'], request, response)

        return response

    def destroy(self, request, *args, **kwargs):

        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            logger.info(f"Account {kwargs['pk']} deleted.")

        return response




