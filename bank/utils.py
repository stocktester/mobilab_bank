from .transaction_settings import API_METHODS
import requests
import logging

logger = logging.getLogger(__name__)


def convert_currency(src="USD", dst="EUR", amount=1):

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

        logger.error(f"No convert method defined in API_METHODS. Returning error_method value as exchange rate: {e}")
        return alt_value

    except requests.exceptions.RequestException as e:

        logger.critical(f"Exchange api not working. Returning error_method value as exchange rate: {e}")
        return alt_value


