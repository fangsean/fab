from fabric.colors import *
from setting import *

def show():
    print, green('success')
    print, red('fail')
    print, yellow('yellow')

local_repo_path = r"/root/work"
remote_repo_path = "/root"


def local_ops():
    # commit local changes and push to git@osc
    with lcd(local_repo_path):
        local("echo 'add and commit changes in local'")
        local("git add git_deploy.py")
        local("git commit")
        # local("git commit")
        local("git pull origin")
        local("git push origin")


def remote_ops():
    # pull repo from git@osc
    run("echo 'async repo in remote'")
    with cd(remote_repo_path):
        run("git pull origin")


def task():
    local_ops()
    remote_ops()