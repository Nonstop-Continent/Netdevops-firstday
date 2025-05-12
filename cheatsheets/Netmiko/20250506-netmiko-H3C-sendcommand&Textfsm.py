'''
实验目的
（1）调用 send_command() 函数，执行 display vlan 检查交换机VLAN。
（2）制作 Textfsm 模板 display_vlan.template ，解析（1）的返回信息，把字符串格式化为咱们更容易操控的其它 Python 数据模型。
'''
from netmiko import ConnectHandler
from textfsm import TextFSM

h3c_device_01 = {
    'device_type': 'hp_comware',
    'host': '11.0.0.1',
    'username': 'netops',
    'password': 'Admin@1234',
    'port': 22,}

with ConnectHandler(**h3c_device_01) as h3c_ssh:
    output = h3c_ssh.send_command('display vlan brief')   
print(output)
print(type(output))

with open('20250506-netmiko-H3C-sendcommand&Textfsm.template') as template_file:
    template = TextFSM(template_file)
    demo_output = template.ParseText(output)
print(demo_output)

for each in demo_output:
    print(each[0],each[1])



