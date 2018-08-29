## 线上服务自动化部署工具操作说明


#### 适用环境
    根据 config.ini 文件进行配置 服务，远程主机，以及之间的依赖关系。

#### 提供功能有如下步骤：
1. [ fab git ]  构建本地代码库
2. [ fab go ]   远程发布服务
3. [ fab backup ] 远程回退服务


```linux
[root@localhost fab]# fab list

Warning: Command(s) not found:
    list

Available commands:

    backup
    git
    go


```



#### 操作说明：

操作控制台环境：  

【主机】：192.168.1.13\
【用户】：root\
【密码】：*** \
【目录】：`/root/work/fab`\
【命令】：fab



-----------
<i>以下步骤根据实际情况操作！</i>

##### 1.操作本地代码库
构建本地代码库，更新分支代码

```linux
[root@localhost fab]# fab git
[localhost] Executing task 'git'
***git 执行代码更新任务***
        参数缺失！
        请输入执行参数:
                model:{'bsweb': '后台公共服务系统', 'tradeweb': '前台客户系统', 'scmweb': '后台管理系统', 'sellerweb': '后台管理系统'}
                branch:{'branch': 'developer'}
        如 fab git:model=bsweb,branch=developer
Do
```
> fab git:model=bsweb,branch=jsen_branch  ## 使用jsen_branch分支 构建本地bsweb代码库 

...等待控制台提示执行完成


##### 2.远程发布服务
代码打包，远程发包，控制进程，远程部署，验证发布结果

```linux
[Nq007] Executing task 'go'
***go 执行发布任务***
        参数缺失！
        请输入执行参数:
                model:{'bsweb': '后台公共服务系统', 'tradeweb': '前台客户系统', 'scmweb': '后台管理系统', 'sellerweb': '后台管理系统'}
                deploy:{'pre': '预发', 'prod': '生产', 'test': '测试', 'dev': '本地'}
        如 fab go:model=bsweb,deploy=pre
Do

```

> fab go:model=bsweb,deploy=pre ##使用pre环境打包本地bsweb代码库,发布服务到bsweb


##### 3.远程回退服务
发布版本的远程回退，控制进程，远程部署，验证发布结果

```
[root@localhost fab]# fab backup
[Nq007] Executing task 'backup'
***backup 执行回退任务***
        参数缺失！
        请输入执行参数:
                model:{'bsweb': '后台公共服务系统', 'tradeweb': '前台客户系统', 'scmweb': '后台管理系统', 'sellerweb': '后台管理系统'}
        如 fab backup:model=bsweb
Do

```

> fab backup:model=bsweb #通过指定的备份文件 回退bsweb的服务版本

---



#### 配置文件说明

```


#################该区域配置为： 基本配置 #####################
[Apps]
domain = nqtown

;访问参数
[Account]
;用户
user = admin
;加密后的密码
password = 72eb150361d194b1d414a0da83d885e4

[branch]
;无效
branch = developer

;环境版本
[deploy]
pre = 预发
prod = 生产
test = 测试
dev = 本地

;远程hosts列表
[hosts]
;采用host别名，暂时禁止
;host1 = Nq001
;host2 = Nq002
;host3 = Nq003
;host4 = Nq004
host1 = Nq007
host2 = Nq007
host3 = Nq007
host4 = Nq007
host5 = Nq007
host6 = localhost
;... ...添加n个,key键不冲突就行
###################################!

;服务归类
[servers]
bsweb = 后台公共服务系统
tradeweb = 前台客户系统
scmweb = 后台管理系统
sellerweb = 后台管理系统

;server对应哪些host主机，必须在[hosts]中选择，[hosts]列表没有的一次添加，key键不冲突就行
[server_hosts]
;bsweb = host1,host2
bsweb = host5,host6
tradeweb = host1,host2
scmweb = host3,host4
sellerweb = host3,host4

;更新代码地址
[path_git]
bsweb = git@git.coding.net:shenlan/nq_basicservice.git
tradeweb = git@git.coding.net:shenlan/nq_tradeweb.git
scmweb = git@git.coding.net:shenlan/nq_scmweb.git
sellerweb = git@git.coding.net:shenlan/nq_sellerweb.git

;本地代码库，工作空间
[path_local]
;工作空间根目录
root = /root/work/
bsweb = /root/work/nq_basicservice/
tradeweb = /root/work/nq_tradeweb/
scmweb = /root/work/nq_scmweb/
sellerweb = /root/work/nq_sellerweb/

;本地jar包存放地址
[path_local_target]
bsweb = /root/work/nq_basicservice/bs-web/target/
tradeweb = /root/work/nq_tradeweb/target/
scmweb = /root/work/nq_scmweb/target/
sellerweb = /root/work/nq_sellerweb/target/


;远程主机对应服务地址
[path_remote]
bsweb = /home/admin/bsweb/
tradeweb = /home/admin/tradeweb/
scmweb = /home/admin/scmweb/
sellerweb = /home/admin/sellerweb/


```
-----------------------
DOS:pip install --editable .
