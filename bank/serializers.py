from rest_framework import serializers
from .models import BankCustomer, BankAccount
import re


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:

        model = BankCustomer
        fields = '__all__'

    @staticmethod
    def validate_phone(value):

        pattern = r'^\+\d+$'
        if not re.fullmatch(pattern, value):
            raise serializers.ValidationError(
                "Phone number must start with + and only contain numbers after that.")

        return value

    @staticmethod
    def validate_email(value):

        pattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
        if not re.fullmatch(pattern, value):
            raise serializers.ValidationError("Email address is not in correct format.")

        return value


class AccountSerializer(serializers.ModelSerializer):

    class Meta:

        model = BankAccount
        fields = '__all__'

