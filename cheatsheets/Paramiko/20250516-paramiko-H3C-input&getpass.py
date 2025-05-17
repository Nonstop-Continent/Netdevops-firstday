'''
实验目的
1、使用input()函数和getpass模块实现交互式的SSH用户名和密码输入
2、通过for循环同时为2台设备cisco交换机配置VLAN10-VLAN20
'''

import paramiko
import time
import getpass #内建模块，交互式提示用户输入密码，且密文显示（采用input()函数是直接显示明文）

username = input("请输入用户名：")
password = getpass.getpass("请输入密码：")

for i in range(115,117):
    ip = "192.168.112." + str(i) # i是个整数格式，需要转成字符串格式才能与其他字符串拼接。
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print("successfully connect to ",ip)    
    command = ssh_client.invoke_shell()

    #关闭分屏功能
    command.send("screen-length 0 temporary\n")
    #进入系统视图
    command.send("system\n")
    for n in range (10,21): #嵌套循环，需要注意缩进。
        print("Creating VLAN " + str(n))
        command.send("vlan " + str(n) + "\n")
        command.send("desc Python_VLAN_" + str(n) + "\n")
        time.sleep(1)  #每创建一个VLAN，暂停1秒。

    command.send("return\n")
    command.send("save\n")
    command.send("Y\n")
    #在 output 前，一定记得休眠等待，否则极有可能回显抓取不全
    time.sleep(2)
    outputt = command.recv(65535)
    print(outputt.decode('ascii'))

ssh_client.close