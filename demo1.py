# -*- coding:utf-8 -*-
from fabric.contrib.console import confirm
from fabric.api import *
from fabric.colors import *
from setting import user, password, hosts1, gitpath, git1, branch, buildpath1, appliation1, local_path1

env.user = user
env.password = password
env.hosts = hosts1

@runs_once
def demo_mvn_clone():
    with lcd(gitpath):
        local('rm -rf demo')
        local('git clone -b %s %s' % (branch, git1))


@runs_once
def demo_mvn_package(deploy='prod'):
    print("[INFO]  ............................................ 打包 > demo_mvn_package")
    with lcd(gitpath):
        local('mvn clean compile package install -Dmaven.test.skip=true -U -P %s' % (deploy))
    print("[INFO]  ............................................ 打包成功 > demo_mvn_package")


@runs_once
def demo_pull():
    print("[INFO]  ............................................ 更新 > demo_pull")
    with lcd(buildpath1):
        local('git checkout developer')
        local('git pull')
    print("[INFO]  ............................................ 更新成功 > demo_pull")


@runs_once
def demo_merge():
    print("[INFO]  ............................................ 合并 > demo_merge")
    with lcd(buildpath1):
        local('git fetch')
        local('git merge origin/developer')
    print("[INFO]  ............................................ 合并成功 > demo_merge")


@runs_once
def demo_put_before():
    print("[INFO]  ............................................ 发布之前 备份 > demo_put_before")
    with cd(appliation1):
        with settings(warn_only=True):
            run('mv demo.war ../backup/demo.war_$(date '
                '+%Y-%m-%d)_bak')
            run('rm -rf *')
    print("[INFO]  ............................................ 备份成功 > demo_put_before")


@runs_once
def demo_put():
    print("[INFO]  ............................................ 远程发包 > demo_put")
    with lcd(local_path1):
        result = put('bsweb.jar', appliation1 + 'bsweb.jar')
        if result.failed and not confirm("put file faild, Continue[Y/N]?"):
            abort("Aborting file put task!")
            print("[INFO]  ............................................ 远程发包失败 > demo_put")
        else:
            print("[INFO]  ............................................ 远程发包成功 > demo_put")


@runs_once
def demo_jar():
    with cd(appliation1):
        run('jar -xvf *.war')
    open_shell('sh /opt/admin/script/tomcat.sh restart  &&  exit')


@runs_once
def demo_check():
    with lcd(local_path1):
        with settings(warn_only=True):
            lmd5 = local("md5sum demo.war", capture=True).split(' ')[0]
            rmd5 = run("md5sum /opt/admin/application/demo.war").split(' ')[0]
        if lmd5 == rmd5:
            print(yellow('OK'))
        else:
            print(blue('ERROR'))


@runs_once
def demo_netstat():
    open_shell("ps aux | grep java | grep -v grep  &&  exit")
    local('sleep 5')
    open_shell("netstat -an | grep 8080  &&  exit")
    print(blue('demo 系统已经发布成功...'))


@runs_once
def demo():
    open_shell("ps aux | grep java | grep -v grep  &&  exit")
    local('sleep 5')
    open_shell("netstat -an | grep 8080  &&  exit")
    print(blue('demo 系统已经发布成功...'))


@task()
@parallel
def go():
    # execute(demo_mvn)
    execute(demo_pull)
    execute(demo_merge)
    execute(demo_mvn_package)
    execute(demo_put)
    execute(demo_jar)
    # execute(demo_check)
    # execute(demo_netstat)
