import pytest
from requests.exceptions import Timeout, ConnectionError, TooManyRedirects

from page_loader.loader import download
from page_loader.exceptions import (NetworkError,
                                    FileSystemError)

URL = "https://example.ru"
HTML_PAGE = "Never mind"


@pytest.mark.parametrize("status_code",
                         [404, 503])
def test_requests_errors(requests_mock, status_code):
    """Check if raise exception for response with status codes 4** and 5**."""

    requests_mock.get(URL, status_code=status_code)
    with pytest.raises(NetworkError):
        _ = download(URL)


@pytest.mark.parametrize("error, exception",
                         [(Timeout, NetworkError),
                          (ConnectionError, NetworkError),
                          (TooManyRedirects, NetworkError)])
def test_connection_exceptions(requests_mock, error, exception):
    """Check if raises Timeout, Connection and TooManyRedirect exceptions."""

    requests_mock.register_uri("GET", URL, exc=error)
    with pytest.raises(exception):
        _ = download(URL)


@pytest.mark.parametrize("dir_path, exception",
                         [("/", FileSystemError),
                          ("not/existent/dir", FileSystemError)])
def test_file_exceptions(requests_mock, dir_path, exception):
    """Check if raises Permission and FileExists exceptions."""

    requests_mock.register_uri("GET", URL, text=HTML_PAGE)
    with pytest.raises(exception):
        _ = download(URL, dir_path)
