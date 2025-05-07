import netmiko
import json
from netmiko import ConnectHandler

# 存放认证失败的设备信息
# []：表示一个空的列表（list），如果某台设备出现认证失败则可以将该设备的信息（例如 IP、设备名称等）添加到这个列表中，便于后续排查或输出报告
switch_with_authentication_issue = []
# 存放网络不通的设备信息
switch_not_reachable = []

with open('20250507-netmiko-H3C-Login&jsonlist.json') as f:
    devices = json.load(f) #作用是从打开的文件对象 f 中加载 JSON 格式的数据，并将其解析为 Python 对象（通常是字典或列表），然后赋值给变量 devices。
    print(devices)  
    for device in devices: 
        try:
            with ConnectHandler(**device['connection']) as conn: #with ... as conn	创建连接并赋值给 conn，离开代码块时自动断开连接
                hostname = device['name']
                print(f'已经成功登陆交换机｛hostname｝')
                output = conn.send_command('display current-configuration | include sysname')
                print(output)
        except netmiko.NetmikoAuthenticationException:
        #这个异常会在使用 Netmiko 登录设备时，如果用户名或密码错误等情况发生时被触发
            print(f'认证失败的设备是：{hostname}')
            #使用了 f-string 格式化输出，变量 hostname 应该是在前面定义的设备主机名或 IP
            switch_with_authentication_issue.append(device['connection']['host']) 
            # (device['connection']['host'])表示从嵌套字典结构中获取设备的主机地址（IP 或域名）
        except netmiko.NetmikoTimeoutException:
            print(device['name'] + "设备不可达")
            switch_not_reachable.append(device['connection']['host'])

print('\n ====结果输出====')
print('·下列交换机用户验证失败：')
for i in switch_with_authentication_issue:
    print(f"  {i}")

print('·下列交换机不可达：')
for i in switch_not_reachable:
    print(f"  {i}")