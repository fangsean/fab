import functools
import sys

import click
from fabric.colors import *

from release.util.mylog import Logger


def func_exception_log(name=None):
    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                print(blue('............................................call %s():' % func.__name__))
                return func(*args, **kw)
            except Exception as e:
                click.echo(red(str(e)))
                Logger("error", name).exception(func.__name__ + "(%s,%s)" % (args, kw))
                sys.exit(1)
        return wrapper
    return log