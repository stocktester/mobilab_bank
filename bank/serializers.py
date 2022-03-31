from rest_framework import serializers
from rest_framework.fields import empty
from .models import BankCustomer, BankAccount
from django.shortcuts import reverse
from .exchange_settings import CUR_DICT
import re


class CustomerSerializer(serializers.ModelSerializer):

    accounts = serializers.SerializerMethodField("get_accounts")

    class Meta:

        model = BankCustomer
        fields = ["id", "name", "phone", "email", "register_datetime", "modified", "accounts"]

    def __init__(self, instance=None, data=empty, context=None, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)
        scheme = context["request"].scheme
        host = context["request"].get_host()
        self.scheme_host = f'{scheme}://{host}'

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

    def get_accounts(self, instance):

        accounts = instance.accounts.all()
        acc_list = [dict(
            id=x.id,
            account_name=x.account_name,
            balance=f'{x.balance} {x.currency}',
            ref=f'{self.scheme_host}{reverse("bank:account_detail", kwargs={"pk": x.id})}'
        ) for x in accounts]

        return acc_list


class AccountSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField('get_status')

    class Meta:

        model = BankAccount
        exclude = ["closed"]

    def __init__(self, instance=None, data=empty, context=None, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)
        scheme = context["request"].scheme
        host = context["request"].get_host()
        self.scheme_host = f'{scheme}://{host}'

    def to_representation(self, instance):

        response = super().to_representation(instance)

        owner_dict = dict(
            id=instance.owner.id,
            name=instance.owner.name,
            ref=f'{self.scheme_host}{reverse("bank:customer_detail", kwargs={"pk": instance.owner.id})}'
        )
        response["owner"] = owner_dict

        response["currency"] = dict(
            code=instance.currency,
            name=CUR_DICT[instance.currency]
        )

        return response

    @staticmethod
    def get_status(instance):

        if not instance.closed:
            return "open"
        else:
            return "closed"


