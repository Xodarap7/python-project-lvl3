import logging
from os import mkdir
from os.path import exists


def save_file(file_name: str, content: str):
    """
    Safe file saving.

    :param file_name: path and filename
    :param content: file content
    :return: None
    """
    mode = 'w' if isinstance(content, str) else 'wb'
    try:
        with open(file_name, mode) as res_file:
            res_file.write(content)
    except FileNotFoundError as exc:
        logging.exception(f'Failed to save site {file_name}. Error {exc}')
        raise FileNotFoundError(f'Failed to save site {file_name}. Error {exc}')
    except TypeError as exc:
        logging.exception(f'Failed to save file{file_name}. Error {exc}')
    logging.info(f'File {file_name} saved successfully.')


def mk_dir(res_dir: str):
    """
    Safe directory creation.
    :param: res_dir: path and directory name
    :return: None
    """
    if not exists(res_dir):
        try:
            mkdir(res_dir)
        except OSError:
            logging.error('Failed to create resource folder.')
            raise FileNotFoundError('Failed to create resource folder.')
