import functools
import logging
import sys
import time

import click
from fabric.colors import *


def Logger(log_name, name=None):
    LOG_ROOT = os.getcwd() + os.altsep + "logs"
    if os.path.isdir(LOG_ROOT) == False:
        os.mkdir(LOG_ROOT)

    # LOG_FILE是日志文件名
    LOG_FILE = LOG_ROOT + os.altsep + log_name + "." + time.strftime('%Y-%m-%d-%H',
                                                                     time.localtime(
                                                                         time.time()))

    # 生成一个日志对象
    logger = logging.getLogger(name)

    # 按文件大小分隔日志，分隔多少份
    # file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=40 * 1024 * 1024, backupCount=40)
    # 根据时间对日志分隔，S-second（按秒对日志进行分割），M-Minutes（按分钟对日志进行分割），H-Hours（按小时对日志进行分割），D-Days（按天对日志进行分割）
    # file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='M', interval=1, backupCount=40)
    file_handler = logging.FileHandler(LOG_FILE)
    # 生成一个规范日志的输出格式
    formater = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    # 将格式器设置到处理器上
    file_handler.setFormatter(formater)
    stream_handler_err = logging.StreamHandler(sys.stderr)
    stream_handler_stdout = logging.StreamHandler(sys.stdout)
    stream_handler_stdin = logging.StreamHandler(sys.stdin)
    print(sys.exc_info())
    # 将处理器加到日志对象上
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler_err)
    logger.addHandler(stream_handler_stdout)
    logger.addHandler(stream_handler_stdin)
    # 设置日志信息输出的级别
    logger.setLevel(logging.NOTSET)
    return logger


def func_exception_log(name=None):
    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                print('call %s():' % func.__name__)
                return func(*args, **kw)
            except Exception as e:
                click.echo(red(str(e)))
                Logger("error", name).exception(func.__name__ + "(%s,%s)" % (args, kw))
                sys.exit(1)
        return wrapper
    return log
