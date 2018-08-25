# -*- coding:utf-8 -*-
from fabric.contrib.console import confirm
from fabric.api import *
from fabric.colors import *
from setting import user, password, hosts1, gitpath, git1, branch, buildpath1, appliation1, local_path1

env.user = user
env.password = password
env.hosts = hosts1


# env.roledefs = {
#      'webservers' : ['192.168.198.246', '192.168.198.247']
#      'dbservers' : ['192.168.198.245', '192.168.198.250']
# }


# 代码克隆
@runs_once
def demo_mvn_clone():
    with lcd(gitpath):
        local('rm -rf demo')
        local('git clone -b %s %s' % (branch, git1))


# 代码更新合并
@runs_once
def demo_merge():
    print("[INFO]  ............................................ 更新合并 > demo_pull")
    with lcd(buildpath1):
        local('git fetch')
        local('git checkout developer')
        local('git merge origin/developer')
        local('git pull')
    print(blue("[INFO]  ............................................ 更新合并成功 > demo_pull"))


# 2）打包：start /root/work/nq_basicservice/deploy/basicservice-mvn-build-prod.bat
@runs_once
def demo_mvn_package(deploy='prod'):
    print(deploy)
    print("[INFO]  ............................................ 打包 > demo_mvn_package")
    with lcd(gitpath):
        local('mvn clean compile package install -Dmaven.test.skip=true -U -P %s' % (deploy))
    print(blue("[INFO]  ............................................ 打包成功 > demo_mvn_package"))


# 3）发包：cp -rf /root/work/nq_basicservice/bs-web/target/bsweb.jar /home/admin/bsweb/target/temp
@runs_once
def demo_jar_push(model=None):
    if model == None:
        return
    print("[INFO]  ............................................ 远程发包 > demo_jar_push")
    with lcd(local_path1):
        result = put(model + '.jar', os.path.join(appliation1, 'target', 'temp', model) + '.jar')
        if result.failed and not confirm("put file faild, Continue[Y/N]?"):
            abort("Aborting file put task!")
            print(red("[INFO]  ............................................ 远程发包失败 > demo_jar_push"))
        else:
            print(blue("[INFO]  ............................................ 远程发包成功 > demo_jar_push"))
        # flag = demo_jar_check(model)
        # if flag == True:
        #     print(yellow("[INFO]  ............................................ 已经发布 > demo_jar_push"))
        # else:
        #     result = put(model + '.jar', os.path.join(appliation1, 'target','temp', model) + '.jar')
        #     if result.failed and not confirm("put file faild, Continue[Y/N]?"):
        #         abort("Aborting file put task!")
        #         print(red("[INFO]  ............................................ 远程发包失败 > demo_jar_push"))
        #     else:
        #         print(blue("[INFO]  ............................................ 远程发包成功 > demo_jar_push"))


# 校验文件
def demo_jar_check(model):
    if model == None:
        return False
    with lcd(local_path1):
        with settings(warn_only=True):
            lmd5 = local('md5sum ' + model + '.jar', capture=True).split(' ')[0]
            rmd5 = run('md5sum ' + os.path.join(appliation1, 'target', 'temp', model) + '.jar').split(' ')[0]
            print("lmd5 %s", (lmd5))
            print("rmd5 %s", (rmd5))
        if lmd5 == rmd5:
            return True
        else:
            return False


# 4）停止服务 jps | awk  '{ if($(NF) == "scmweb.jar"){print $(NF-1)}}' |xargs  kill -9
@runs_once
def demo_server_kill(model):
    print("[INFO]  ............................................ 停止服务 > demo_kill")
    try:
        run('jps | awk  \'{ if($(NF) == \"' + model + '.jar\"){print $(NF-1)}}\' |xargs  kill -9 ')
    except e:
        print(blue("[INFO]  ............................................ 没有发现服务 > demo_kill"))
    print(blue("[INFO]  ............................................ 停止服务完毕 > demo_kill"))


# 5）
# 备份：cp -rf /home/admin/bsweb/target/bsweb.jar  backup
# 替换jar文件: cp -rf /home/admin/bsweb/target/temp/bsweb.jar /home/admin/bsweb/target
@runs_once
def demo_jar_upgraded(model):
    if model == None:
        return
    print("[INFO]  ............................................ 替换jar文件 > demo_jar_prod")
    with cd(os.path.join(appliation1, 'target')):
        with settings(warn_only=True):
            if int(run(" [ -e '" + model + ".jar' ] && echo 11 || echo 10")) == 11:
                run('cp -rf  ' + model + '.jar  ./backup/' + model + '$(date '
                                                                 '+%Y-%m-%d)_bak')
            run('mv -f  ./temp/' + model + '.jar ./')
    print(blue("[INFO]  ............................................ 替换jar文件成功 > demo_jar_prod"))


# 6）重启服务：cd /home/admin/bsweb/bin; sh bsappstart.sh start
@runs_once
def demo_server_startup():
    print("[INFO]  ............................................ 重启服务 > demo_server_startup")
    with cd(os.path.join(appliation1, 'bin')):
        run('find . -name "*appstart.sh" -exec {} start \;')
    print(blue('[INFO]  ............................................ 重启服务完成 > demo_server_startup'))


# 查看服务
@runs_once
def demo_netstat(model):
    print("[INFO]  ............................................ 查看服务 > demo_netstat")
    print(".................正在查看，请稍等...........................")
    local('sleep 5')
    run("ps aux | grep java | grep -v grep ")
    local('sleep 1')
    open_shell("jps  &&  exit")


# 发布成功
@runs_once
def demo_end(model):
    print(blue("[INFO]  ............................................ [" + model + "] 系统已经发布成功..."))


@task()
@parallel
def go(deploy, model):
    # execute(demo_merge),
    # execute(demo_mvn_package, deploy),
    # execute(demo_jar_push, model),
    # execute(demo_server_kill, model),
    # execute(demo_jar_upgraded, model),
    execute(demo_server_startup, model),
    execute(demo_netstat, model),
    execute(demo_end, model)
