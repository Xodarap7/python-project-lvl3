import logging
from os import getcwd, mkdir
from os.path import abspath, exists, join
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


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


def download_and_replace(attr: tuple, path: str, text_html: str, page: str) -> str:
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

        ext = link.split(".")[-1]
        file_name = f"{urlparse(page).netloc}/{link}"

        src = requests.get(f"{urlparse(page).scheme}://{file_name}")
        file_name = link_to_filename(
            file_name[0 : file_name.rfind(ext)],
        )
        logging.info("Download completed")

        file_name = f"{file_name}.{ext}"
        file_name = join(path, file_name)

        with open(file_name, "wb") as img:
            img.write(src.content)
        logging.info("Saving to file completed")

        tag[attr[1]] = file_name

    return soup.prettify()


def download(page: str, dir_path: str) -> str:
    """
    Load and save file
    :param page: page address
    :param dir_path: where to save
    :return: full path
    """
    if not dir_path:
        dir_path = getcwd()
    elif not exists(dir_path):
        return "Path is not exist"
    logging.info("Checking if a directory exists")

    if "http" not in page:
        return "incomplete address"
    logging.info("Page address verification passed")

    resp = requests.get(page)
    if resp.status_code != requests.codes.ok:
        return "The site is not available."
    logging.info("Page accessibility check passed")

    file_name = link_to_filename(page)

    page_name = f"{file_name}.html"
    page_name = join(dir_path, page_name)
    text_html = resp.text
    with open(page_name, "w") as html_file:
        html_file.write(text_html)
    logging.info("Page was saved")

    src_dir = join(dir_path, f"{file_name}_files")
    if not exists(src_dir):
        mkdir(src_dir)
    attr = [
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
    ]
    for tag_arg in attr:
        text_html = download_and_replace(tag_arg, src_dir, text_html, page)
        logging.info(f"Saved {tag_arg}.")

    with open(page_name, "w") as html_file:
        html_file.write(text_html)
    logging.info("Page was changed.")

    return abspath(page_name)
