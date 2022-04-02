from rest_framework import serializers
from .utils import SchemeHostModelSerializer
from .models import BankCustomer, BankAccount, Transaction
from django.shortcuts import reverse
from .currency_data import CUR_DICT
import re


class CustomerSerializer(SchemeHostModelSerializer):

    accounts = serializers.SerializerMethodField("get_accounts")

    class Meta:

        model = BankCustomer
        fields = ["id", "name", "phone", "email", "register_datetime", "modified", "accounts"]

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


class AccountSerializer(SchemeHostModelSerializer):

    status = serializers.SerializerMethodField('get_status')
    balance = serializers.SerializerMethodField('get_balance')

    class Meta:

        model = BankAccount
        exclude = ["closed"]

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

    @staticmethod
    def get_balance(instance):

        return instance.balance


class TransactionSerializer(SchemeHostModelSerializer):

    from_account = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.all(),
                                                      allow_null=True, required=False)
    currency = serializers.CharField(required=False)

    class Meta:

        model = Transaction
        fields = '__all__'

    def to_representation(self, instance):

        response = super().to_representation(instance)

        if instance.from_account:

            from_account = dict(
                id=instance.from_account.id,
                account_name=instance.from_account.account_name,
                currency=instance.from_account.currency,
                ref=f'{self.scheme_host}{reverse("bank:account_detail", kwargs={"pk": instance.from_account.id})}'
            )

        else:

            from_account = None

        to_account = dict(
            id=instance.to_account.id,
            account_name=instance.to_account.account_name,
            currency=instance.to_account.currency,
            ref=f'{self.scheme_host}{reverse("bank:account_detail", kwargs={"pk": instance.to_account.id})}'
        )

        response["from_account"] = from_account
        response["to_account"] = to_account
        response["amount"] = f'{response["amount"]}'
        return response


class TransactionSmallSerializer(SchemeHostModelSerializer):

    amount = serializers.SerializerMethodField("get_amount")
    ref = serializers.SerializerMethodField("get_ref")

    class Meta:

        model = Transaction
        fields = ['id', 'from_account', 'to_account', 'amount', "ref"]
        path_name = 'bank:transaction_detail'

    @staticmethod
    def get_amount(instance):

        return f"{instance.amount} {instance.currency}"

