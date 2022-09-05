#!/usr/bin/env python3

import sys

from page_loader.loader import download
from page_loader.cli import parse_args
from page_loader.logger_agent import get_logger
from page_loader.exceptions import (PLConnectionException,
                                    PLFileExistsException)


def main():
    url, path, debug = parse_args()
    get_logger(debug_mode=debug)

    try:
        final_path = download(url, path)
    except (PLConnectionException,
            PLFileExistsException) as exception:
        print(str(exception))
        sys.exit(1)

    print(f"Page was successfully downloaded into '{final_path}'")


if __name__ == '__main__':
    main()
