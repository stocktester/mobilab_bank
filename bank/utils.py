from django.conf import settings
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import empty
from .currency_data import INPLACE_RATES
from django.utils import timezone
from functools import partial
import requests
import logging

logger = logging.getLogger(__name__)

cache_time = None
cached_data = None


class SchemeHostModelSerializer(ModelSerializer):

    def __init__(self, instance=None, data=empty, context=None, **kwargs):

        super().__init__(instance=instance, data=data, **kwargs)
        scheme = context["request"].scheme
        host = context["request"].get_host()
        self.scheme_host = f'{scheme}://{host}'


def log_update(object_name, pk, request, response):

    edited_keys = [x for x in request.data.keys() if x in response.data.keys()]
    if edited_keys:
        edited_data = ",".join(map(lambda x: f"{x} => {request.data[x]}", edited_keys))
        logger.info(f"{object_name} {pk} modified: {edited_data}")


def _get_rates(use_cached=True):

    global cache_time
    global cached_data
    if use_cached and cached_data and (timezone.now() - cache_time).total_seconds() < 300:

        logger.info(f"returning cached data instead of calling api.")
        return cached_data

    cached_data = None
    cache_time = None

    result = INPLACE_RATES

    try:

        url = settings.BANK["API_URL"] + settings.BANK["API_METHODS"]["list"]()
        response = requests.get(url)
        if response.status_code == 200 and response.json()["success"]:

            result = response.json()["rates"]
            cached_data = result
            cache_time = timezone.now()
            logger.info("Called api.")

        else:

            logger.error("API not working correctly. Returning inplace dictionary.")

    except (KeyError, TypeError) as e:

        logger.error(f"API is not set properly: {e}")

    except requests.exceptions.RequestException as e:

        logger.error("API not working correctly. Returning inplace dictionary.")

    finally:

        return result


get_rates = partial(_get_rates, use_cached=settings.BANK.get("use_cached", True))

