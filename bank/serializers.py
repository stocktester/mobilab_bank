from rest_framework import serializers
from bank.models import BankCustomer, BankAccount


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:

        model = BankCustomer
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):

    class Meta:

        model = BankAccount
        fields = '__all__'

