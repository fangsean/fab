# -*- coding:utf-8 -*-

import sys

import click
from fabric.api import *
from fabric.colors import *

from release.comm_model.component import MainComponent, GitComponent, BackUpComponent,func_exception_log
from release.setting import Configer

__configer = click.make_pass_decorator(Configer, ensure=True)

env.roledefs['git'] = ['localhost']


@roles('git')
@task()
@parallel
@func_exception_log("git")
def git(model, branch):
    ''' 执行代码更新任务 '''

    click.echo("***git 执行代码更新任务***")
    click.echo(blue("================================ START GIT TASK =============================="))
    component = GitComponent(model, branch)
    execute(component.model_dir_check),
    execute(component.model_mvn_clone),
    execute(component.model_branch_list),
    # execute(component.model_merge),
    # execute(component.model_pull),
    execute(component.model_end)
    sys.exit(0)


@task()
@parallel
@func_exception_log("go")
def go(model, deploy):
    ''' 执行发布任务 '''

    click.echo("***go 执行发布任务***")
    click.echo(blue("================================ START GO TASK =============================="))
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
@func_exception_log("backup")
def backup(model, deploy):
    ''' 执行回退任务 '''

    click.echo(yellow("***backup 执行回退任务***"))
    click.echo(blue("================================ START BACKUP TASK =============================="))
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
@func_exception_log("testt")
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
