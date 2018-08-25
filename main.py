# -*- coding:utf-8 -*-
# !/usr/bin/env python3

from fabric.api import *


def release(releases):
    if releases == 'bsweb':
        local('fab -f ./bsweb_model.py go:deploy=pre,model=bsweb')
    else:
        exit('输入有误，工程名称错误...')


if __name__ == "__main__":
        ob = ['bsweb','tradeweb', 'scmweb']
        print('Release demo: ' + str(ob))
        releases = input("please input release system:")
        release(releases)