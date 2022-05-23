import logging


def setup_logger():
    """ Logger settings"""
    fmt_line = (
        '%(asctime)s::%(levelname)s::%(module)s::%(funcName)s::%(message)s'
    )
    logging.basicConfig(
        level=logging.ERROR,
        format=fmt_line,
    )
