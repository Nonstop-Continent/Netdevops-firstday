'''
实验目的：
（1）用netmiko将Switch-2（11.0.0.2）目录flash:/下的text.txt文件删除。
（2）用netmiko在Switch-2(（11.0.0.2）上执行save保存配置操作。
'''
import netmiko
from netmiko import ConnectHandler,file_transfer

Switch1 = {
    'device_type': 'hp_comware',
    'host': '11.0.0.2',
    'username': 'netops',
    'password': 'Admin@1234',
    'port': 22,
}
with ConnectHandler(**Switch1) as connect:
    print("已经成功登录交换机"+Switch1['host'])

    output = connect.send_command(command_string="delete flash:/text.txt",
                  expect_string=r"Delete flash:/text.txt?",
                  strip_prompt=False,
                  strip_command=False)
    output += connect.send_command(command_string="y",
                  expect_string=r">",
                  strip_prompt=False,
                  strip_command=False)
    print(output)
'''
通过ConnectHandler()登录Switch1后，前后两次调用send_command()函数，
在第一个send_command()函数中通过command_string这个参数向Switch1输入命令del flash0:/test.txt，
然后在expect_string这个参数里告知Netmiko去Switch1的回显内容里查找“Delete flash:/text.txt?”这段系统返回的提示命令，
如果查到了的话，则继续输入命令y（第二个send_command()）让脚本删除test.txt这个文件，
之后如果接收到命令提示符">"，则继续执行脚本后面的代码。
strip_prompt和strip_command两个参数这里放Fasle就行，目的是让代码最后的print(output)输出的内容的格式更好看一点：
''' 
    

   