# -*- coding:utf-8 -*-
# !/usr/bin/env python3

from fabric.api import *
from release.setting import Configer

__configer__ = Configer()
systems = __configer__.get_params('servers')
deploys = __configer__.get_params('deploy')
env.user = user
env.password = password


def release(releases):
    if releases == 'bsweb':
        local('fab -f ./bsweb_model.py go:deploy=pre,model=bsweb')
    else:
        exit('输入有误，工程名称错误...')


if __name__ == "__main__":
    argv = sys.argv[1:]
    command = None
    param = None
    output_dir = None
    xml_path = None
    label = "data"
    dict_only = False
    dbname = "robotx"
    delete_db = False
    help_ = False
    for arg in argv:
        if command is None:
            command = arg
        else:
            if command == "--help" or command == "--h":
                help_ = True
            elif command == "--config_path":
                xml_path = arg
            elif command == "--dict_only":
                if arg == "Y" or arg == "y":
                    dict_only = True
                else:
                    dict_only = False
            elif command == "--dbname":
                dbname = arg
            elif command == "--delete_db":
                if arg == "Y" or arg == "y":
                    delete_db = True
                else:
                    delete_db = False
            command = None
    if help_:
        print("--g  --git 提供git操作  --branch 分支名称 --clone y|n 是否重新克隆（默认n）")
        print("--f  --fab 提供发布项目操作")
        print("--p  --pro 需要操作的工程 " + str(systems.keys()))
        print("--d  --deploy 需要操作的版本环境 " + str(deploys.keys()))
        print("--h  --help 提供帮助")
        sys.exit(0)


    print("starting------------------------------------------")

    # releases = {}
    # print('Release systems: ' + str(systems.keys()))
    # releases.system = input("please input release system:")
    # if releases.system not in systems.keys():
    #     exit(red('输入有误，系统工程名称错误...'))
    # else:
    #     print(blue("您选的工程名称是[%s]" % (__configer__.get_params('servers', releases.system))))
    #
    # print('Release deploys: ' + str(deploys.keys()))
    # releases.deploy = input("please input release deploy:")
    # if releases.deploy not in deploys.keys():
    #     exit(red('输入有误，系统环境名称错误...'))
    # else:
    #     print(blue("您将发布的系统环境是[%s]" % (__configer__.get_params('deploy', releases.deploy))))
    #
    # print('Release branch: ' + str(demo_branch_list()))
    # releases.deploy = input("please input release branch:")
    # if releases.deploy not in deploys.keys():
    #     exit(red('输入有误，系统环境名称错误...'))
    # else:
    #     print(blue("您将发布的系统环境是[%s]" % (__configer__.get_params('deploy', releases.deploy))))
    #
    # release(releases)
