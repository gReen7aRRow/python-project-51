import os
from urllib.parse import urljoin
import logging

from progress.bar import ChargingBar

from page_loader.file_system import make_dir, save_file
from page_loader.resource import request, parsing_html
from page_loader.urls import to_dirname, to_filename, is_local


ASSETS_TYPES = {
    "img": "src",
    "script": "src",
    "link": "href"
}


def find_all_elements(soup, page_url: str) -> list:
    all_tags = []

    for tag, attr in ASSETS_TYPES.items():

        for asset in soup.find_all(tag):
            asset_url = asset.get(attr)

            if asset_url:
                full_asset_url = urljoin(page_url + "/", asset_url)

                filename = to_filename(full_asset_url)

                all_tags.append({
                        "url": full_asset_url,
                        "filename": filename
                    })

    return all_tags


def filter_elements(all_tags: list, page_url: str):
    for asset in all_tags:
        full_asset_url = asset['url']

        if is_local(page_url, full_asset_url):
            pass
        else:
            all_tags.remove(asset)


def _download_assets(assets_to_download: list, assets_path: str) -> None:
    if not os.path.isdir(assets_path):
        logging.info(f"Create directory '{assets_path}' for assets")
        make_dir(assets_path)

    logging.info("Starting downloading assets")

    bar_name = "Downloading assets: "
    for asset in ChargingBar(bar_name).iter(assets_to_download):
        response = request(asset["url"])
        asset_path = os.path.join(assets_path, asset["filename"])
        save_file(asset_path, response.content)


def change_attr_to_local_path(tags_list, page_url, assets_dir_name):
    for tag, attr in ASSETS_TYPES.items():

        for asset in tags_list:

            asset_url = asset.get(attr)

            if asset_url:
                full_asset_url = urljoin(page_url + "/", asset_url)

                filename = to_filename(full_asset_url)

                rel_filepath = os.path.join(assets_dir_name, filename)

                asset[attr] = rel_filepath


def download(url: str, path=os.getcwd()) -> str:
    page_name = to_filename(url)
    assets_dir_name = to_dirname(url)
    assets_path = os.path.join(path, assets_dir_name)

    response = request(url)
    soup = parsing_html(response.text)
    tags_list = find_all_elements(soup, url)
    filter_elements(tags_list, url)

    if tags_list:
        _download_assets(tags_list, assets_path)
        change_attr_to_local_path(tags_list, url, assets_dir_name)

    page_path = save_file(os.path.join(path, page_name),
                          soup.prettify())

    return page_path

