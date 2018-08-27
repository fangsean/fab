# -*- coding:utf-8 -*-
import time
from abc import ABCMeta

from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm

from release.util.crypt import prpcrypt as CRYPT

from release.setting import Configer

__configer__ = Configer()


class Component(object):
    __metaclass__ = ABCMeta
    # config
    configer = __configer__
    # [server] model
    DEFAULT_MODEL = None
    FILE_TYPE = '.jar'
    CLASS_TYPE = "Component"
    COMPONENT_TYPE = None
    TASK_RELY = None

    def __init__(self, model):
        self.model = model
        self.path_local = Component.configer.get_params("path_local", model)
        # [Apps] domain
        self.DEFAULT_DOMAIN = Component.configer.get_params('Apps', 'domain')

    # 发布成功
    @runs_once
    def model_end(self):
        print(blue("[INFO]  ............................................ [" + self.model + "] 工作流程执行完毕..."))

    @staticmethod
    def extract_component_class(component_type):
        """
        提取组件类型
        :param component:
        :return:
        """
        return eval('%s%s' % (component_type, Component.CLASS_TYPE))


class GitComponent(Component):
    # [branch]
    DEFAULT_BRANCH = None

    def __init__(self, model, branch):
        super().__init__(model)
        self.branch = branch
        self.path_git = Component.configer.get_params("path_git", model)
        self.root = Component.configer.get_params("path_local", "root")

    # 代码克隆
    @runs_once
    def model_mvn_clone(self):
        with lcd(self.root):
            local("rm  -rf %s" % (self.path_local))
            local('git clone -b %s %s' % (self.branch, self.path_git))

    @runs_once
    def model_branch_list(self):
        with lcd(self.path_local):
            branchs = local('git branch -r')
            return branchs

    # 代码更新合并
    @runs_once
    def model_merge(self):
        print("[INFO]  ............................................ 更新合并 > model_merge")
        with lcd(self.path_local):
            local('git fetch')
            local('git checkout %s' % (self.branch))
            local('git merge origin/%s' % (self.branch))
        print(blue("[INFO]  ............................................ 更新合并成功 > model_merge"))

    # 代码更新合并
    @runs_once
    def model_pull(self):
        print("[INFO]  ............................................ 更新合并 > model_pull")
        with lcd(self.path_local):
            local('git fetch')
            local('git checkout %s' % (self.branch))
            local('git pull origin/%s' % (self.branch))
        print(blue("[INFO]  ............................................ 更新合并成功 > model_pull"))


