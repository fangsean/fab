# -*- encoding: utf-8 -*-
# from fabric.api import run, cd, env, local, lcd
from fabric.api import *

env.hosts = ["root@47.98.187.132:22"]
env.password = "nanquan@2017"

serverInfo = {
    'preserver':
        {
            'bs': ['root@47.98.187.132:22', 'root@192.168.1.13:22'],
            'tradeweb': ['root@47.98.187.132:22', 'root@192.168.1.13:22'],
            'scm': ['root@47.98.187.132:22', 'root@192.168.1.13:22'],
        },
    'prodserver':
        {
            'bs': ['root@47.98.187.132:22', 'root@192.168.1.13:22'],
            'tradeweb': ['root@47.98.187.132:22', 'root@192.168.1.13:22'],
            'scm': ['root@47.98.187.132:22', 'root@192.168.1.13:22'],
        },
}


