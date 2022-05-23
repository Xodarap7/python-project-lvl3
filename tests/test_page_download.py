from os import listdir
from os.path import exists, join
from tempfile import TemporaryDirectory

import pytest
import requests_mock

from page_loader import download
from page_loader.html import url_to_filename

correct_file_name = 'www-site-name-com.html'
correct_dir_name = 'www-site-name-com_files'
address_page = 'https://www.site_name.com'
address_img1 = f'{address_page}/img/python.jpeg'
address_img2 = f'{address_page}/img/python_real.svg'
address_style = f'{address_page}/files/css/style.css'
address_js = f'{address_page}/empty.js'
file_name = 'tests/fixtures/very_long_and_complicated_site_name.html'

head_txt = {'Content-Type': 'text/html'}
head_all = {'Content-Type': 'all'}


def get_mock(temp_dir,
             text_html,
             img1_content,
             img2_content,
             css_content,
             js_content) -> str:
    with requests_mock.Mocker() as mock:
        mock.get(address_page, text=text_html, headers=head_txt)
        mock.get(address_img1, content=img1_content, headers=head_all)
        mock.get(address_img2, content=img2_content, headers=head_all)
        mock.get(address_style, content=css_content, headers=head_all)
        mock.get(address_js, content=js_content, headers=head_all)

        return download(address_page, temp_dir)


def test_page_loader_download(
        text_html,
        img1_content,
        img2_content,
        css_content,
        js_content):

    indicator = False

    with TemporaryDirectory() as temp_dir:
        expected_path = join(temp_dir, correct_file_name)
        received_patch = get_mock(temp_dir,
                                  text_html,
                                  img1_content,
                                  img2_content,
                                  css_content,
                                  js_content)
        if exists(received_patch) and exists(join(temp_dir, correct_dir_name)):
            indicator = True

    current_file_name = received_patch.split('/')[-1]

    assert expected_path == received_patch
    assert indicator
    assert correct_file_name == current_file_name


def test_page_loader_files(
        text_html,
        img1_content,
        img2_content,
        css_content,
        js_content):
    with open('tests/fixtures/expected.html', 'r') as exp_file:
        expected = exp_file.read()

    with TemporaryDirectory() as temp_dir:
        received_patch = get_mock(temp_dir,
                                  text_html,
                                  img1_content,
                                  img2_content,
                                  css_content,
                                  js_content)
        with open(received_patch, 'r') as file_html:
            received = file_html.read()

        path = join(temp_dir, correct_dir_name)
        list_file = listdir(path)
        list_content = {img1_content, img2_content, css_content, js_content}
        exp_list_content = set()
        for item in list_file:
            with open(join(path, item), 'rb') as f:
                exp_list_content.add(f.read())

    assert len(list_file) == 4
    assert expected == received
    assert exp_list_content == list_content
