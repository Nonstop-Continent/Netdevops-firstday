'''
实验目的：
1、配置对象中如果出现账号密码错误、IP不可达时，程序可以继续执行。
2、使用try...except结构
'''
import paramiko
import time
import getpass
import sys
import socket


username = input("请输入用户名：")
password = getpass.getpass("请输入密码：")
#将命令行中第一个参数的值赋给变量 ip_file，通常用于获取用户指定的输入文件路径;
#sys.argv 是一个包含命令行参数的列表，sys.argv[0] 是脚本名称，sys.argv[1] 是第一个传入的参数。

switch_with_authentication_issue = []
switch_not_reachable = []

iplist = open("ip_list.txt",'r')
for line in iplist.readlines():#readlines() 方法会返回文件中所有行的列表
    try:
        ip = line.strip()#去掉每行末尾的换行符
        print("正在连接设备：",ip)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip,username=username,password=password,look_for_keys=False,timeout=5)
        print("连接成功")
        command = ssh_client.invoke_shell()
        cmdlist = open("cmd_file.txt",'r')
        cmdlist.seek(0) #调用文件对象的 seek 方法，参数 0 表示移动到文件的起始位置;常用于在读取或写入文件后，重新定位到文件开头以便再次读取或覆盖内容
        for line in cmdlist.readlines():
            command.send(line + "\n")
        time.sleep(2)
        cmdlist.close()
        output = command.recv(65535)
        print(output.decode('ascii'))
    except paramiko.ssh_exception.AuthenticationException:
        print("账号密码错误")
        switch_with_authentication_issue.append(ip)
    except socket.error:
        print(ip + "is not reachable.")
        switch_not_reachable.append(ip)

iplist.close()
ssh_client.close()

print("\n账号密码错误的设备:")
for i in switch_with_authentication_issue:
    print(i)
print("\n不可达的设备")
for i in switch_not_reachable:
    print(i)
