# -*- coding:utf-8 -*-
import time
import sys, os
from abc import ABCMeta

from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm
from fabric.context_managers import settings, hide

from release.setting import Configer, Logger
from release.util.crypt import prpcrypt as CRYPT


class Component(object):
    __metaclass__ = ABCMeta
    # [server] model
    DEFAULT_MODEL = None
    FILE_TYPE = '.jar'
    CLASS_TYPE = "Component"
    COMPONENT_TYPE = None
    TASK_RELY = None

    def __init__(self, model):
        self.__finnal_configer__ = Configer()
        self.__finnal_logger__ = Logger().get_logger()

        self.model = model
        self.path_local = self.__finnal_configer__.get_params("path_local", model)
        # [Apps] domain
        self.DEFAULT_DOMAIN = self.__finnal_configer__.get_params('Apps', 'domain')

        # 4）停止服务 jps | awk  '{ if($(NF) == "scmweb.jar"){print $(NF-1)}}' |xargs  kill -9
        # @runs_once
        def model_server_kill(self):
            self.__finnal_logger__.info("[INFO]  ............................................ 停止服务 > model_kill")
            try:
                while True:
                    with settings(hide('running'), warn_only=False):
                        # result = run('ps -ef |grep java |grep ' + self.model + ' |grep -v grep | awk \'{print $2}\' ')
                        PID = run(
                            'jps | awk  \'{ if($(NF) == \"' + self.model + Component.FILE_TYPE + '\"){print $(NF-1)}}\'')
                        self.__finnal_logger__.info(yellow("PID: %s" % (PID)))
                        if PID != None and PID != '' and int(PID) > 0:
                            self.__finnal_logger__.warning(
                                yellow("[INFO]  ............................................ 进程存在，进行kill > model_kill"))
                            run("kill  %s && sleep 1" % (PID), pty=False)
                            time.sleep(1)
                        # open_shell('jps | awk  \'{ if($(NF) == \"' + model + '.jar\"){print $(NF-1)}}\' |xargs  kill -9 ')
                        else:
                            self.__finnal_logger__.warning(
                                blue("[INFO]  ............................................ 已经杀掉进程，没有发现服务 > model_kill"))
                            break
            except Exception as e:
                self.__finnal_logger__.error(red(str(e)))
                sys.exit()
            self.__finnal_logger__.info(
                blue("[INFO]  ............................................ 停止服务完毕 > model_kill"))

    # 发布成功
    # @runs_once
    def model_end(self):
        self.__finnal_logger__.info(
            blue("[INFO]  ............................................ [" + self.model + "] 工作流程执行完毕..."))

    @staticmethod
    def extract_component_class(component_type):
        """
        提取组件类型
        :param component:
        :return:
        """
        return eval('%s%s' % (component_type, Component.CLASS_TYPE))

    @staticmethod
    def runmkdir(dir):
        with settings(hide('running'), warn_only=False):
            run(''' mkdir -p %s ''' % dir)


