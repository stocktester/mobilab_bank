from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import BankAccount
from ..serializers import AccountSerializer
import logging

logger = logging.getLogger(__name__)


class AccountListView(ListCreateAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = AccountSerializer


