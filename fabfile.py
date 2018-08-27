# -*- coding:utf-8 -*-
import sys

from fabric.api import *
from fabric.colors import *

from release.comm_model.Component import Component, MainComponent, GitComponent,BackUpComponent

env.roledefs['main'] = ['Nq007', 'localhost']
env.roledefs['git'] = ['localhost']


@roles('git')
@task()
@parallel
def git(**kwargs):
    print("***git 执行代码更新任务***")
    if len(kwargs) < 2 or 'model' not in kwargs.keys() or 'branch' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (Component.configer.get_params("servers"))))
        print(yellow("\t\tbranch:%s" % (Component.configer.get_params("branch"))))
        print(yellow("\t如 fab git:model=bsweb,branch=developer"))
        print("Do")
        sys.exit(0)

    model = kwargs['model']
    branch = kwargs['branch']
    print("================================ START TASK ==============================")
    component = GitComponent(model, branch)
    execute(component.model_mvn_clone),
    execute(component.model_branch_list),
    execute(component.model_merge),
    execute(component.model_pull),
    execute(component.model_end)


@roles('main')
@task()
@parallel
def go(**kwargs):
    print("***go 执行发布任务***")
    if len(kwargs) < 2 or 'model' not in kwargs.keys() or 'deploy' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (Component.configer.get_params("servers"))))
        print(yellow("\t\tdeploy:%s" % (Component.configer.get_params("deploy"))))
        print(yellow("\t如 fab go:model=bsweb,deploy=pre"))
        print("Do")
        sys.exit(0)

    model = kwargs['model']
    deploy = kwargs['deploy']
    print("================================ START TASK ==============================")
    component = MainComponent(model, deploy)
    execute(component.model_mvn_package),
    execute(component.model_jar_push),
    execute(component.model_server_kill),
    execute(component.model_jar_upgraded),
    execute(component.model_server_startup),
    execute(component.model_netstat),
    execute(component.model_end)


@roles('main')
@task()
@parallel
def backup(**kwargs):
    print(yellow("***backup 执行回退任务***"))
    if len(kwargs) < 1 or 'model' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (Component.configer.get_params("servers"))))
        print(yellow("\t如 fab backup:model=bsweb"))
        print("Do")
        sys.exit(0)

    model = kwargs['model']
    print("================================ START TASK ==============================")
    component = BackUpComponent(model)
    execute(component.model_jar_backup_list),

    print(white('Release file: '))
    file = input("please input file from head list:")
    if file ==None or file == '' or model not in file:
        exit(red('输入有误，文件名称不规范,重新输入...'))
    else:
        print(blue("您输入的文件名称是[%s]" % (file)))

    execute(component.model_jar_backup, file),
    execute(component.model_server_kill),
    execute(component.model_server_startup),
    execute(component.model_netstat),
    execute(component.model_end)
