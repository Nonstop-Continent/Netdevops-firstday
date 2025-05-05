#使用netmiko模块登录H3C S6850交换机，给它的 LoopBack0口配置 IP 30.30.1.1/32，之后保存退出，打印回显。

from netmiko import ConnectHandler

h3c_device_01 = {
    'device_type': 'hp_comware',
    'host': '11.0.0.1',
    'username': 'netops',
    'password': 'Admin@1234',
    'port': 22,
}
connect = ConnectHandler(**h3c_device_01)
print('已经成功登陆交换机' + h3c_device_01['host'])

# netmiko 已经集成休眠、截屏等操作
config_commands = [
    'interface Loopback 0',
    'ip address 30.30.1.1 255.255.255.255',
]
# 如何需要系统视图下执行，可用 send_config_set，会自动执行system
# 截屏直接作为函数返回
output  = connect.send_config_set(config_commands)
print(output)

print('\n====分割线====\n')

# 如果需要用户视图下执行，可用send_command
# 截屏直接作为函数返回

result =  connect.send_command('display current-configuration interface Loopback0')
print(result)