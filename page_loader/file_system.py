import os
import logging

from page_loader.exceptions import FileSystemError


def make_dir(path: str) -> str:
    logging.info(f"Creating '{path}'")

    try:
        os.mkdir(path)

    except FileExistsError:
        logging.info(f"{path} already exists.")

    except PermissionError as exception:
        logging.info(exception)
        raise FileSystemError(exception)

    except FileNotFoundError as exception:
        logging.info(exception)
        raise FileSystemError(exception)

    logging.info(f"{path} was created")
    return path


def save_file(filename: str, data: any) -> str:
    logging.info(f"Starting to save '{filename}'")

    mode = 'wb' if isinstance(data, bytes) else 'w'

    try:
        with open(filename, mode) as file:
            file.write(data)

    except FileNotFoundError as exception:
        logging.info(exception)
        raise FileSystemError(exception)

    except OSError as exception:
        logging.info(exception)
        raise FileSystemError(exception)

    logging.info(f"File '{filename}' was saved with mode '{mode}'")
    return filename
