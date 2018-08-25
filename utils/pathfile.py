#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import configparser

# config
conf = configparser.ConfigParser()
print(conf)
conf.read("../properties/path.properties", encoding='utf-8')
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
