import os
from datetime import datetime
import logging

def info2file(task, info):

    date = str(datetime.today())[:10]
    today_file = os.path.join('logs', task, date+'.log')
    # create logger obj
    logger = logging.getLogger()

    # set log level
    logger.setLevel(logging.DEBUG)

    # file handler
    handler = logging.FileHandler(today_file, mode='a', encoding='utf-8')
    handler.setFormatter(logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s"))

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s"))

    logger.addHandler(handler)
    logger.addHandler(ch)

    logger.info(info)
    logger.removeHandler(handler)
    logger.removeHandler(ch)