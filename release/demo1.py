#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from fabric.api import *
from fabric.colors import *

# from utils.pathfile import gitpath, branch, git1, buildpath1, local_path1, appliation1, user, password, hosts1
from fabric.context_managers import *

import configparser

# config
conf = configparser.ConfigParser()
conf.read("/root/work/fab/properties/path.properties", encoding='utf-8')
conf.sections()

# user and passwd
user = conf.get('Account', 'user')
password = conf.get('Account', 'password')

# host
hosts1 = conf.get('server', 'hosts1')
hosts2 = conf.get('server', 'hosts2')
hosts3 = conf.get('server', 'hosts3')
hosts4 = conf.get('server', 'hosts4')
hosts5 = conf.get('server', 'hosts5')

# branch
branch = conf.get('branch', 'branch')

# git_clone_address
git1 = conf.get('gitpath', 'git1')
git2 = conf.get('gitpath', 'git2')
git3 = conf.get('gitpath', 'git3')
git4 = conf.get('gitpath', 'git4')

# git_storage_address
gitpath = conf.get('path', 'gitpath')

# build_path
buildpath1 = conf.get('path', 'buildpath1')
buildpath2 = conf.get('path', 'buildpath2')
buildpath3 = conf.get('path', 'buildpath3')
buildpath4 = conf.get('path', 'buildpath4')

# war_pak_path
local_path1 = conf.get('path', 'local_path1')
local_path2 = conf.get('path', 'local_path2')
local_path3 = conf.get('path', 'local_path3')
local_path4 = conf.get('path', 'local_path4')

# release_path
appliation1 = conf.get('path', 'appliation1')
appliation2 = conf.get('path', 'appliation2')
appliation3 = conf.get('path', 'appliation3')

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
    with lcd(gitpath):
        local('mvn clean install -Dmaven.test.skip -U %s' % (deploy))


@runs_once
def demo_pull():
    with lcd(buildpath1):
        local('git checkout developer')
        local('git pull')


@runs_once
def demo_merge():
    with lcd(buildpath1):
        local('git fetch')
        local('git merge origin/developer')


@runs_once
def demo_put_before():
    with cd(appliation1):
        with settings(warn_only=True):
            run('mv demo.war ../backup/demo.war_$(date '
                '+%Y-%m-%d)_bak')
            run('rm -rf *')


@runs_once
def demo_put():
    with lcd(local_path1):
        put('bsweb.jar', appliation1)


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
    # execute(demo_jar)
    # execute(demo_check)
    # execute(demo_netstat)
