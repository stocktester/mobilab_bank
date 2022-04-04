list_get = dict(
        operation_description="Returns list of transactions. "
                              "The list can be filtered. "
                              "The result json is also paginated. "
                              "limit and offset can be passed as parameters. "
                              "Below is a full list of all query parameters "
                              "available to filter the result.\n"
                              "To use order filter, set it to the required field, "
                              "and change order direction by putting `-` before the field name. "
                              "For example: `order=-created` which will return transactions in"
                              " descending order. \n"
                              "Note: created is a datetime filter, but the "
                              "correct usage is with `_after` or `_before` postfixes.\n"
                              "example: `created_before=2021-04-01T12:39:22Z`",
    )

post = dict(
        operation_description="Creates a new transaction.\n"
                              "Restrictions:\n1. neither from_account, nor to_account can be closed.\n"
                              "2. A transaction from one account to the same account can not happen.\n"
                              "3. A transaction happens if from_account has enough balance."
    )


delete = dict(
        operation_description="Deleting transactions is not safe. It can make an account balance negative, "
                              "which undermines the integrity of the api. Logically, it doesn't make sense "
                              "to delete a transaction. Thus the chain of transactions can not change. This "
                              "endpoint is designed for experimenting and can only delete the last transaction.",
    )

detail_get = dict(
        operation_description="Get detail of a transaction. Simply returns one transaction by id.",
    )

