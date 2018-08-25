# -*- coding:utf-8 -*-
# !/usr/bin/env python3

from fabric.api import *


def release(releases):
    if releases == 'bsweb':
        local('fab -f ./bsweb_model.py go')
    elif releases == 'demo1':
        local('fab -f ./demo1.py go')
    elif releases == 'demo2':
        local('fab -f ./demo2.py go')
    elif releases == 'demo3':
        local('fab -f ./demo3.py go')
    elif releases == 'demo4':
        local('fab -f ./demo4.py go')
    else:
        exit('输入有误，工程名称错误...')


if __name__ == "__main__":
        ob = ['bsweb','demo1, demo2, demo3, demo4']
        print('Release demo: ' + str(ob))
        releases = input("please input release system:")
        release(releases)