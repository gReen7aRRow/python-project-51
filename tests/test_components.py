import pytest
from logging import DEBUG, WARNING

from page_loader.urls import to_dirname, to_filename
from page_loader.logger_agent import get_logger


INPUT = (
    "https://ru.hexlet.io/",
    "https://ru.hexlet.io/courses/intro_to_git/",
    "https://ru.hexlet.io/my/ratings/month?q%5Bcity_id_eq%5D=1/",
    "https://ru.hexlet.io",
    "https://ru.hexlet.io/courses/intro_to_git",
    "https://ru.hexlet.io/my/ratings/month?q%5Bcity_id_eq%5D=1",
)

EXPECTED_PAGE_NAMES = (
    "ru-hexlet-io.html",
    "ru-hexlet-io-courses-intro_to_git.html",
    "ru-hexlet-io-my-ratings-month-q-5Bcity_id_eq-5D-1.html",
)

EXPECTED_DIR_NAMES = (
    "ru-hexlet-io_files",
    "ru-hexlet-io-courses-intro_to_git_files",
    "ru-hexlet-io-my-ratings-month-q-5Bcity_id_eq-5D-1_files",
)


@pytest.mark.parametrize("url, result", [
    (INPUT[0], EXPECTED_PAGE_NAMES[0]),
    (INPUT[1], EXPECTED_PAGE_NAMES[1]),
    (INPUT[2], EXPECTED_PAGE_NAMES[2]),
    (INPUT[3], EXPECTED_PAGE_NAMES[0]),
    (INPUT[4], EXPECTED_PAGE_NAMES[1]),
    (INPUT[5], EXPECTED_PAGE_NAMES[2]),
])
def test_page_name(url, result):
    assert to_filename(url) == result


@pytest.mark.parametrize("url, result", [
    (INPUT[0], EXPECTED_DIR_NAMES[0]),
    (INPUT[1], EXPECTED_DIR_NAMES[1]),
    (INPUT[2], EXPECTED_DIR_NAMES[2]),
])
def test_dir_name(url, result):
    assert to_dirname(url) == result


@pytest.mark.parametrize("debug_mode, right_log_level",
                         [(True, DEBUG),
                          (False, WARNING)])
def test_debug_activate(debug_mode, right_log_level):
    assert get_logger(debug_mode).level == right_log_level
