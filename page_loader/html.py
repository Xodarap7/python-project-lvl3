import logging
import string
from os.path import basename
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def url_to_filename(link: str) -> str:
    """
    :param link: address page
    :return: filename
    """
    netloc = urlparse(link).netloc
    path = urlparse(link).path
    if path:
        path = path if path[0] == '/' else f'/{path}'
    file_name = path.split('/')[-1]
    if path and '.' in file_name:
        ext = file_name.split('.')[-1]
        file_name = f'{path[:-(len(ext) + 1)]}'
    else:
        file_name = path
        ext = 'html'
    file_name = f'{netloc}{file_name}' if netloc else f'{file_name[1:]}'
    alpha_num = string.ascii_letters + string.digits
    file_name = [char if char in alpha_num else '-' for char in file_name]
    file_name = ''.join(file_name)
    return f'{file_name}.{ext}'


def prepare_page(base_url: str,
                 text_html: str,
                 dir_path: str):
    """
    Finding resources in text_html and changing the link to them.
    :param dir_path: directory for resources
    :param base_url: page address
    :param text_html: html
    :return: changed html
    """
    tags = [
        {'tag': 'img', 'attr': 'src'},
        {'tag': 'link', 'attr': 'href'},
        {'tag': 'script', 'attr': 'src'},
    ]
    page = urlparse(base_url)
    soup = BeautifulSoup(text_html, 'html.parser')

    list_res = []
    for tag in tags:
        for element in soup.find_all(tag['tag']):
            logging.debug(f':Checked {element}')
            url = element.attrs.get(tag['attr'])

            if url is None:
                continue
            url = urlparse(url)
            if url.netloc != page.netloc and url.netloc != '':
                logging.debug('Link to another domain.')
                continue

            url = f'{page.scheme}://{page.netloc}{url.path}'
            file_name = url_to_filename(url)

            element[tag['attr']] = f'{basename(dir_path)}/{file_name}'

            list_res.append(
                {
                    'link': url,
                    'path': element[tag['attr']],
                },
            )
    return list_res, soup.prettify()
