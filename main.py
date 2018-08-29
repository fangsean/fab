# -*- coding:utf-8 -*-
import sys
import getopt
from fabric.api import *
from fabric.colors import *
from release.comm_model.Component import CRYPT


def release(releases):
    if releases == 'bsweb':
        local('fab -f ./bsweb_model.py go:deploy=pre,model=bsweb')
    else:
        sys.exit('输入有误，工程名称错误...')

    print("starting------------------------------------------")



    # __releases__ = {}
    # print('Release systems: ' + str(systems.keys()))
    # __releases__.system = input("please input release system:")
    # if __releases__.system not in systems.keys():
    #     sys.exit(red('输入有误，系统工程名称错误...'))
    # else:
    #     print(blue("您选的工程名称是[%s]" % (__configer__.get_params('servers', __releases__.system))))
    #
    # print('Release deploys: ' + str(deploys.keys()))
    # __releases__.deploy = input("please input release deploy:")
    # if __releases__.deploy not in deploys.keys():
    #     sys.exit(red('输入有误，系统环境名称错误...'))
    # else:
    #     print(blue("您将发布的系统环境是[%s]" % (__configer__.get_params('deploy', __releases__.deploy))))
    #
    # print('Release branch: ' + str(demo_branch_list()))
    # __releases__.deploy = input("please input release branch:")
    # if __releases__.deploy not in deploys.keys():
    #     sys.exit(red('输入有误，系统环境名称错误...'))
    # else:
    #     print(blue("您将发布的系统环境是[%s]" % (__configer__.get_params('deploy', __releases__.deploy))))
    #
    # release(__releases__)
