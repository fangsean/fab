import os, sys
import click
from fabric.api import *
from fabric.colors import *
from release.setting import Configer
from release.comm_model.Component import CRYPT

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
    if model == None or branch == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[branch]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        click.echo(yellow("\t如 git  --model bsweb --branch developer"))
        sys.exit(red("================ Break =================="))

    local('fab git:model=%s,branch=%s' % (model, branch))
    click.echo("================================ END TASK ==============================")


@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=False)
@click.option('--deploy', default=None, help="版本环境", type=str, required=False)
@pass_config
def go(config, model, deploy):
    ''' 执行发布任务 '''

    click.echo(yellow("***go 执行发布任务***"))
    if model == None or deploy == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        click.echo(yellow("\t如 go  --model bsweb --deploy pre "))
        sys.exit(red("================ Break =================="))

    env.hosts = config.get_params("server_hosts", model, deploy)
    local('fab go:model=%s,deploy=%s' % (model, deploy))
    click.echo("================================ END TASK ==============================")


@main.command()
@click.option('--model', default=None, help='项目服务名.', type=str, required=False)
@click.option('--deploy', default=None, help="版本环境", type=str, required=False)
@pass_config
def backup(config, model, deploy):
    ''' 执行回退任务 '''

    click.echo(yellow("***backup 执行回退任务***"))
    if model == None or deploy == None:
        click.echo(red("\t参数缺失！"))
        click.echo(red("\t请输入[model]参数："))
        click.echo(magenta(list(config.get_params("servers").keys())))
        click.echo(red("\t请输入[deploy]参数:"))
        click.echo(magenta(list(config.get_params("deploy").keys())))
        click.echo(yellow("\t如 backup  --mode bsweb --deploy pre "))
        sys.exit(red("================ Break =================="))

    env.hosts = config.get_params("server_hosts", model, deploy)
    local('fab backup:model=%s,deploy=%s' % (model, deploy))
    click.echo("================================ END TASK ==============================")


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

    sys.exit(blue("================ END =================="))


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

    sys.exit(blue("================ END =================="))

# main.add_command(encrypt)
# main.add_command(backup)
# main.add_command(go)
# main.add_command(git)
# @main.command()
# @click.option('--string-to-print', default='world', help='The subject of the greeting.')
# @click.option('--repeat', default=1, type=int, help='How many times you should be greeted.')
# @click.argument('out', type=click.File('w'), default='-', required=False)
# @pass_config
# def other(config, string_to_print, repeat, out):
#     """
#      This script is the Greeter.
#     \b
#     :param out: The file to write the greeting into. Defaults to '-'.
#     """
#     click.echo(config.get_params("server_hosts", 'bsweb', 'prod', 1))
#
#     click.echo_via_pager('\n'.join('Line %d' % idx
#                                    for idx in range(60)))
#     # click.clear()
#
#     click.secho('\nOne fish ', bold=True, nl=False)
#     click.secho('Two fish', underline=True, nl=False)
#     click.secho(' Red fish ', fg='red', nl=False)
#     click.secho('Blue fish\n', fg='blue', nl=False)
#
#     for x in range(repeat):
#         click.echo(f'Hello {string_to_print}!', file=out)
