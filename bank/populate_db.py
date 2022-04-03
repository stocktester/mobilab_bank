from django.core.management.commands.flush import Command
from django.conf import settings
from names import CustomerAccountGenerator
import logging
import random

logger = logging.getLogger(__name__)


def populate():

    from .models import BankCustomer, BankAccount, Transaction, TransactionExtra
    from .utils import get_rates
    options = settings.BANK["POPULATE"]
    generator = CustomerAccountGenerator()

    if settings.BANK.get("FLUSH", False):

        logger.critical("Populate: FLUSH switch is set. Flushing database.")
        cmd = {"database": "default", "interactive": False, "verbosity": 1}
        Command().handle(**cmd)
        logger.critical("Database flushed.")
        print("Populate: Database flushed.")

    if options.get("customer", False):

        n = 2
        for customer in generator.generate_customer_data(iterate=n):

            new_customer = BankCustomer(**customer)
            new_customer.save()

        print(f"Populate: Created {n * 20} random customers.")

    if options.get("account", False):

        id_list = BankCustomer.objects.values_list('id')
        id_list = [x[0] for x in id_list]

        n = 4
        length = len(id_list)
        counter = 0

        for iteration in range(n):

            random.shuffle(id_list)
            id_list = id_list[:length]
            length //= 2

            for idx in id_list:

                account = generator.generate_account()
                new_account = BankAccount(**account, owner_id=idx)
                new_account.save()
                counter += 1

        print(f"Populate: Created {counter} accounts for customers.")

    if options.get("transaction", False):

        account_queryset = BankAccount.objects.all()
        account_id_list = BankAccount.objects.values_list()

        for account in account_queryset:

            transaction_data = {
                "to_account": account,
                "amount": 20000,
                "currency": account.currency,
                "description": "Deposit"
            }

            new_transaction = Transaction(**transaction_data)
            new_transaction.save()
            extra = {
                "to_amount": 20000,
                "from_amount": 20000,
                "transaction_id": new_transaction.id
            }
            new_extra = TransactionExtra(**extra)
            new_extra.save()

        print("Populate: each account now has 20000 balance.")

        rates = get_rates()
        for account in account_queryset:

            n = 4
            amount = 20000

            for iteration in range(n):

                amount //= 2
                target = random.choice(account_queryset)
                rate = rates[target.currency] / rates[account.currency]

                to_amount = amount * rate

                transaction_data = {
                    "from_account": account,
                    "amount": amount,
                    "to_account": target,
                    "currency": account.currency,
                    "description": f"From {account.id} to {target.id} as gift."
                }

                new_transaction = Transaction(**transaction_data)
                new_transaction.save()
                extra = {
                    "to_amount": to_amount,
                    "from_amount": amount,
                    "transaction_id": new_transaction.id
                }
                new_extra = TransactionExtra(**extra)
                new_extra.save()

        print(f"Populate: each account has {n} outgoing transactions now.")

    print("Populate: Populate Completed.")

    with open(".populated", "w") as pop_file:

        pop_file.write("true")



















