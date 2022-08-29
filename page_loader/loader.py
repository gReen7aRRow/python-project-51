import os
import re
from urllib.parse import urlparse, urljoin
import logging

from bs4 import BeautifulSoup
from progress.bar import ChargingBar

from page_loader.file_system import make_dir, save_file
from page_loader.network import make_request


def _generate_name(url: str, is_dir=False) -> str:
    url = url[:-1] if url.endswith("/") else url
    parsed_url = urlparse(url)

    path, ext = os.path.splitext(parsed_url.path)

    filename = f"{parsed_url.netloc}{path}"
    filename += f"?{parsed_url.query}" if parsed_url.query else ""
    filename = re.sub(r"\W", "-", filename)

    if is_dir:
        full_filename = filename + "_files"
        logging.info(f"Create name '{full_filename}' for  directory of "
                     f"references of '{url}'")
        return full_filename

    ext = ext if ext else ".html"
    full_filename = filename + ext
    logging.info(f"Create name '{full_filename}' for url '{url}'")

    return full_filename


def _is_local_asset(page_url: str, full_item_url: str) -> bool:
    page_url_netloc = urlparse(page_url).netloc
    item_url_netloc = urlparse(full_item_url).netloc

    return page_url_netloc == item_url_netloc


def _switch_assets(soup, page_url: str, assets_dir_name: str) -> list:
    logging.info("Starting analyzing page assets")

    asset_types = {
        "img": "src",
        "script": "src",
        "link": "href"
    }
    assets_to_download = []

    for tag, attr in asset_types.items():

        assets = soup.find_all(tag)
        for asset in assets:
            logging.info(f"Analyze '{attr}' in '{tag}'")

            asset_url = asset.get(attr)

            if asset_url:
                full_asset_url = urljoin(page_url + "/", asset_url)

                if _is_local_asset(page_url, full_asset_url):
                    filename = _generate_name(full_asset_url)

                    rel_filepath = os.path.join(assets_dir_name, filename)

                    asset[attr] = rel_filepath
                    assets_to_download.append({
                        "url": full_asset_url,
                        "filename": filename
                    })

                    logging.info(f"Switch asset reference "
                                 f"'{asset[attr]}'")

    logging.info("End of analyzing page assets")
    return assets_to_download


def _download_assets(assets_to_download: list, assets_path: str) -> None:
    if not os.path.isdir(assets_path):
        logging.info(f"Create directory '{assets_path}' for assets")
        make_dir(assets_path)

    logging.info("Starting downloading assets")

    bar_name = "Downloading assets: "
    for asset in ChargingBar(bar_name).iter(assets_to_download):
        response = make_request(asset["url"])
        asset_path = os.path.join(assets_path, asset["filename"])
        save_file(asset_path, "wb", response.content)


def download(url: str, path=os.getcwd()) -> str:
    response = make_request(url)

    page_name = _generate_name(url)
    assets_dir_name = _generate_name(url, is_dir=True)
    assets_path = os.path.join(path, assets_dir_name)

    soup = BeautifulSoup(response.text, features="html.parser")
    assets_to_download = _switch_assets(soup, url, assets_dir_name)

    page_path = save_file(os.path.join(path, page_name),
                          "w",
                          soup.prettify())

    if assets_to_download:
        _download_assets(assets_to_download, assets_path)

    return page_path
