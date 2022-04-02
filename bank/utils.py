from django.conf import settings
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import empty
from .currency_data import *
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


def get_rates():

    result = INPLACE_RATES

    try:

        url = settings.BANK["API_URL"] + settings.BANK["API_METHODS"]["list"]()
        response = requests.get(url)
        if response.status_code == 200 and response.json()["success"]:

            result = response.json()["rates"]

        else:

            logger.error("API not working correctly. Returning inplace dictionary.")

    except (KeyError, TypeError) as e:

        logger.error(f"API is not set properly: {e}")

    except requests.exceptions.RequestException as e:

        logger.error("API not working correctly. Returning inplace dictionary.")

    finally:

        return result
