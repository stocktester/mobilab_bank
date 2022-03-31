from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import BankCustomer
from ..serializers import CustomerSerializer
import logging

logger = logging.getLogger(__name__)


class CustomerListView(ListCreateAPIView):

    queryset = BankCustomer.objects.all()
    serializer_class = CustomerSerializer

    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)
        if response.status_code == 201:
            keys = ["id", "name", "email", "phone"]
            logger.info(f"Created user { {x: response.data[x] for x in keys} }.")
        return response


class CustomerDetailView(RetrieveUpdateDestroyAPIView):

    queryset = BankCustomer.objects.all()
    serializer_class = CustomerSerializer

    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            edited_data = ",".join(map(lambda x: f"{x} => {request.data[x]}", request.data.keys()))
            logger.info(f"Customer {kwargs['pk']} modified: {edited_data}")

        return response

    def destroy(self, request, *args, **kwargs):

        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            logger.info(f"Customer {kwargs['pk']} deleted.")

        return response

