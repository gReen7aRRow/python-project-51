#!/usr/bin/env python3

from page_loader.cli import parse_args
from page_loader.loader import download


def main():
    url, path, debug = parse_args()
    full_path = download(url, path)
    print(full_path)


if __name__ == '__main__':
    main()
