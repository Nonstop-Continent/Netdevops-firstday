'''
实验目的
1、使用input()函数和getpass模块实现交互式的SSH用户名和密码输入
2、通过for循环同时为2台设备cisco交换机配置VLAN10-VLAN20
'''

import paramiko
import time
import getpass

username = input("请输入用户名：")
password = getpass.getpass("请输入密码：")

for i in range(111,113):
    ip = "192.168.112." + str(i)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print("successfully connect to ",ip)
    command = ssh_client.invoke_shell()
    command.send("configure terminal\n")
    for n in range (10,21):
        print("Creating VLAN " + str(n))
        command.send("vlan " + str(n) + "\n")
        command.send("name Python_VLAN_" + str(n) + "\n")
        time.sleep(1)  

    command.send("end\n")
    command.send("wr\n")
    time.sleep(2)
    outputt = command.recv(65535)
    print(outputt.decode('ascii'))

ssh_client.close