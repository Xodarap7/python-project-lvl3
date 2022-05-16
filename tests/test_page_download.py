from os import listdir
from os.path import exists, join
from tempfile import TemporaryDirectory

from page_loader import download
import requests_mock
import logging

logger = logging.getLogger()


def test_function_download():

    file_indicator = False
    page = 'very_long_and_complicated_site_name'
    correct_file_name = 'www-very-long-and-complicated-site-name-com.html'
    correct_dir_name = 'www-very-long-and-complicated-site-name-com_files'
    address_page = f'https://www.{page}.com'
    address_img1 = f'{address_page}/img/python.jpeg'
    address_img2 = f'{address_page}/img/python_real.svg'
    file_name = f'tests/fixtures/{page}.html'

    with open(file_name, 'r') as test_html:
        text_html = test_html.read()
    with open('tests//fixtures//img//1.jpeg', 'rb') as test_page:
        img1_content = test_page.read()
    with open('tests//fixtures//img//2.jpg', 'rb') as test_page:
        img2_content = test_page.read()

    with TemporaryDirectory() as temp_dir:
        expected_patch = join(temp_dir, correct_file_name)
        with requests_mock.Mocker() as mock:
            mock.get(address_page, text=text_html)
            mock.get(address_img1, content=img1_content)
            mock.get(address_img2, content=img2_content)
            received_patch = download(address_page, temp_dir)
        if exists(received_patch):
            file_indicator = True

        list_file = listdir(join(temp_dir, correct_dir_name))

    current_file_name = received_patch.split('/')[-1]

    assert expected_patch == received_patch
    assert file_indicator
    assert correct_file_name == current_file_name
    assert len(list_file) == 2
