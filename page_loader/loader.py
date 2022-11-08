import os
from urllib.parse import urljoin
import logging

from bs4 import BeautifulSoup
from progress.bar import ChargingBar

from page_loader.file_system import make_dir, save_file
from page_loader.resource import request
from page_loader.urls import to_dirname, to_filename, is_local


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

                if is_local(page_url, full_asset_url):
                    filename = to_filename(full_asset_url)

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
        response = request(asset["url"])
        asset_path = os.path.join(assets_path, asset["filename"])
        save_file(asset_path, "wb", response.content)


def download(url: str, path=os.getcwd()) -> str:
    response = request(url)

    page_name = to_filename(url)
    assets_dir_name = to_dirname(url)
    assets_path = os.path.join(path, assets_dir_name)

    soup = BeautifulSoup(response.text, features="html.parser")
    assets_to_download = _switch_assets(soup, url, assets_dir_name)

    page_path = save_file(os.path.join(path, page_name),
                          "w",
                          soup.prettify())

    if assets_to_download:
        _download_assets(assets_to_download, assets_path)

    return page_path
