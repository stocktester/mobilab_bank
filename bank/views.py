from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import BankAccount, BankCustomer
from .serializers import AccountSerializer, CustomerSerializer


class CustomerListView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):

        customers = BankCustomer.objects.all()
        serialized = CustomerSerializer(customers, many=True)
        return Response(serialized.data)

    @staticmethod
    def post(request, *args, **kwargs):

        serialized = CustomerSerializer(data=request.data)

        if serialized.is_valid():

            serialized.save()
            return Response(serialized.data, status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):

    @staticmethod
    def get_customer(pk):

        try:
            customer = BankCustomer.objects.get(pk=pk)
            return customer
        except BankCustomer.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):

        customer = self.get_customer(kwargs["pk"])
        serialized = CustomerSerializer(customer)

        return Response(serialized.data)

    def put(self, request, *args, **kwargs):

        customer = self.get_customer(kwargs["pk"])
        serialized = CustomerSerializer(customer, data=request.data)

        if serialized.is_valid():

            serialized.save()
            return Response(serialized.data)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):

        customer = self.get_customer(kwargs["pk"])
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






