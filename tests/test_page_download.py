from os.path import exists, join
from tempfile import TemporaryDirectory

from page_loader import download
import requests_mock
import logging

logger = logging.getLogger()


def test_function_download():  # noqa: WPS210

    file_indicator = False
    page = 'very_long_and_complicated_site_name'
    correct_name = 'www-very-long-and-complicated-site-name-com.html'
    address_page = f'https://www.{page}.com'
    file_name = f'tests/fixtures/{page}.html'

    with open(file_name, 'r') as test_html:
        text_html = test_html.read()

    with TemporaryDirectory() as temp_dir:
        expected_patch = join(temp_dir, correct_name)
        with requests_mock.Mocker() as mock:
            mock.get(address_page, text=text_html)
            received_patch = download(address_page, temp_dir)
        if exists(received_patch):
            file_indicator = True

    current_name = received_patch.split('/')[-1]

    assert expected_patch == received_patch
    assert file_indicator
    assert correct_name == current_name
