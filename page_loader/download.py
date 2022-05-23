import logging
from os import getcwd
from os.path import abspath, join
from urllib.parse import urlparse

import requests
from progress.bar import Bar

from page_loader.fs import mk_dir, save_file
from page_loader.html import url_to_filename, prepare_page


def get(url):
    """
    Load file

    :param url: file link
    :return: file content
    """
    if not urlparse(url).netloc:
        raise ValueError('Incomplete address.')

    try:
        resp = requests.get(url)
    except requests.RequestException as exc:
        logging.error(f'Connection error {exc}')
        raise ConnectionError(f'Connection error {exc}')
    if resp.status_code != requests.codes.ok:
        logging.error(f'Link is not available. {resp.status_code}')
        raise ConnectionError(f'Link is not available. {resp.status_code}')
    logging.info(f'File {url} received')
    conn_type = resp.headers.get('Content-Type')
    if conn_type and 'text/html' in conn_type:
        resp.encoding = 'utf-8'
        return resp.text
    else:
        return resp.content


def download(url, directory):  # noqa: WPS210, C901, WPS213
    """
    Load and save file

    :param url: Page address
    :param directory: Directory for save
    :return: Full path for saved page
    """
    if not directory:
        directory = getcwd()

    page_name = url_to_filename(url)
    page_name = join(directory, page_name)
    res_dir = f'{page_name[:-5]}_files'

    text_html = get(url)

    urls, text_html = prepare_page(url, text_html, res_dir)

    save_file(page_name, text_html)

    mk_dir(res_dir)
    progress_bar = Bar('Saving: ', max=len(urls))
    for url in urls:
        try:
            res = get(url['link'])
            save_file(join(directory, url['path']), res)
        except ConnectionError as exc:
            logging.debug(f'Resource {url} is not loaded {exc}')
            continue
        except OSError:
            logging.info(f'Resource {url} is not saved')
            progress_bar.next()
            continue
        logging.info(f'Resource {url} saved successfully')

        progress_bar.next()

    progress_bar.finish()

    return abspath(page_name)
