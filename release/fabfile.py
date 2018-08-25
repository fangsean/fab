from fabric.api import *
from setting import *

@roles('preserver')
def task1():
    run('ls -l | wc -l')

@roles('productserver')
def task2():
    run('ls ~/temp/ | wc -l')

def do():
    execute(task1)
    execute(task2)
