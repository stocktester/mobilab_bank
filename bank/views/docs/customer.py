list_get = dict(
        operation_description="Returns list of customers. "
                              "The list can be filtered. "
                              "The result json is also paginated. "
                              "limit and offset can be passed as parameters. "
                              "Below is a full list of all query parameters "
                              "available to filter the result.\n"
                              "Note: register and modified are datetime filters, but the "
                              "correct usage is with `_after` or `_before` postfixes.\n"
                              "example: `register_before=2021-04-01T12:39:22Z`",
    )

post = dict(
        operation_description="Creates a new customer."
    )

patch = dict(
        operation_description="Updates customer with partial data. "
                              "Request can contain one or more attributes to change.",
    )

put = dict(
        operation_description="Updates customer completely (replace data). "
                              "Request data can not be partial."
    )


delete = dict(
        operation_description="Deletes a customer.",
    )

detail_get = dict(
        operation_description="Get detail of a customer. Simply returns one customer by id.",
    )

