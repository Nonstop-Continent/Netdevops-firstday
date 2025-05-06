'''
实验目的：
（1）调用 send_command() 函数，执行 display interface description 检查接口描述。
（2）调用 send_config_set() 函数，通过列表形式，配置 interface GigabitEthernet 0/0/0 的描述为“descby_send_config_set()”。
（3）调用 send_config_from_file()函数，通过文件形式，配置 interface GigabitEthernet 0/0/1 的描述为“descby_send_config_from_file()”。
'''

from netmiko import ConnectHandler
h3c_device_01 = {
    'device_type': 'hp_comware',
    'host': '11.0.0.1',
    'username': 'netops',
    'password': 'Admin@1234',
    'port': 22,
}

commands = ['interface GigabitEthernet 1/0/1', 'description descby_send_config_set()','quit','interface GigabitEthernet 1/0/2','description descby_send_config_set()']

with ConnectHandler(**h3c_device_01) as h3c_ssh:
    print("已经成功登陆交换机" + h3c_device_01['host'])

    print('===实验目的1交互形式推送一条指令===')
    output = h3c_ssh.send_command('display interface brief | include GE1/0/[12][^0-9]')
    print(output)

    print('===实验目的2：通过列表形式推送多条指令===')
    output = h3c_ssh.send_config_set(commands)
    print(output) 

    print('===实验目的3：通过文件形式推送多条指令===')
    output = h3c_ssh.send_config_from_file('20250506-netmiko-H3C-sendcommand.txt')
    print(output) 

    print('===最后再检查配置')
    output = h3c_ssh.send_command('display interface brief | include GE1/0/[12][^0-9]')
    print(output)


