# -*- coding:utf-8 -*-
from fabric.contrib.console import confirm
from fabric.api import *
from fabric.colors import *

import sys
import click

from fabric.api import *
from fabric.colors import *
from release.comm_model.Component import CRYPT
from release.comm_model.Component import Component, MainComponent, GitComponent, BackUpComponent

from release.setting import Configer

comm_config = click.make_pass_decorator(Configer, ensure=True)
# env.user = user
# env.password = password
# env.hosts = hosts1

env.roledefs['main'] = ['Nq007', 'localhost']
env.roledefs['git'] = ['localhost']


@roles('git')
@task()
@parallel
@comm_config
def git(config, **kwargs):
    ''' 执行代码更新任务 '''

    print("***git 执行代码更新任务***")
    if len(kwargs) < 2 or 'model' not in kwargs.keys() or 'branch' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (config.get_params("servers"))))
        print(yellow("\t\tbranch:%s" % (config.get_params("branch"))))
        print(yellow("\t如 fab git:model=bsweb,branch=developer"))
        print("Break")
        sys.exit(0)

    model = kwargs['model']
    branch = kwargs['branch']
    print("================================ START TASK ==============================")
    component = GitComponent(config, model, branch)
    execute(component.model_mvn_clone),
    execute(component.model_branch_list),
    execute(component.model_merge),
    execute(component.model_pull),
    execute(component.model_end)


@roles('main')
@task()
@parallel
@comm_config
def go(config, **kwargs):
    ''' 执行发布任务 '''

    print("***go 执行发布任务***")
    if len(kwargs) < 2 or 'model' not in kwargs.keys() or 'deploy' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (config.get_params("servers"))))
        print(yellow("\t\tdeploy:%s" % (config.get_params("deploy"))))
        print(yellow("\t如 fab go:model=bsweb,deploy=pre"))
        print("Break")
        sys.exit(0)

    model = kwargs['model']
    deploy = kwargs['deploy']
    print("================================ START TASK ==============================")
    component = MainComponent(config, model, deploy)
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
@comm_config
def backup(config, **kwargs):
    ''' 执行回退任务 '''

    print(yellow("***backup 执行回退任务***"))
    if len(kwargs) < 1 or 'model' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t\tmodel:%s" % (config.get_params("servers"))))
        print(yellow("\t\tdeploy:%s" % (config.get_params("deploy"))))
        print(yellow("\t如 fab backup:model=bsweb,deploy=pre"))
        print("Break")
        sys.exit(0)

    model = kwargs['model']
    deploy = kwargs['deploy']
    print("================================ START TASK ==============================")
    component = BackUpComponent(config, model, deploy)
    execute(component.model_jar_backup_list),
    execute(component.model_input_backup_file),
    execute(component.model_jar_backup, component.file),
    execute(component.model_server_kill),
    execute(component.model_server_startup),
    execute(component.model_netstat),
    execute(component.model_end)
    # exit(blue("回退成功"))


@task()
@parallel
@comm_config
def test(config, model, deploy):
    ''' 测试 '''

    print(yellow("***test 测试***"))

    component = BackUpComponent(config, model, deploy)
    execute(component.model_netstat),
    execute(component.model_end)

    sys.exit(blue("================ END =================="))


@task()
@parallel
def help(**args):
    ''' 帮助 '''
