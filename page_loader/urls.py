import os
import re
import logging
from urllib.parse import urlparse


def to_dirname(url: str) -> str:
    url = url[:-1] if url.endswith("/") else url
    parsed_url = urlparse(url)

    path, ext = os.path.splitext(parsed_url.path)

    filename = f"{parsed_url.netloc}{path}"
    filename += f"?{parsed_url.query}" if parsed_url.query else ""
    filename = re.sub(r"\W", "-", filename)

    full_filename = filename + "_files"
    logging.info(f"Create name '{full_filename}' for  directory of "
                 f"references of '{url}'")

    return full_filename


def to_filename(url: str) -> str:
    url = url[:-1] if url.endswith("/") else url
    parsed_url = urlparse(url)

    path, ext = os.path.splitext(parsed_url.path)

    filename = f"{parsed_url.netloc}{path}"
    filename += f"?{parsed_url.query}" if parsed_url.query else ""
    filename = re.sub(r"\W", "-", filename)

    ext = ext if ext else ".html"
    full_filename = filename + ext
    logging.info(f"Create name '{full_filename}' for url '{url}'")

    return full_filename


def is_local(page_url: str, full_item_url: str) -> bool:
    page_url_netloc = urlparse(page_url).netloc
    item_url_netloc = urlparse(full_item_url).netloc

    return page_url_netloc == item_url_netloc
