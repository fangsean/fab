# -*- encoding: utf-8 -*-
from release import ROOT_PATH

__author__ = "jsen"
import configparser
from release.util.fileUtil import file_name
import os

class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if Singleton._instance is None:
            Singleton._instance = object.__new__(cls, *args, **kwargs)
        return Singleton._instance


# @Singleton
class Init(Singleton):
    """
        Python变量命名用法（以字符或者下划线开头，可以包括字母、数字、下划线，区别大小写）
        一般变量
        常量
        私有变量
        内置变量
    """

    # config

    def __init__(self):
        self.__final__config = configparser.ConfigParser()
        self.__final__config.read(file_name(ROOT_PATH, '.ini'), encoding='utf-8')
        self.config_params = {}
        sections = self.__final__config.sections()
        self.config_params = {
            section: {
                item[0]: item[1]
                for item in self.__final__config.items(section)
            }
            for section in sections
        }

    # descriptor
    # def __get__(self, obj, objtype):
    #     print('Retrieving', self.name)
    #     return self.val
    #
    # def __set__(self, obj, val):
    #     print('Updating', self.name)
    #     self.val = val

    # def get_configer(self):
    #     return self.__final__config;

    def get_params(self):
        return self.config_params