class GitComponent(Component):
    # [branch]
    DEFAULT_BRANCH = None

    def __init__(self, model, branch):
        super().__init__(model)
        self.branch = branch
        self.path_git = self.__finnal_configer__.get_params("path_git", model)
        self.root = self.__finnal_configer__.get_params("path_local", "root")

    @runs_once
    def model_dir_check(self):
        # with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=False):
        Component.runmkdir(self.root)

    # 代码克隆
    @runs_once
    def model_mvn_clone(self):
        with settings(hide('running'), warn_only=False):
            with lcd(self.root):
                local("rm  -rf %s" % (self.path_local))
                local('git clone -b %s %s' % (self.branch, self.path_git))

    @runs_once
    def model_branch_list(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 远程分支列表：")
        with settings(hide('running', 'stdout'), warn_only=False):
            with lcd(self.path_local):
                branchs = local("git remote show origin | awk '{L[NR]=$1}END{for (i=6;i<=NR-4;i++){print L[i]}}'")
                self.__finnal_logger__.info(branchs)
                return branchs

    # 代码更新合并
    @runs_once
    def model_merge(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 更新合并 > model_merge")
        with settings(hide('running'), warn_only=False):
            with lcd(self.path_local):
                local('git fetch')
                local('git checkout %s' % (self.branch))
                local('git merge origin/%s' % (self.branch))
        self.__finnal_logger__.info(blue("[INFO]  ............................................ 更新合并成功 > model_merge"))

    # 代码更新合并
    @runs_once
    def model_pull(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 更新合并 > model_pull")
        with settings(hide('running'), warn_only=False):
            with lcd(self.path_local):
                local('git fetch')
                local('git checkout %s' % (self.branch))
                local('git pull origin %s' % (self.branch))
        self.__finnal_logger__.info(blue("[INFO]  ............................................ 更新合并成功 > model_pull"))


class MainComponent(Component):
    DEFAULT_DEPLOY = 'prod'

    def __init__(self, model, deploy):
        super().__init__(model)
        if deploy != None and deploy != '':
            self.deploy = deploy
        self.path_local_target = self.__finnal_configer__.get_params("path_local_target", model)
        self.path_remote = self.__finnal_configer__.get_params("path_remote", model)
        env.user = self.__finnal_configer__.get_params('Account', 'user')
        password = CRYPT.get_password(self.DEFAULT_DOMAIN, self.__finnal_configer__.get_params('Account', 'password'))
        env.password = password
        env.hosts = self.__finnal_configer__.get_params('server_hosts', self.model, self.deploy)

    # @runs_once
    def model_dir_check(self):
        # with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=False):
        Component.runmkdir(os.path.join(self.path_remote, 'target', 'temp'))
        Component.runmkdir(os.path.join(self.path_remote, 'target', 'backup'))

    # 2）打包：start /root/work/nq_basicservice/deploy/basicservice-mvn-build-prod.bat
    @runs_once
    def model_mvn_package(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 打包 > model_mvn_package")
        with settings(hide('running'), warn_only=False):
            with lcd(self.path_local):
                local('mvn clean compile package install -Dmaven.test.skip=true -U -P %s' % (self.deploy))
        self.__finnal_logger__.info(
            blue("[INFO]  ............................................ 打包成功 > model_mvn_package"))

    # 3）发包：cp -rf /root/work/nq_basicservice/bs-web/target/bsweb.jar /home/admin/bsweb/target/temp
    # @runs_once
    def model_jar_push(self):
        if self.model == None or self.model == '':
            return
        self.__finnal_logger__.info("[INFO]  ............................................ 远程发包 > model_jar_push")
        with settings(hide('running'), warn_only=False):
            with lcd(self.path_local_target):
                result = put(self.model + Component.FILE_TYPE,
                             os.path.join(self.path_remote, 'target', 'temp', self.model) + Component.FILE_TYPE)
                if result.failed and not confirm("put file faild, Continue[Y/N]?"):
                    self.__finnal_logger__.info(abort("Aborting file put task!"))
                    self.__finnal_logger__.info(
                        self.__finnal_logger__.error(
                            red("[INFO]  ............................................ 远程发包失败 > model_jar_push")))
                    sys.exit()
                else:
                    self.__finnal_logger__.info(
                        self.__finnal_logger__.info(
                            blue("[INFO]  ............................................ 远程发包成功 > model_jar_push")))

    # 校验文件
    def model_jar_check(self):
        with settings(hide('running'), warn_only=False):
            with lcd(self.path_local_target):
                lmd5 = local('md5sum ' + self.model + Component.FILE_TYPE, capture=True).split(' ')[0]
                rmd5 = run('md5sum ' + os.path.join(self.path_remote, 'target', 'temp',
                                                    self.model) + Component.FILE_TYPE).split(' ')[0]
            if lmd5 == rmd5:
                return True
            else:
                return False

    # 5）
    # 备份：cp -rf /home/admin/bsweb/target/bsweb.jar  backup
    # 替换jar文件: cp -rf /home/admin/bsweb/target/temp/bsweb.jar /home/admin/bsweb/target
    # @runs_once
    def model_jar_upgraded(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 替换jar文件 > model_jar_prod")
        with settings(hide('running'), warn_only=False):
            with cd(os.path.join(self.path_remote, 'target')):
                if int(run(" [ -e '" + self.model + Component.FILE_TYPE + "' ] && echo 11 || echo 10")) == 11:
                    run(
                        'cp -rf  ' + self.model + Component.FILE_TYPE + '  ./backup/' + self.model + Component.FILE_TYPE + '.$(date +%Y%m%d.%H.%M.%S)')
                run('mv -f  ./temp/' + self.model + Component.FILE_TYPE + ' ./')
        self.__finnal_logger__.info(
            self.__finnal_logger__.info(
                blue("[INFO]  ............................................ 替换jar文件成功 > model_jar_prod")))

    # 6）重启服务：cd /home/admin/bsweb/bin; sh bsappstart.sh start
    # @runs_once
    def model_server_startup(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 重启服务 > model_server_startup")
        with settings(hide('running'), warn_only=False):
            with cd(os.path.join(self.path_remote, 'bin')):
                # run("find . -name '*appstart.sh' -exec {} start \;")
                # run("sh bsappstart.sh start && sleep 3 ", pty=False)
                run("find . -name '*appstart.sh' -exec {} start \; && sleep 3 ", pty=False)
        self.__finnal_logger__.info(
            self.__finnal_logger__.info(
                blue('[INFO]  ............................................ 重启服务完成 > model_server_startup')))

    # 查看服务
    # @runs_once
    def model_netstat(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 查看服务 > model_netstat")
        self.__finnal_logger__.info(".................正在查看，请稍等...........................")
        with settings(hide('running'), warn_only=True):
            local('sleep 2')
            run("ps aux | grep java | grep -v grep ", pty=False)
            local('sleep 1')
            self.__finnal_logger__.info("[INFO]  ............................................ JPS : ")
            open_shell("jps && exit ")


class BackUpComponent(Component):
    DEFAULT_DEPLOY = 'prod'

    def __init__(self, model, deploy):
        super().__init__(model)
        if deploy != None and deploy != '':
            self.deploy = deploy
        self.path_remote = self.__finnal_configer__.get_params("path_remote", model)
        env.user = self.__finnal_configer__.get_params('Account', 'user')
        password = CRYPT.get_password(self.DEFAULT_DOMAIN, self.__finnal_configer__.get_params('Account', 'password'))
        env.password = password
        env.hosts = self.__finnal_configer__.get_params('server_hosts', self.model, self.deploy)
        self.file = None

    # @runs_once
    def model_input_backup_file(self):
        self.__finnal_logger__.info(white('Release file: '))
        while (True):
            file = input("please input file from head list:")
            if file == None or file == '' or self.model not in file:
                red('输入有误，文件名称不规范,重新输入...')
            else:
                self.__finnal_logger__.info(blue("您输入的文件名称是[%s]" % (file)))
                self.file = file
                return

    # 5）
    # 查看文件: ll /home/admin/tradeweb/target/backup
    # @runs_once
    def model_jar_backup_list(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 还原jar文件 > model_jar_backup")
        try:
            with settings(hide('running'), warn_only=False):
                with cd(os.path.join(self.path_remote, 'target', 'backup')):
                    result = run('ls  -l ' + os.path.join(self.path_remote, 'target',
                                                          'backup') + ' ' + self.model + Component.FILE_TYPE + '*')
                    if "No such file or directory" in result:
                        self.__finnal_logger__.error(
                            red("[ERROR]  ............................................ 未发现备份文件"))
                        sys.exit()
                    else:
                        return result
        except Exception as e:
            self.__finnal_logger__.error(red(str(e)))
            sys.exit()

    # 5）
    # 还原: cp -rf /home/admin/bsweb/target/back/bswebxxxxx.jar /home/admin/bsweb/target/bsweb.jar
    # @runs_once
    def model_jar_backup(self, file):
        if file == None or file == '':
            self.__finnal_logger__.error(red("备份文件错误，请检查！！"))
            sys.exit()
        self.__finnal_logger__.info("[INFO]  ............................................ 还原jar文件 > model_jar_backup")
        with settings(hide('running'), warn_only=False):
            with cd(os.path.join(self.path_remote, 'target', 'backup')):
                run("pwd")
                with settings(hide('running'), warn_only=False):
                    if int(run(" [ -e '" + os.path.join(self.path_remote, 'target', 'backup',
                                                        file) + "' ] && echo 11 || echo 10")) == 11:
                        run('cp -rf ' + os.path.join(self.path_remote, 'target', 'backup', file) + ' ' + os.path.join(
                            self.path_remote, 'target', 'backup', self.model + Component.FILE_TYPE))
                        run('mv -f ' + ' ' + os.path.join(self.path_remote, 'target', 'backup',
                                                          self.model + Component.FILE_TYPE) + ' ' + os.path.join(
                            self.path_remote, 'target'))
                        self.__finnal_logger__.info(
                            blue("[INFO]  ............................................ 还原jar文件成功 > model_jar_backup"))
                    else:
                        self.__finnal_logger__.error(
                            red("[INFO]  ............................................ 未发现该文件 %s" % (file)))
                        sys.exit()

    # 6）重启服务：cd /home/admin/bsweb/bin; sh bsappstart.sh start
    # @runs_once
    def model_server_startup(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 重启服务 > model_server_startup")
        with settings(hide('running'), warn_only=False):
            with cd(os.path.join(self.path_remote, 'bin')):
                # run("find . -name '*appstart.sh' -exec {} start \;")
                # run("sh bsappstart.sh start && sleep 3 ", pty=False)
                run("find . -name '*appstart.sh' -exec {} start \; && sleep 3 ", pty=False)
        self.__finnal_logger__.info(
            blue('[INFO]  ............................................ 重启服务完成 > model_server_startup'))

    # 查看服务
    # @runs_once
    def model_netstat(self):
        self.__finnal_logger__.info("[INFO]  ............................................ 查看服务 > model_netstat")
        self.__finnal_logger__.info(".................正在查看，请稍等...........................")
        with settings(hide('running'), warn_only=False):
            local('sleep 2')
            run("ps aux | grep java | grep -v grep ", pty=False)
            local('sleep 1')
            self.__finnal_logger__.info("[INFO]  ............................................ JPS > ")
            open_shell("jps && exit ")
