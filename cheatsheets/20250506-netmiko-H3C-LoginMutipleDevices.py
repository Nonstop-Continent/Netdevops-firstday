import netmiko
from netmiko import ConnectHandler

#存放认证失败的设备信息
switch_with_authentication_issue = []
#存放网络不通的设备信息
switch_not_reachable = []

with open('20250506-netmiko-H3C-LoginMutipleDevices.txt') as f:
    for ips in f.readlines():
        try:
            ip = ips.strip()
            connection_info =  {
                'device_type': 'hp_comware',
                'ip': ip,
                'username': 'netops',
                'password': 'Admin@1234',
                # 'conn_timeout': 10sec
            } 
            with ConnectHandler(**connection_info) as conn:
                print('Connected to {}'.format(ip))
                #执行命令
                output = conn.send_command('display cur | include sysname' )
                print(output)
        except netmiko.NetmikoAuthenticationException:
            print('Authentication failed for {}'.format(ip))
            switch_with_authentication_issue.append(ip)

        except netmiko.NetmikoTimeoutException:
            print('{} is not reachable'.format(ip))
            switch_not_reachable.append(ip)


# 特别说明一下，Netmiko3和4有点区别。
# 如果已升级到Netmiko4的话，直接运行except netmiko.ssh_exception.NetmikoTimeoutException会报错。
# 可改为except netmiko.NetmikoTimeoutException。

print('\n ====结果输出====')
print('·下列交换机用户验证失败：')
for i in switch_with_authentication_issue:
    print(f"  {i}")

print('·下列交换机不可达：')
for i in switch_not_reachable:
    print(f"  {i}")