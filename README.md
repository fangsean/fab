发布步骤：
**bs 为例**
1）备份：cp -rf /home/admin/bsweb/target/bsweb.jar  backup
2）打包：start /root/work/nq_basicservice/deploy/basicservice-mvn-build-prod.bat
3）上传：cp -rf /root/work/nq_basicservice/bs-web/target/bsweb.jar /home/admin/bsweb/target/temp
4）停止服务 jps | awk  '{ if($(NF) == "scmweb.jar"){print $(NF-1)}}' |xargs  kill -9
5）替换jar文件: cp -rf /home/admin/bsweb/target/temp/bsweb.jar /home/admin/bsweb/target
6）重启服务：cd /home/admin/bsweb/bin; sh bsappstart.sh start 
7）结束/验证 jps 或者 ps aux | grep java | grep -v grep


