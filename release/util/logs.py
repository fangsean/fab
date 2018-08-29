from fabric.api import *
from fabric.colors import green, red, blue, cyan, yellow
import os, sys
import socket
import datetime
import logging
import logging.handlers


def initLoggerWithRotate():
    logname = ''.join(env.host_string.split('.')) + '.log'
    logFileName = "logs/%s" % logname
    logger = logging.getLogger("fabric")
    formater = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logFileName, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(formater)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    return logger
