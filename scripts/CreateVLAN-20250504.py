# 导入 Netmiko 相关模块，用于连接和配置网络设备
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException

def netmiko_connect(hostname, username, password, device_type='cisco_ios'):
    """
    使用 Netmiko 连接到网络设备。
    
    参数:
        hostname (str): 设备的 IP 地址或主机名
        username (str): 登录用户名
        password (str): 登录密码
        device_type (str): 设备类型，默认为 'cisco_ios'

    返回:
        net_connect: Netmiko 连接对象，若连接失败则返回 None
    """
    # 定义设备连接参数字典
    device = {
        'device_type': device_type,
        'host': hostname,
        'username': username,
        'password': password,
    }
    try:
        # 建立 SSH 连接
        net_connect = ConnectHandler(**device)
        return net_connect
    except NetMikoAuthenticationException:
        print("认证失败，请检查用户名和密码。")
    except NetMikoTimeoutException:
        print("连接超时，请检查交换机的网络连接。")
    except Exception as e:
        print(f"出现错误: {e}")

def create_vlan(net_connect, vlan_id, vlan_name):
    """
    在已连接的设备上创建 VLAN。

    参数:
        net_connect: Netmiko 连接对象
        vlan_id (int/str): 要创建的 VLAN ID
        vlan_name (str): VLAN 的名称

    返回:
        str: 执行命令的输出结果，如果出错则返回 None
    """
    try:
        # 构造 VLAN 创建命令序列
        commands = [
            'configure terminal',
            f'vlan {vlan_id}',
            f'name {vlan_name}',
            'end',
            'write memory'
        ]
        # 发送配置命令并获取输出
        output = net_connect.send_config_set(commands)
        return output
    except Exception as e:
        print(f"创建VLAN时出错: {e}")


# 示例用法
hostname = '192.168.1.1'  # 网络设备的 IP 地址
username = 'admin'        # 登录用户名
password = 'password'     # 登录密码
vlan_id = 10              # 要创建的 VLAN ID
vlan_name = 'Test_VLAN'   # VLAN 名称

# 建立设备连接
net_connect = netmiko_connect(hostname, username, password)

# 如果连接成功，则执行 VLAN 创建逻辑
if net_connect:
    output = create_vlan(net_connect, vlan_id, vlan_name)
    if output:
        print("VLAN创建成功")
        print(output)
    # 断开连接
    net_connect.disconnect()