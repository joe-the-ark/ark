import logging


logger = logging.getLogger('api')


def log(text, *args):
    log_text = text if not args else text % tuple(args)
    logger.info(log_text)


def error(text, *args):
    log_text = text if not args else text % tuple(args)
    logger.error(log_text)
