import csv
import random
from bank.currency_data import CURRENCY


class CustomerAccountGenerator:

    first_names = None
    surnames = None
    account_names = None
    currency = None

    def __new__(cls, *args, **kwargs):

        instance = super().__new__(cls, *args, **kwargs)

        if not cls.first_names:
            with open("names/firstnames.csv", "r") as csv_file:

                csv_reader = csv.reader(csv_file, delimiter=',')
                cls.first_names = [x[1] for x in csv_reader]

        if not cls.surnames:
            with open("names/surnames.csv", "r") as csv_file:

                csv_reader = csv.reader(csv_file, delimiter=',')
                cls.surnames = [x[1] for x in csv_reader]

        if not cls.account_names:

            with open("names/account_names.csv", "r") as csv_file:

                csv_reader = csv.reader(csv_file, delimiter=',')
                cls.account_names = [x[0] for x in csv_reader]

        if not cls.currency:
            cls.currency = [x[0] for x in CURRENCY if not x[0].startswith("X")]

        return cls

    @classmethod
    def generate_customer_data(cls, iterate=1):

        surnames = cls.surnames
        first_names = cls.first_names
        domains = ["com", "org", "net", "io", "co.uk", "de", "nl", "fr"]
        for _ in range(iterate):
            random.shuffle(first_names)
            random.shuffle(surnames)
            for f_name, l_name in zip(first_names, surnames):

                block = random.randint(1, 30)
                floor = random.randint(1, 10)
                phone = random.randint(10000000, 99999999)
                ext = random.choice(domains)
                customer = {
                    "name": f"{f_name} {l_name}",
                    "email": f"{f_name}@{l_name}.{ext}",
                    "address": f"Test Street, Block {block}, Fl. {floor}",
                    "phone": f"+{phone}"
                }
                yield customer

    @classmethod
    def generate_account(cls):

        account_names = cls.account_names
        account = {
            "currency": random.choice(cls.currency),
            "account_name": random.choice(account_names)
        }

        return account
