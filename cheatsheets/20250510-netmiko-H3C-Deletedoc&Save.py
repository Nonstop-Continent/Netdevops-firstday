'''
实验目的：
（1）用netmiko将Switch-2（11.0.0.2）目录flash:/下的text.txt文件删除。
（2）用netmiko在Switch-2(（11.0.0.2）上执行save保存配置操作。
'''
import netmiko
from netmiko import ConnectHandler,file_transfer

Switch2 = {
    'device_type': 'hp_comware',
    'host': '11.0.0.2',
    'username': 'netops',
    'password': 'Admin@1234',
    'port': 22,
}
with ConnectHandler(**Switch2) as connect:
    print("已经成功登录交换机"+Switch2['host'])

    output = connect.send_command(command_string="delete flash:/text.txt",
                  expect_string=r"Delete flash:/text.txt?",
                  strip_prompt=False,
                  strip_command=False)
    output += connect.send_command(command_string="y",
                  expect_string=r">",
                  strip_prompt=False,
                  strip_command=False)
    
    print(output)

   