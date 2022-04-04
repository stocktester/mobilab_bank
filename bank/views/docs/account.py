list_get = dict(
        operation_description="Returns list of accounts. "
                              "The list can be filtered. "
                              "The result json is also paginated. "
                              "limit and offset can be passed as parameters. "
                              "Below is a full list of all query parameters "
                              "available to filter the result.\n"
                              "Note: created and modified are datetime filters, but the "
                              "correct usage is with `_after` or `_before` postfixes.\n"
                              "example: `created_before=2021-04-01T12:39:22Z`",
    )

post = dict(
        operation_description="Creates a new account."
    )

patch = dict(
        operation_description="Updates account with partial data. "
                              "Request can contain one or more attributes to change. \n\n"
                              "Closing accounts: set `close` parameter to `true`. Closed accounts "
                              "can not transfer any money to other accounts, and can not receive "
                              "any transaction.\n"
                              "Openning the closed account: set `open` parameter to `true`.\n"
                              "Notice: both parameters can not be true simultaneously."
    )

put = dict(
        operation_description="Updates account completely (replace data). "
                              "Request data can not be partial. \n\n"
                              "Closing accounts: set `close` parameter to `true`. Closed accounts "
                              "can not transfer any money to other accounts, and can not receive "
                              "any transaction.\n"
                              "Openning the closed account: set `open` parameter to `true`.\n"
                              "Notice: both parameters can not be true simultaneously."
    )


delete = dict(
        operation_description="Deletes an account.",
    )

detail_get = dict(
        operation_description="Get detail of an account. Simply returns one account by id.",
    )

