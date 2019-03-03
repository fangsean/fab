## 线上服务自动化部署工具操作说明


#### 适用环境
    根据 config.ini 文件进行配置 服务，远程主机，路径相关信息，以及./config/$(*).json文件 配置主机，服务之间的依赖映射关系。。

#### 提供功能有如下步骤：

1.	git 执行代码更新任务
2.	go 执行发布任务
3.	backup 执行回退任务
4.	jar 打包服务 ##被依赖的不需要发布的服务情况##
5.	kill 停止服务进程
6.	restart  重启服务进程
7.	encrypt 加密字符串密码
8.	test 测试



```linux
[root@localhost fab]# fab list

Warning: Command(s) not found:
    list

Available commands:

        backup   执行回退任务
        encrypt  加密字符串密码
        git      执行代码更新任务
        go       执行发布任务
        jar      打包服务 ##被依赖的不需要发布的服务情况##
        kill     停止服务进程
        restart  重启服务进程
        test     测试


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
见 .ini文件 和 json文件
-----------------------
#### init app
```
DOS:pip install --editable .
```