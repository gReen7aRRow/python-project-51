#!/usr/bin/env python3

import logging
import sys

from page_loader.cli import get_args
from page_loader.engine import download


logger = logging.getLogger('base_error')


def main():
    """Select format selection."""
    args = get_args().parse_args()
    try:
        print(download(args.url, args.output))
    except Exception:
        logger.exception("Exception occurred")
        sys.exit(1)


if __name__ == '__main__':
    main()
