from django.apps import AppConfig
from django.conf import settings
from .populate_db import populate
from os import environ


class BankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank'

    def ready(self):

        try:
            with open(".populated", "r") as pop_file:
                populated = pop_file.read()
        except FileNotFoundError as e:
            populated = False

        if not populated:

            flush = environ.get("FLUSH_DB", False)
            populate_customer = environ.get("POP_CUSTOMER", False)
            populate_account = environ.get("POP_ACCOUNT", False)
            populate_transaction = environ.get("POP_TRANS", False)

            settings.BANK["FLUSH"] = flush
            settings.BANK["POPULATE"] = dict(
                customer=populate_customer,
                account=populate_account,
                transaction=populate_transaction
            )

        if settings.BANK.get("POPULATE", None):
            populate()
