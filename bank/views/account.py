from rest_framework.generics import RetrieveUpdateDestroyAPIView
from common.utils import UrlLisCreateAPIView
from ..models import BankAccount
from ..serializers import AccountSerializer
import logging

logger = logging.getLogger(__name__)


class AccountListView(UrlLisCreateAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = AccountSerializer


