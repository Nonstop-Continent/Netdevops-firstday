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

f = open("ip_list.txt","r")
for ip in f.readlines():
    ip = ip.strip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,username=username,password=password,look_for_keys=False)
    print ("\n\nConnecting to device " + (ip))
    print ("Successfully connected to device ",ip)
    remote_connection = ssh_client.invoke_shell()
    remote_connection.send("config t\n")
    remote_connection.send("router eigrp 90\n")
    remote_connection.send("end\n")
    remote_connection.send("wr mem\n")
    time.sleep(1)
    output = remote_connection.recv(65535)
    print (output.decode("ascii"))


f.close()
ssh_client.close()
