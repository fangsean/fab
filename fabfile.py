# -*- coding:utf-8 -*-
import sys

from fabric.api import *
from fabric.colors import *

import click


@click.command()
@click.option('--model', help='项目服务名.', type=str)
@click.option('--branch', help='分支.', type=str)
@task(name="git")
@parallel
def git(**kwargs):
    ''' 执行代码更新任务 '''

    print("***git 执行代码更新任务***")
    if len(kwargs) < 2 or 'model' not in kwargs.keys() or 'branch' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t如 fab git:model=bsweb,branch=developer"))
        print("Do")
        sys.exit(0)

    model = kwargs['model']
    branch = kwargs['branch']
    print("================================ START TASK ==============================")


@task(name="go")
@parallel
def go(**kwargs):
    ''' 执行发布任务 '''

    print("***go 执行发布任务***")
    if len(kwargs) < 2 or 'model' not in kwargs.keys() or 'deploy' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t如 fab go:model=bsweb,deploy=pre"))
        print("Do")
        sys.exit(0)

    model = kwargs['model']
    deploy = kwargs['deploy']
    print("================================ START TASK ==============================")


@roles('main')
@task(name="back")
@parallel
def backup(**kwargs):
    ''' 执行回退任务 '''

    print(yellow("***backup 执行回退任务***"))
    if len(kwargs) < 1 or 'model' not in kwargs.keys():
        print(red("\t参数缺失！"))
        print(yellow("\t请输入执行参数:"))

    model = kwargs['model']
    print("================================ START TASK ==============================")

@click.command()
@click.option('--name', prompt='%s \r\nname of model：' % (__configer__.get_params("servers")),
              help='name of model.', type=str)
@task(name="encrypt")
@parallel
def encrypt(**kwargs):
    ''' 加密字符串密码 '''

    print(yellow("***encrypt 加密字符串密码***"))
    if len(kwargs) < 1 or 'passwd' not in kwargs.keys():
        print(yellow("\t请输入执行参数:"))
        print(yellow("\t如 fab encrypt:passwd=***"))
        print("Do")
        sys.exit(0)

    passwd = kwargs['passwd']

    sys.exit(blue("================ END =================="))


@click.command()
@click.option('--name', prompt='%s \r\nname of model：' % (__configer__.get_params("servers")),
              help='name of model.')
@task()
@parallel
def help(name):
    ''' 帮助 '''
    click.echo('[%s, %s, %s, %s ]' % ('git', 'go', 'backup', 'encrypt'))
    click.echo('Hello %s!!!' % name)


@click.group()
def cli():
    pass


cli.add_command(help)
cli.add_command(encrypt)
cli.add_command(backup)
cli.add_command(go)
cli.add_command(git)

if __name__ == '__main__':
    help()
