from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Transaction
from ..serializers import TransactionSerializer
import logging

logger = logging.getLogger(__name__)


class TransactionView(ListAPIView):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):

        return Response({self.request}, status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #
    #     data = serializer.validated_data
    #     currency = self.request.data.get("currency", None)
    #     from_account = data.get("from_account", None)
    #     to_id = data['to_account'].id
    #     from_id = None if not from_account else from_account.id
    #     if not currency:
    #         if not from_account:
    #             serializer.save(description=f"{data['amount']} EUR")
    #             logger.info(f"{data['amount']} EUR transferred to {to_id}")
    #             return
    #         else:
    #             currency = from_account.currency
    #             amount = convert_currency(src=currency, amount=data["amount"])
    #             serializer.save(amount=amount, description=f"{data['amount']} {currency}")
    #             logger.info(f"{data['amount']} {currency} transferred from {from_id} to {to_id}")
    #             return
    #
    #     amount = convert_currency(src=currency, amount=data["amount"])
    #     serializer.save(amount=amount, description=f"{data['amount']} {currency}")
    #     logger.info(f"{data['amount']} {currency} transferred from {from_id} to {to_id}")










