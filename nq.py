import sys

import click
from fabric.api import *
from fabric.colors import *

from release.comm_model.component import CRYPT
from release.setting import Configer

pass_config = click.make_pass_decorator(Configer, ensure=True)


@click.group()
def main():
    pass


@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=False)
@click.option('--branch', default=None, help="分支名称", type=str, required=False)
@pass_config
def git(config, model, branch):
    ''' 执行代码更新任务 '''

    click.echo("***git 执行代码更新任务***")
    models = list(config.get_params("servers").keys())
    deploys = list(config.get_params("branch").keys())
    if model == None or branch == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(models))
        click.echo(red("\t请输入[branch]参数:"))
        click.echo(magenta(deploys))
        click.echo(yellow("\t如 git  --model bsweb --branch developer"))
        sys.exit(red("================ Break =================="))
    if model not in models:
        click.echo(red("\t参数错误！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(models))
        sys.exit(red("================ Stop =================="))
    try:
        local('fab git:model=%s,branch=%s' % (model, branch))
    except Exception as e:
        click.echo(red("================================ ERROR TASK ================================"))
    click.echo(green("================================ END TASK ================================"))


@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=False)
@click.option('--deploy', default=None, help="版本环境", type=str, required=False)
@pass_config
def jar(config, model, deploy):
    ''' 打包服务 ##被依赖的不需要发布的服务情况## '''

    click.echo(yellow("***jar 打包服务依赖***"))
    models = list(config.get_params("servers").keys())
    deploys = list(config.get_params("deploy").keys())

    if model == None or deploy == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        click.echo(yellow("\t如 jar  --model bsweb --deploy pre "))
        sys.exit(red("================ Break =================="))

    if model not in models or deploy not in deploys:
        click.echo(red("\t参数错误！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        sys.exit(red("================ Break =================="))

    try:
        env.hosts = config.get_params("server_hosts", model, deploy)
        local('fab jar:model=%s,deploy=%s' % (model, deploy))
    except Exception as e:
        click.echo(red("================================ ERROR TASK ================================"))
    click.echo(green("================================ END TASK ================================"))

@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=False)
@click.option('--deploy', default=None, help="版本环境", type=str, required=False)
@pass_config
def go(config, model, deploy):
    ''' 执行发布任务 '''

    click.echo(yellow("***go 执行发布任务***"))
    models = list(config.get_params("servers").keys())
    deploys = list(config.get_params("deploy").keys())

    if model == None or deploy == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        click.echo(yellow("\t如 go  --model bsweb --deploy pre "))
        sys.exit(red("================ Break =================="))

    if model not in models or deploy not in deploys:
        click.echo(red("\t参数错误！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        sys.exit(red("================ Break =================="))

    try:
        env.hosts = config.get_params("server_hosts", model, deploy)
        local('fab go:model=%s,deploy=%s' % (model, deploy))
    except Exception as e:
        click.echo(red("================================ ERROR TASK ================================"))
    click.echo(green("================================ END TASK ================================"))


@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=False)
@click.option('--deploy', default=None, help="版本环境", type=str, required=False)
@pass_config
def backup(config, model, deploy):
    ''' 执行回退任务 '''

    click.echo(yellow("***backup 执行回退任务***"))
    models = list(config.get_params("servers").keys())
    deploys = list(config.get_params("deploy").keys())

    if model == None or deploy == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        click.echo(yellow("\t如 backup  --model bsweb --deploy pre "))
        sys.exit(red("================ Break =================="))

    if model not in models or deploy not in deploys:
        click.echo(red("\t参数错误！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        sys.exit(red("================ Break =================="))

    try:
        env.hosts = config.get_params("server_hosts", model, deploy)
        local('fab backup:model=%s,deploy=%s' % (model, deploy))
    except Exception as e:
        click.echo(red("================================ ERROR TASK ================================"))

    click.echo(green("================================ END TASK ================================"))


@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=False)
@click.option('--deploy', default=None, help="版本环境", type=str, required=False)
@pass_config
def kill(config, model, deploy):
    ''' 停止服务进程 '''

    click.echo(yellow("***kill 停止服务进程***"))
    models = list(config.get_params("servers").keys())
    deploys = list(config.get_params("deploy").keys())

    if model == None or deploy == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        click.echo(yellow("\t如 kill  --model bsweb --deploy pre "))
        sys.exit(red("================ Break =================="))

    if model not in models or deploy not in deploys:
        click.echo(red("\t参数错误！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        sys.exit(red("================ Break =================="))

    try:
        env.hosts = config.get_params("server_hosts", model, deploy)
        local('fab kill:model=%s,deploy=%s' % (model, deploy))
    except Exception as e:
        click.echo(red("================================ ERROR TASK =============================="))

    click.echo(green("================================ END TASK =============================="))


@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=False)
@click.option('--deploy', default=None, help="版本环境", type=str, required=False)
@pass_config
def restart(config, model, deploy):
    ''' 重启服务进程 '''

    click.echo(yellow("***restart 重启服务进程***"))
    models = list(config.get_params("servers").keys())
    deploys = list(config.get_params("deploy").keys())

    if model == None or deploy == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        click.echo(yellow("\t如 restart --model bsweb --deploy pre "))
        sys.exit(red("================ Break =================="))

    if model not in models or deploy not in deploys:
        click.echo(red("\t参数错误！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        sys.exit(red("================ Break =================="))

    try:
        env.hosts = config.get_params("server_hosts", model, deploy)
        local('fab restart:model=%s,deploy=%s' % (model, deploy))
    except Exception as e:
        click.echo(red("================================ ERROR TASK =============================="))

    click.echo(green("================================ END TASK =============================="))



@main.command()
@click.argument('passwd', default=None, required=True, type=str)
@pass_config
@task
def encrypt(config, passwd):
    ''' 加密字符串密码 '''

    click.echo(yellow("***encrypt 加密字符串密码***"))
    # click.clear()
    key = config.get_params('Apps', 'domain')
    password_crypt = CRYPT.encrypt_password(key, passwd)
    click.echo(yellow("\tinput passwd:%s" % (passwd)))
    click.echo(yellow("\tencrypt passwd:%s" % (password_crypt)))

    sys.exit(green("================ END =================="))


@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=True)
@click.option('--deploy', default=None, help="环境", type=str, required=True)
@pass_config
@task
def test(config, model, deploy):
    ''' 测试 '''

    click.echo(yellow("***test 测试***"))
    # click.clear()
    env.hosts = config.get_params("server_hosts", model, deploy)

    local('fab test:model=%s,deploy=%s' % (model, deploy))

    sys.exit(green("================ END =================="))
