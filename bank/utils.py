from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse
from rest_framework.serializers import ModelSerializer
from .currency_data import INPLACE_RATES
from functools import partial
from rest_framework import generics
import requests
import logging

logger = logging.getLogger(__name__)

cache_time = None
cached_data = None


class SchemeHostModelSerializer(ModelSerializer):

    @property
    def scheme_host(self):

        request = self._context.get("request")
        return getattr(request, "_current_scheme_host", "")

    def get_ref(self, instance):
        return f"{self.scheme_host}{reverse(self.Meta.path_name, kwargs={'pk': instance.id})}"


class TwoSerializerListMixin:

    def get_serializer_class(self: generics.GenericAPIView):

        serializers: dict = self.serializer_class

        assert serializers is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        assert type(serializers) is dict, (
                "`serializer_class` attribute when using TwoSerializerListMixin should be a dictionary "
                "which keys are request method types."
        )

        assert serializers.get(self.request.method) is not None, (
                f"There is no {self.request.method} key in `serializer_class` attribute"
        )

        return serializers.get(self.request.method)


def log_update(object_name, pk, request, serializer):

    edited_keys = [x for x in request.data.keys() if x in serializer.data.keys()]
    if edited_keys:
        edited_data = ",".join(map(lambda x: f"{x} => {request.data[x]}", edited_keys))
        logger.info(f"{object_name} {pk} modified: {edited_data}")


def _get_rates(use_cached=True):

    global cache_time
    global cached_data
    if use_cached and cached_data and (timezone.now() - cache_time).total_seconds() < 300:

        logger.info(f"returning cached data instead of calling api.")
        return cached_data, 1

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

        logger.error(f"API not working correctly. Returning inplace dictionary: {e}")

    finally:

        return result, (cached_data is not None)


get_rates = partial(_get_rates, use_cached=settings.BANK.get("use_cached", True))
