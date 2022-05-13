import argparse


def parse_args():
    """
    Create arguments parser

    :return: parser
    """
    parser = argparse.ArgumentParser(description='Page loader.')
    parser.add_argument('page')
    parser.add_argument(
        '-o',
        '--output',
        default='',
        help='Директория для сохранения файлов',
    )

    return parser.parse_args()
