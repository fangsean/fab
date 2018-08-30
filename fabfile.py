# -*- coding:utf-8 -*-

import sys

import click
from fabric.api import *
from fabric.colors import *

from release.comm_model.Component import MainComponent, GitComponent, BackUpComponent
from release.setting import Configer

__configer = click.make_pass_decorator(Configer, ensure=True)
# env.user = user
# env.password = password
# env.hosts = hosts1

env.roledefs['git'] = ['localhost']


# def _execute(task):
#     output = StringIO()
#     error = StringIO()
#     sys.stdout = output
#     sys.stderr = error
#     task()
#     sys.stdout = sys.__stdout__
#     sys.stderr = sys.__stderr__
#     return (output.getvalue(), error.getvalue())


@roles('git')
@task()
@parallel
def git(model,branch):
    ''' 执行代码更新任务 '''

    print("***git 执行代码更新任务***")
    if model == '' or branch == '':
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (__configer.get_params("servers"))))
        print(yellow("\t\tbranch:%s" % (__configer.get_params("branch"))))
        print(yellow("\t如 fab git:model=bsweb,branch=developer"))
        print("Break")
        sys.exit(1)

    print("================================ START TASK ==============================")
    component = GitComponent(model, branch)
    execute(component.model_dir_check),
    execute(component.model_mvn_clone),
    execute(component.model_branch_list),
    execute(component.model_merge),
    execute(component.model_pull),
    execute(component.model_end)
    sys.exit(0)


@task()
@parallel
def go(model, deploy):
    ''' 执行发布任务 '''

    print("***go 执行发布任务***")
    if model == '' or deploy == '':
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (__configer.get_params("servers"))))
        print(yellow("\t\tdeploy:%s" % (__configer.get_params("deploy"))))
        print(yellow("\t如 fab go:model=bsweb,deploy=pre"))
        print("Break")
        sys.exit(1)

    print("================================ START TASK ==============================")
    component = MainComponent(model, deploy)
    execute(component.model_dir_check()),
    execute(component.model_mvn_package),
    execute(component.model_jar_push),
    execute(component.model_server_kill),
    execute(component.model_jar_upgraded),
    execute(component.model_server_startup),
    execute(component.model_netstat),
    execute(component.model_end)
    sys.exit(0)


@task()
@parallel
def backup(model, deploy):
    ''' 执行回退任务 '''

    print(yellow("***backup 执行回退任务***"))
    if model == '' or deploy == '':
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (__configer.get_params("servers"))))
        print(yellow("\t\tdeploy:%s" % (__configer.get_params("deploy"))))
        print(yellow("\t如 fab backup:model=bsweb,deploy=pre"))
        print("Break")
        sys.exit(1)

    print("================================ START TASK ==============================")
    component = BackUpComponent(model, deploy)
    execute(component.model_jar_backup_list),
    execute(component.model_input_backup_file),
    execute(component.model_jar_backup, component.file),
    execute(component.model_server_kill),
    execute(component.model_server_startup),
    execute(component.model_netstat),
    execute(component.model_end)
    sys.exit(0)


@task()
@parallel
def test(model, deploy):
    ''' 测试 '''
    print(yellow("***test 测试***"))
    config = comm_config
    component = BackUpComponent(model, deploy)
    # execute(component.model_netstat),
    execute(component.model_end)
    sys.exit(0)


@task()
@parallel
def help(**args):
    ''' 帮助 '''
