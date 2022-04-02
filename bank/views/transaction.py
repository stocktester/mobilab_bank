from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Transaction, TransactionExtra
from ..serializers import TransactionSerializer, TransactionSmallSerializer
from ..utils import get_rates, TwoSerializerListMixin
import logging

logger = logging.getLogger(__name__)


class TransactionView(TwoSerializerListMixin, ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = {
        "GET": TransactionSmallSerializer,
        "POST": TransactionSerializer
    }

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer_class()

        transaction = serializer(data=request.data, context={"request": request})
        transaction.is_valid(raise_exception=True)
        data = transaction.validated_data

        currency = data.get("currency")
        from_account = data.get("from_account")

        to_currency = data["to_account"].currency
        currency = currency if currency else getattr(from_account, "currency", to_currency)
        from_currency = getattr(from_account, "currency", to_currency)

        # Validate amount if from_currency == currency and from_account exists

        if ((from_account and
             from_currency == currency and
             from_account.balance < data["amount"])):
            return Response({
                'error': f"Account #{from_account.id} doesn't have enough balance to complete the transaction."
            }, status.HTTP_400_BAD_REQUEST)

        # Make api call if needed

        if not (currency == to_currency == from_currency):
            rates = get_rates()

            if not rates:
                rates = dict()
                rates.__setitem__(currency, 1)
                rates.__setitem__(to_currency, 1)
                rates.__setitem__(from_currency, 1)
        else:
            rates = {currency: 1}

        # Calculating amounts in corresponding currencies

        trans_2_base = 1 / rates.get(currency, 1)
        trans_2_to = rates.get(to_currency, 1) * trans_2_base
        trans_2_from = rates.get(from_currency, 1) * trans_2_base

        to_amount = data['amount'] * trans_2_to
        from_amount = data['amount'] * trans_2_from

        # Validating the amount

        if from_account and from_account.balance < from_amount:
            return Response({
                'error': f"Account #{from_account.id} doesn't have enough balance to complete the transaction."
            }, status.HTTP_400_BAD_REQUEST)

        transaction_obj = transaction.save(currency=currency)

        extra = TransactionExtra(
            from_amount=from_amount,
            to_amount=to_amount,
            transaction=transaction_obj
        )

        extra.save()
        logger.info(f"Transferred {data['amount']} {currency} {f'from {from_account.id} ' if from_account else ''}to "
                    f"{data['to_account'].id}.")
        return Response(transaction.data, status.HTTP_201_CREATED)


class TransactionDetailView(RetrieveAPIView):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
