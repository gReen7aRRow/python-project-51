import pytest
from requests.exceptions import ConnectionError

from page_loader.loader import download
from page_loader.exceptions import (PLFileExistsException,
                                    PLConnectionException)

URL = "https://example.ru"
HTML_PAGE = "Never mind"



@pytest.mark.parametrize("error, exception",
                         [(ConnectionError, PLConnectionException)])
def test_connection_exceptions(requests_mock, error, exception):
    requests_mock.register_uri("GET", URL, exc=error)
    with pytest.raises(exception):
        _ = download(URL)


@pytest.mark.parametrize("dir_path, exception",
                         [("not/existent/dir", PLFileExistsException)])
def test_file_exceptions(requests_mock, dir_path, exception):
    requests_mock.register_uri("GET", URL, text=HTML_PAGE)
    with pytest.raises(exception):
        _ = download(URL, dir_path)
