from django.conf import settings
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import empty
import requests
import logging

logger = logging.getLogger(__name__)


class SchemeHostModelSerializer(ModelSerializer):

    def __init__(self, instance=None, data=empty, context=None, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)
        scheme = context["request"].scheme
        host = context["request"].get_host()
        self.scheme_host = f'{scheme}://{host}'


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


def log_update(object_name, pk, request, response):

    edited_keys = [x for x in request.data.keys() if x in response.data.keys()]
    if edited_keys:
        edited_data = ",".join(map(lambda x: f"{x} => {request.data[x]}", edited_keys))
        logger.info(f"{object_name} {pk} modified: {edited_data}")


def convert_currency(src="USD", dst="EUR", amount=1):

    API_METHODS = settings.BANK.get("API_METHODS", dict())

    try:

        alt_value = API_METHODS["error"](src, dst, amount)

    except (KeyError, TypeError) as e:

        logger.error("No error_method defined in API_METHODS. Returning 1.00 as exchange rate.")
        return amount

    try:
        url = API_METHODS["convert"](src, dst, amount)
        response = requests.get(url)

        if (response.status_code != 200) or (not response.json()["success"]):
            logger.critical("Exchange api not working. Returning error_method value as exchange rate.")
            return alt_value

        data = response.json()
        return float(data["result"])
    except (KeyError, TypeError) as e:

        logger.error(
            f"No convert method defined in API_METHODS. Returning error_method value as exchange rate: {e}")
        return alt_value

    except requests.exceptions.RequestException as e:

        logger.critical(f"Exchange api not working. Returning error_method value as exchange rate: {e}")
        return alt_value
