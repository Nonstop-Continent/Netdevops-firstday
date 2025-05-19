# 实验目的：登陆非连续的华为设备，关闭华为交换机默认开启的STP协议

import paramiko 
import time 
import os
from getpass import getpass

'''
# 检查文件系统中是否存在名为"ip_list.txt"的文件，并打印结果
print(os.path.isfile("ip_list.txt"))

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# 获取当前脚本所在的目录
script_directory = os.path.dirname(script_path)

# 构建 ip_list.txt 的完整路径
ip_list_path = os.path.join(script_directory, "ip_list.txt")

# 检查 ip_list.txt 是否存在于当前脚本目录下，并打印结果
print(os.path.isfile(ip_list_path))

'''

username = input("Enter your username: ")
password = getpass("Enter your password: ")

f = open("ip_list.txt","r") #"r" 表示以只读方式打开文件
for ip in f.readlines():
    ip = ip.strip() #去除字符串 ip 两端的空白字符（如空格、换行、制表符等），并重新赋值给变量 ip

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,username=username,password=password,look_for_keys=False)

    print ("Successfully connected to device ",ip)
    remote_connection = ssh_client.invoke_shell() #ssh_client.invoke_shell() 创建一个远程 SSH 交互式 shell 会话，并将该会话对象赋值给变量 remote_connection。
    remote_connection.send("N\n")
    #关闭分屏功能
    remote_connection.send("screen-length 0 temporary\n")
    #进入系统视图
    remote_connection.send("system\n")
    #关闭消息通知
    remote_connection.send("undo info-center enable\n")
    remote_connection.send("undo stp enable\n")
    remote_connection.send("commit\n")
    time.sleep(2)
    
    #返回用户视图
    remote_connection.send("return\n")
    #保存配置
    remote_connection.send("save\n")
    remote_connection.send("Y\n")
    time.sleep(1)
    output = remote_connection.recv(65535)
    print (output.decode("ascii"))
f.close()
ssh_client.close()


'''
ssh_client = paramiko.SSHClient()
这段代码创建了一个 SSHClient 对象，用于实现 SSH 连接。具体功能如下：
1)paramiko.SSHClient() 是 Paramiko 库提供的类，用于建立和管理 SSH 连接。
2)ssh_client 是该类的一个实例，后续可用于连接远程服务器、执行命令等操作。

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
自动接受所有未知的SSH主机密钥指纹，避免连接时因未保存的主机密钥而抛出异常。
1)set_missing_host_key_policy()：设置当目标主机的密钥未在本地缓存时的处理策略
2)paramiko.AutoAddPolicy()：自动将未知主机密钥添加到本地缓存中（不安全，适合测试环境）

ssh_client.connect(hostname=ip,username=username,password=password,look_for_keys=False)
该代码使用paramiko库的SSHClient对象连接远程SSH服务器。
hostname=ip：指定目标主机的IP地址
username=username：登录用户名
password=password：登录密码
look_for_keys=False：禁用自动查找本地私钥，避免尝试使用密钥认证
'''


