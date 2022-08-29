import os
import tempfile

import pytest

from page_loader.loader import download
from urllib.parse import urljoin

URL = "https://example.ru/subpage"
ASSETS_INFO = ({"path": "css/rel-styles.css",
                "url": "css/rel-styles.css"},
               {"path": "css/abs-styles.css",
                "url": "/css/abs-styles.css"},
               {"path": "css/full-styles.css",
                "url": "https://example.ru/css/full-styles.css"},
               {"path": "img/rel-googlelogo.png",
                "url": "img/rel-googlelogo.png"},
               {"path": "img/abs-googlelogo.png",
                "url": "/img/abs-googlelogo.png"},
               {"path": "img/full-googlelogo.png",
                "url": "https://example.ru/img/full-googlelogo.png"},
               {"path": "js/rel-scripts.js",
                "url": "js/rel-scripts.js"},
               {"path": "js/abs-scripts.js",
                "url": "/js/abs-scripts.js"},
               {"path": "js/full-scripts.js",
                "url": "https://example.ru/js/full-scripts.js"},)

EXPECTED_HTML_DIR = "tests/fixtures/demo_page/out"
EXPECTED_FILENAME = "example-ru-subpage.html"
EXPECTED_ASSETS_DIR = "example-ru-subpage_files"
FIXTURE_DIR = "tests/fixtures/demo_page/in"


@pytest.fixture
def html():
    data = {"url": URL}
    with open(os.path.join(FIXTURE_DIR, "example.html"), "r") as file:
        data["text"] = file.read()
    return data


@pytest.fixture
def assets():
    data = []
    for asset in ASSETS_INFO:
        element = {"url": urljoin(URL + "/", asset["url"])}
        with open(os.path.join(FIXTURE_DIR, asset["path"]), "rb") as file:
            element["content"] = file.read()
        data.append(element)
    return data


def _setup_mock(requests_mock, html, assets):
    url = html["url"]
    requests_mock.get(url, text=html["text"])

    for asset in assets:
        requests_mock.get(asset["url"], content=asset["content"])


def _compare_files_content(result_path, expected_path):
    with open(result_path, "rb") as file:
        result_content = file.read()
    with open(expected_path, "rb") as file:
        expected_content = file.read()

    return result_content == expected_content


def test_download_page(requests_mock, html, assets):
    _setup_mock(requests_mock, html, assets)

    with tempfile.TemporaryDirectory() as temp_dir:
        result = download(URL, temp_dir)
        result_filepath, result_filename = os.path.split(result)
        assert result_filepath == temp_dir
        assert result_filename == EXPECTED_FILENAME

        result_assets_dir = os.path.join(temp_dir,
                                         EXPECTED_ASSETS_DIR)
        expected_assets_dir = os.path.join(EXPECTED_HTML_DIR,
                                           EXPECTED_ASSETS_DIR)

        assert os.path.isdir(result_assets_dir)

        result_assets = sorted(os.listdir(result_assets_dir))
        expected_assets = sorted(os.listdir(expected_assets_dir))
        assert len(result_assets) == len(expected_assets)

        for result_asset_name, expected_asset_name in zip(result_assets,
                                                          expected_assets):
            assert result_asset_name == expected_asset_name

            result_asset_path = os.path.join(temp_dir,
                                             EXPECTED_ASSETS_DIR,
                                             result_asset_name)
            expected_asset_path = os.path.join(EXPECTED_HTML_DIR,
                                               EXPECTED_ASSETS_DIR,
                                               expected_asset_name)
            assert _compare_files_content(result_asset_path,
                                          expected_asset_path)
