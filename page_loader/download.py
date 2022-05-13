from os import getcwd
from os.path import abspath, exists, join

import requests


def page_to_filename(page: str) -> str:
    """
    :param page: address page
    :return: filename
    """
    file_name = page.split('//')[-1]
    symbols = set(
        '[qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890]',
    )
    file_name = [char if char in symbols else '-' for char in file_name]
    file_name = ''.join(file_name)

    return f'{file_name}.html'


def download(page: str, dir_patch: str) -> str:
    """
    Load and save file

    :param page: page address
    :param dir_patch: where to save
    :return: full path
    """
    if not dir_patch:
        dir_patch = getcwd()
    elif not exists(dir_patch):
        return 'Path does not exists.'

    if 'http' not in page:
        return 'This path isn\'t full'

    resp = requests.get(page)
    if resp.status_code != requests.codes.ok:
        return 'Page is not available.'

    file_name = page_to_filename(page)
    file_name = join(dir_patch, file_name)
    with open(file_name, 'w') as html_file:
        html_file.write(resp.text)

    return abspath(file_name)
