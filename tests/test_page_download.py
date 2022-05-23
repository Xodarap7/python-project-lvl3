import os
from os.path import exists, join
from tempfile import TemporaryDirectory

import requests_mock

from page_loader import download


def test_function_download():

    file_indicator = False
    correct_file_name = "www-very-long-and-complicated-site-name-com.html"
    correct_dir_name = "www-very-long-and-complicated-site-name-com_files"
    address_page = "https://www.very_long_and_complicated_site_name.com"
    address_img1 = f"{address_page}/img/1.jpeg"
    address_img2 = f"{address_page}/img/2.jpg"
    address_style = f"{address_page}/style.css"
    file_name = "tests/fixtures/very_long_and_complicated_site_name.html"

    with open(file_name, "r") as test_html:
        text_html = test_html.read()
    with open("tests//fixtures//img//1.jpeg", "rb") as test_page:
        img1_content = test_page.read()
    with open("tests//fixtures//img//2.jpg", "rb") as test_page:
        img2_content = test_page.read()
    with open("tests//fixtures//style.css", "r") as test_page:
        css_content = test_page.read()

    with TemporaryDirectory() as temp_dir:
        expected_patch = join(temp_dir, correct_file_name)
        with requests_mock.Mocker() as mock:
            mock.get(address_page, text=text_html)
            mock.get(address_img1, content=img1_content)
            mock.get(address_img2, content=img2_content)
            mock.get(address_style, text=css_content)
            received_patch = download(address_page, temp_dir)
        if exists(received_patch):
            file_indicator = True

        list_file = os.listdir(join(temp_dir, correct_dir_name))

    current_file_name = received_patch.split("/")[-1]

    assert expected_patch == received_patch
    assert file_indicator
    assert correct_file_name == current_file_name
    assert len(list_file) == 3
