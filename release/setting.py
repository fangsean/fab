# -*- encoding: utf-8 -*-
import json
import logging
import logging.handlers
import os
import sys

from fabric.api import *

from release import ROOT_PATH
from release.init import Init
from release.util.fileUtil import file_name


class Logger(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        log_root = os.path.join(ROOT_PATH, "..", "logs")
        run("mkdir -p %s" % (log_root))
        log_name = ''.join(env.host_string.split('.')) + '.log'
        self.log_file = os.path.join(log_root, log_name)

    def get_logger(self):
        logger = logging.getLogger("fabric")
        formater = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        file_handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes=10240000, backupCount=5)
        file_handler.setFormatter(formater)
        stream_handler_err = logging.StreamHandler(sys.stderr)
        stream_handler_stdout = logging.StreamHandler(sys.stdout)
        stream_handler_stdin = logging.StreamHandler(sys.stdin)
        sys.exc_info()
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler_err)
        logger.addHandler(stream_handler_stdout)
        logger.addHandler(stream_handler_stdin)
        logger.setLevel(logging.DEBUG)
        return logger


class Configer(object):
    instance = None
    # __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        # if self.__first_init:
        self.__init__ = Init()
        self.__config_params__ = self.__init__.get_params()
        files = file_name(ROOT_PATH, '.json')
        for file in files:
            if os.path.getsize(file) > 0:
                name = os.path.basename(file)
                index = name.rfind('.')
                name = name[:index]
                with open(file, 'rb') as f:
                    self.__config_params__[name] = json.loads(f.read())

        self.__config_params__["server_hosts"] = {
            server: {
                _deploy: self.__host_ref__(self.__config_params__["hosts"], _hosts)
                for _deploy, _hosts in deploy.items()
            }
            for server, deploy in self.__config_params__["server_hosts"].items()
        }
        # self.__first_init = False

    def get_params(self, key, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return self.__config_params__[key]
        else:
            temp = self.__config_params__[key]
            for arg in args:
                temp = temp[arg]
            return temp

    def __split_list__(self, str):
        return str.split(',')

    def __host_ref__(self, dict, lists):
        params = []
        try:
            for list in lists:
                params.append(dict[list])
        except Exception as e:
            pass
        return params


if __name__ == "__main__":
    configer = Configer()
    params = configer.get_params("server_hosts", 'bsweb', 'prod')
    print(params)
