import logging
from sys import exit

from page_loader import download
from page_loader.cli import parse_args
from page_loader.logger import setup_logger


def main():
    setup_logger()
    args = parse_args()
    try:
        path = download(args.page, args.output)
    except Exception as exc:
        logging.exception(f'Error! {exc}')
        print(f'Error! {exc}')
        exit(1)
    else:
        print(path)
        logging.info(f'Result: {path}')
        exit(0)


if __name__ == '__main__':
    main()
