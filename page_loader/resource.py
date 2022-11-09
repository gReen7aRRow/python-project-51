import logging
import requests
from bs4 import BeautifulSoup

from page_loader.exceptions import NetworkError


def request(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.ConnectionError as exception:
        logging.info(f"Connection error. {exception}")
        raise NetworkError(exception)

    except requests.Timeout as exception:
        logging.info(f"Timeout error. {exception}")
        raise NetworkError(exception)

    except requests.TooManyRedirects as exception:
        logging.info(f"TooManyRedirectsError. {exception}")
        raise NetworkError(exception)

    except requests.HTTPError as exception:
        logging.info(f"Status bad code: {response.status_code}. {exception}")
        raise NetworkError(exception)

    return response


def parsing_html(response):
    return BeautifulSoup(response, features='html.parser')
