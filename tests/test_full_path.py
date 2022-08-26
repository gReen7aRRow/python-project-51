from page_loader.loader import get_full_path

ANSWER = '/var/tmp/ru-hexlet-io-courses.html'

def test_path():
    file_path = get_full_path('https://ru.hexlet.io/courses', '/var/tmp')
    assert file_path == ANSWER
