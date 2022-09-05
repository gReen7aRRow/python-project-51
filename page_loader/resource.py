import logging
import requests

from page_loader.exceptions import PLConnectionException


def request(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.ConnectionError as exception:
        logging.info(f"Connection error. {exception}")
        raise PLConnectionException(exception)

    return response