class MainComponent(Component):
    configer = Component.configer
    # [Account] passwd
    DEFAULT_PASSWORD = configer.get_params('Account', 'password')

    DEFAULT_DEPLOY = 'prod'

    def __init__(self, model, deploy):
        super().__init__(model)
        if deploy != None and deploy != '':
            self.deploy = deploy
        self.path_local_target = Component.configer.get_params("path_local_target", model)
        self.path_remote = Component.configer.get_params("path_remote", model)
        self.path_remote = Component.configer.get_params("path_remote", model)
        env.user = Component.configer.get_params('Account', 'user')
        password = CRYPT.get_password(self.DEFAULT_DOMAIN, MainComponent.DEFAULT_PASSWORD)
        env.password = password
        env.hosts = Component.configer.get_params('server_hosts', self.model)

    # 2）打包：start /root/work/nq_basicservice/deploy/basicservice-mvn-build-prod.bat
    @runs_once
    def model_mvn_package(self):
        print("[INFO]  ............................................ 打包 > model_mvn_package")
        with lcd(self.path_local):
            local('mvn clean compile package install -Dmaven.test.skip=true -U -P %s' % (self.deploy))
        print(blue("[INFO]  ............................................ 打包成功 > model_mvn_package"))

    # 3）发包：cp -rf /root/work/nq_basicservice/bs-web/target/bsweb.jar /home/admin/bsweb/target/temp
    @runs_once
    def model_jar_push(self):
        if self.model == None or self.model == '':
            return
        print("[INFO]  ............................................ 远程发包 > model_jar_push")
        with lcd(self.path_local_target):
            result = put(self.model + Component.FILE_TYPE,
                         os.path.join(self.path_remote, 'target', 'temp', self.model) + Component.FILE_TYPE)
            if result.failed and not confirm("put file faild, Continue[Y/N]?"):
                abort("Aborting file put task!")
                print(red("[INFO]  ............................................ 远程发包失败 > model_jar_push"))
            else:
                print(blue("[INFO]  ............................................ 远程发包成功 > model_jar_push"))

    # 校验文件
    def model_jar_check(self):
        with lcd(self.path_local_target):
            with settings(warn_only=True):
                lmd5 = local('md5sum ' + self.model + Component.FILE_TYPE, capture=True).split(' ')[0]
                rmd5 = run('md5sum ' + os.path.join(self.path_remote, 'target', 'temp',
                                                    self.model) + Component.FILE_TYPE).split(' ')[0]
            if lmd5 == rmd5:
                return True
            else:
                return False

    # 4）停止服务 jps | awk  '{ if($(NF) == "scmweb.jar"){print $(NF-1)}}' |xargs  kill -9
    @runs_once
    def model_server_kill(self):
        print("[INFO]  ............................................ 停止服务 > model_kill")
        try:
            while True:
                # result = run('ps -ef |grep java |grep ' + self.model + ' |grep -v grep | awk \'{print $2}\' ')
                PID = run('jps | awk  \'{ if($(NF) == \"' + self.model + Component.FILE_TYPE + '\"){print $(NF-1)}}\'')
                print("PID: %s" % (PID))
                if PID != None:
                    print(yellow("[INFO]  ............................................ 进程存在，进行kill > model_kill"))
                    run("kill  %s && sleep 1" % (PID), pty=False)
                    time.sleep(1)
                # open_shell('jps | awk  \'{ if($(NF) == \"' + model + '.jar\"){print $(NF-1)}}\' |xargs  kill -9 ')
                else:
                    print(yellow("[INFO]  ............................................ 已经杀掉进程，没有发现服务 > model_kill"))
                    break
        except Exception as e:
            print(red(str(e)))
        print(blue("[INFO]  ............................................ 停止服务完毕 > model_kill"))

    # 5）
    # 备份：cp -rf /home/admin/bsweb/target/bsweb.jar  backup
    # 替换jar文件: cp -rf /home/admin/bsweb/target/temp/bsweb.jar /home/admin/bsweb/target
    @runs_once
    def model_jar_upgraded(self):
        print("[INFO]  ............................................ 替换jar文件 > model_jar_prod")
        with cd(os.path.join(self.path_remote, 'target')):
            with settings(warn_only=True):
                if int(run(" [ -e '" + self.model + Component.FILE_TYPE + "' ] && echo 11 || echo 10")) == 11:
                    run(
                        'cp -rf  ' + self.model + Component.FILE_TYPE + '  ./backup/' + self.model + '$(date +%Y%m%d.%H.%M.%S)')
                run('mv -f  ./temp/' + self.model + Component.FILE_TYPE + ' ./')
        print(blue("[INFO]  ............................................ 替换jar文件成功 > model_jar_prod"))

    # 6）重启服务：cd /home/admin/bsweb/bin; sh bsappstart.sh start
    @runs_once
    def model_server_startup(self):
        print("[INFO]  ............................................ 重启服务 > model_server_startup")
        with cd(os.path.join(self.path_remote, 'bin')):
            # run("find . -name '*appstart.sh' -exec {} start \;")
            # run("sh bsappstart.sh start && sleep 3 ", pty=False)
            run("find . -name '*appstart.sh' -exec {} start \; && sleep 3 ", pty=False)
        print(blue('[INFO]  ............................................ 重启服务完成 > model_server_startup'))

    # 查看服务
    @runs_once
    def model_netstat(self):
        print("[INFO]  ............................................ 查看服务 > model_netstat")
        print(".................正在查看，请稍等...........................")
        local('sleep 5')
        run("ps aux | grep java | grep -v grep ", pty=False)
        local('sleep 1')
        print("[INFO]  ............................................ JPS > ")
        open_shell("jps && exit ")
