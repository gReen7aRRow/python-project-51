import os
import logging

from page_loader.exceptions import PLPermissionException, PLFileExistsException


def make_dir(path: str) -> str:
    logging.info(f"Creating '{path}'")

    try:
        os.mkdir(path)

    except FileExistsError:
        logging.info(f"{path} already exists.")

    except PermissionError as exception:
        logging.info(exception)
        raise PLPermissionException(exception)

    except FileNotFoundError as exception:
        logging.info(exception)
        raise PLFileExistsException(exception)

    logging.info(f"{path} was created")
    return path


def save_file(filename: str, mode: str, data: any) -> str:
    logging.info(f"Starting to save '{filename}'")

    try:
        with open(filename, mode) as file:
            file.write(data)

    except FileNotFoundError as exception:
        logging.info(exception)
        raise PLFileExistsException(exception)

    except OSError as exception:
        logging.info(exception)
        raise PLPermissionException(exception)

    logging.info(f"File '{filename}' was saved with mode '{mode}'")
    return filename
