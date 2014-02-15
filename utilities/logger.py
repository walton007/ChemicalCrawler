import logging
import sys
import os
logger = logging.getLogger("main")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%d %b %Y %H:%M:%S',)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

htmllogger = logging.getLogger("html")



def GetLogger():
    return logger

def GetHtmlLogger():
    return htmllogger

def SetLoggerFileName(fn):
    if not fn.endswith('.log'):
        fn = "./log/%s.log"%fn
    file_handler = logging.FileHandler(fn)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)


    if not fn.endswith('.log'):
        fnhtml = "./log/html_%s.log"%fn
    else:
        fnhtml = fn
    htmlfile_handler = logging.FileHandler(fnhtml)
    htmlfile_handler.setFormatter(formatter)
    htmlfile_handler.setLevel(logging.INFO)
    htmllogger.addHandler(htmlfile_handler)


if __name__ == '__main__':
    logger.error("fuckgfw")
    logger.info('hello')

