'''
（1）利用Jinja2模板，制作Switch-1的vty登录限制脚本，用ACL方式。
（2）用netmiko登录Switch-1（11.0.0.1），执行（1）脚本并回显。
（3）实验目的效果预期：
可登录Switch-1
    PC电脑WIN10（11.0.0.254）
    Layer3Switch-2（11.0.0.2）
不可登录Switch-1
    Switch-3（11.0.0.3）
    Switch-4（11.0.0.4）
（4）Layer3Switch-5（11.0.0.5），无相关配置，看一下什么效果
'''

import netmiko
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader

allow_ip = ['11.0.0.2', '11.0.0.254']
disallow_ip = ['11.0.0.3', '11.0.0.4']

sw1 = {'device_type':'hp-comware',
      'ip':'11.0.0.1',
      'username':'netops',
      'password':'Admin@1234'}

loader = FileSystemLoader('20250509-netmiko-H3C-Jinja2-templates')
environment = Environment(loader=loader)
tpl = environment.get_template('acl.conf.tpl')
out = tpl.render(allow_ip=allow_ip, disallow_ip=disallow_ip, interface='vty 0 4')

with open("configuration.conf", "w") as f:
       f.write(out)

with ConnectHandler(**sw1) as conn:
        print ("已经成功登陆交换机" + sw1['ip'])
        output = conn.send_config_from_file("configuration.conf")
        print (output)



