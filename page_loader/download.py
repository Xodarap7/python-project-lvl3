import logging
import sys
from os import getcwd, mkdir
from os.path import abspath, exists, join
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

err_handler = logging.StreamHandler()
err_handler.setLevel(logging.ERROR)
logger.addHandler(err_handler)

stdin_handler = logging.StreamHandler(sys.stdin)
stdin_handler.setLevel(logging.INFO)
logger.addHandler(stdin_handler)


def link_to_filename(page: str) -> str:
    """
    :param page: address page
    :return: filename
    """
    file_name = page.split("//")[-1]
    symbols = set(
        "[qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890]",
    )
    file_name = [char if char in symbols else "-" for char in file_name]
    file_name = "".join(file_name)

    return file_name


def download_and_replace(   # noqa: C901
        attr: tuple,
        path: str,
        text_html: str,
        page: str) -> str:
    """
    Load and save resources in path
    return text_html with changed links
    :param page: page address
    :param attr: tuple
    :param path: directory for save
    :param text_html: html-page
    :return: changed page
    """
    soup = BeautifulSoup(text_html, "html.parser")

    for tag in soup.find_all(attr[0]):
        link = tag.get(attr[1])
        if link is None:
            continue
        if "http" in link:
            continue

        ext = link.split('.')[-1]
        file_name = f'{urlparse(page).netloc}/{link}'

        try:
            rsc = requests.get(f'{urlparse(page).scheme}://{file_name}')
        except requests.RequestException:
            logger.error(f'File {file_name} is not available')
            continue
        if rsc.status_code != requests.codes.ok:
            logger.error(
                f"""Returned error code {rsc.status_code}.
                File {file_name} is not available""",
            )
            continue
        file_name = link_to_filename(
            file_name[0:file_name.rfind(ext)],
        )
        logging.info(f'File {file_name} was received')

        file_name = f'{file_name}.{ext}'
        file_name = join(path, file_name)

        try:
            with open(file_name, 'wb') as img:
                img.write(rsc.content)
        except OSError:
            logging.info(f'Failed to save file {file_name}.')
        else:
            logging.info(f'File {file_name} saved successfully')

        tag[attr[1]] = file_name

    return soup.prettify()


def download(page: str, dir_path: str) -> str:  # noqa: WPS210, C901, WPS213
    """
    Load and save file
    :param page: page address
    :param dir_path: where to save
    :return: full path
    """
    if not dir_path:
        dir_path = getcwd()
    elif not exists(dir_path):
        logger.error(f'The directory {dir_path} does not exist.')
        raise FileNotFoundError(f'The directory {dir_path} does not exist.')
    logging.info('Folder existence check passed.')

    if "http" not in page:
        logger.error('Incomplete site address.')
        raise ValueError('Incomplete site address.')
    logging.info("Page address verification passed")

    try:
        resp = requests.get(page)
    except requests.RequestException:
        raise ConnectionError('Connection error')
    if resp.status_code != requests.codes.ok:
        logger.error('The site is not available.')
        raise ConnectionError('The site is not available.')
    logging.info('Website accessibility check passed.')

    file_name = link_to_filename(page)

    page_name = f'{file_name}.html'
    page_name = join(dir_path, page_name)
    text_html = resp.text
    try:
        with open(page_name, 'w') as html_file:
            html_file.write(text_html)
    except OSError:
        logger.error('Failed to save site.')
        raise OSError('Failed to save site.')
    logging.info('The site page has been saved.')

    src_dir = join(dir_path, f'{file_name}_files')
    if not exists(src_dir):
        try:
            mkdir(src_dir)
        except OSError:
            logger.error('Failed to create resource folder.')
            raise OSError('Failed to create resource folder.')
    attr = [
        ('img', 'src'),
        ('link', 'href'),
        ('script', 'src'),
    ]
    for tag_arg in attr:
        text_html = download_and_replace(tag_arg, src_dir, text_html, page)
        logging.info(f'Saved {tag_arg}.')

    try:
        with open(page_name, 'w') as html_file:  # noqa: WPS440
            html_file.write(text_html)
    except OSError:
        logger.error('Failed to save change to resource links.')
        raise OSError('Failed to save change to resource links.')
    logging.info('Links to page resources have been changed.')

    return abspath(page_name)
