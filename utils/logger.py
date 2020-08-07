import logging
from logging.handlers import RotatingFileHandler


def get_logger(path_logger, filename, level_logger=logging.WARNING):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    f_handler = RotatingFileHandler('{}/{}.log'.format(path_logger, filename), maxBytes=1024, backupCount=1)
    f_handler.setLevel(level_logger)
    f_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(f_handler)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(c_handler)
    return logger


if __name__ == '__main__':

    logger_a = get_logger('file_a')
    logger_b = get_logger('file_b')

    for _ in range(100):
        logger_a.error('This is error of file a')
        logger_a.info('This is info of file a')

        logger_b.warning('This is a warning of file b')
        logger_b.debug('This is a debug of file b')
