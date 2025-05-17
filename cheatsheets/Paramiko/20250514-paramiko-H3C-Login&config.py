import paramiko
import time

# 资源信息
ip = '11.0.0.1'
username = 'netops'
password = 'Admin@1234'

#paramiko 联机套路
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
print("successfully connect to ",ip)

#注：这些代码中，我们可以随时加插print(xx)进行测试，术语叫“调试”。

command = ssh_client.invoke_shell()
command.send("sys\n")
command.send("interface loopback 0\n")
command.send("ip address 1.1.1.1 255.255.255.255\n")
command.send("return\n")
command.send("save\n")
command.send("y\n")
command.send("\n")

# 这种场景，paramiko 模块模仿人工进行联机操作。

time.sleep(3)
command.send("display this\n")    # 这里的 dis this 查询意义不大，也可以修改为如下命令，去掉注释即可执行。
# command.send("display current-configuration interface LoopBack 0\n")
time.sleep(1)

# 调用延迟的目的也是等待设备响应和回显信息，否则执行太快，回显信息会“捞”不全。
output = command.recv(65535)
print(output.decode("ascii"))   # 回显信息涉及到编解码。

# 操作完成后，需要断开 SSH 连接。

# 关闭 invoke_shell。
command.close()
# 关闭 ssh 客户端。
ssh_client.close()