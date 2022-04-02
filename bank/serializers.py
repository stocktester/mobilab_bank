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
        fields = ["id", "name", "phone", "address", "email", "register_datetime", "modified", "accounts"]

    def to_representation(self, instance):

        response = super().to_representation(instance)

        response["accounts"] = AccountSmallSerializer(instance.accounts.all(),
                                                      many=True,
                                                      context=self._context).data
        return response

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


class CustomerSmallSerializer(SchemeHostModelSerializer):

    ref = serializers.SerializerMethodField("get_ref")

    class Meta:

        model = BankCustomer
        fields = ['id', 'name', 'phone', 'address', 'email', 'ref']
        path_name = "bank:customer_detail"


class AccountSerializer(SchemeHostModelSerializer):

    status = serializers.SerializerMethodField('get_status')
    balance = serializers.SerializerMethodField('get_balance')

    class Meta:

        model = BankAccount
        exclude = ["closed"]

    def to_representation(self, instance):

        response = super().to_representation(instance)

        owner_dict = CustomerSmallSerializer(instance.owner, context=self._context)
        response["owner"] = owner_dict.data

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

        return round(instance.balance, 2)


class AccountSmallSerializer(SchemeHostModelSerializer):

    ref = serializers.SerializerMethodField('get_ref')
    balance = serializers.SerializerMethodField('get_balance')

    class Meta:

        model = BankAccount
        fields = ["id", "owner", "balance", "ref"]
        path_name = "bank:account_detail"

    @staticmethod
    def get_balance(instance):
        return f"{round(instance.balance, 2)} {instance.currency}"


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

            from_account = AccountSmallSerializer(instance.from_account, context=self._context).data
            from_account.pop("balance")

        else:

            from_account = None

        to_account = AccountSmallSerializer(instance.to_account, context=self._context).data
        to_account.pop("balance")

        response.pop("from_account")
        response.pop("to_account")

        response["from"] = from_account
        response["to"] = to_account
        response["amount"] = f'{instance.amount}'
        return response

    def validate_to_account(self, value):

        from_account_id = self.initial_data.get("from_account")
        if from_account_id and from_account_id == value.id:
            raise serializers.ValidationError("to_account and from_account must be different.")
        return value


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

