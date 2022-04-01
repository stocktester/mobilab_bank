class ReverseDict(dict):

    def __setitem__(self, key, value):

        if key in self:
            del self[key]
        if value in self:
            del self[value]

        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):

        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):

        return dict.__len__(self) // 2


class ChoiceDict(ReverseDict):

    def __init__(self, choice_tuple: tuple = None):

        holder_dict = {x[0]: x[1] for x in choice_tuple}
        super().__init__(**holder_dict)


def log_update(object_name, pk, request, response, logger):

    edited_keys = [x for x in request.data.keys() if x in response.data.keys()]
    if edited_keys:
        edited_data = ",".join(map(lambda x: f"{x} => {request.data[x]}", edited_keys))
        logger.info(f"{object_name} {pk} modified: {edited_data}")


