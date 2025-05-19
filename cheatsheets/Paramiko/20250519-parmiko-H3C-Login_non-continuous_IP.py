# 实验目的：登录非连续的 H3C S 系列交换机，关闭默认开启的 STP 协议

import paramiko
import time
from getpass import getpass

username = input("Enter your username: ")
password = getpass("Enter your password: ")

with open("ip_list.txt", "r") as f:
    for ip in f:
        ip = ip.strip()

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)

        print(f"Successfully connected to device {ip}")
        remote_connection = ssh_client.invoke_shell()

        # 关闭分屏功能
        remote_connection.send("screen-length disable\n")
        # 进入系统视图
        remote_connection.send("system-view\n")
        # 关闭消息通知（如支持）
        remote_connection.send("undo info-center enable\n")
        # 关闭 STP
        remote_connection.send("stp disable\n")
        # 返回用户视图
        remote_connection.send("quit\n")
        # 保存配置
        remote_connection.send("save\n")
        remote_connection.send("y\n")  # H3C 通常用 y 而不是 Y
        time.sleep(1)

        output = remote_connection.recv(65535)
        print(output.decode("ascii"))

        ssh_client.close()