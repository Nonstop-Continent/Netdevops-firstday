import traceback
#这行代码的目的是将 Python 内置的 traceback 模块导入到当前的脚本中。
#traceback 模块的主要功能是提供一种标准的方式来提取、格式化和打印 Python 程序的堆栈跟踪信息（stack traces）
import pandas as pd
from netmiko import ConnectHandler
from pathlib import Path
import re


# .resolve() 可以获取更规范的绝对路径（处理 '..' 和符号链接）
script_dir = Path(__file__).parent.resolve()
print(f"脚本所在目录 (绝对路径): {script_dir}")

# 2. 获取父目录
#parent_dir = script_dir.parent
#print(f"脚本所在目录的父目录 (绝对路径): {parent_dir}")

# 如果文件就在脚本旁边
sibling_file_path = script_dir / 'inventory.xlsx'
print(f"同级文件路径: {sibling_file_path}")


# 检查文件是否存在
if sibling_file_path.is_file():
    print("文件存在")
    # 读取 Excel 文件 (示例)
    # df = pd.read_excel(inventory_path)
    # print(df.head())
    pass # 在这里添加实际的文件读取逻辑

else:
    print(f"错误：在路径 {sibling_file_path} 未找到文件。")


# 各device_type对应的显示配置命令
Show_config_cmd = {
    'cisco_ios': 'show running-config',
    'cisco_nxos': 'show running-config',
    'cisco_xr': 'show running-config',
    'cisco_asa': 'show running-config',
    'hp_comware': 'display current-configuration', # H3C/HP Comware
    'h3c': 'display current-configuration',        # H3C
    'huawei': 'display current-configuration',     # Huawei VRPv5/VRPv8
    'huawei_vrp': 'display current-configuration', # Huawei VRPv5
    'huawei_vrpv8': 'display current-configuration',# Huawei VRPv8
    'juniper_junos': 'show configuration | display set', # Juniper Junos
    'linux': 'cat /etc/network/interfaces' # Example for Linux
}

# 各device_type对应的保存配置命令 (用于确保配置已保存到启动配置)
Save_config_cmd = {
    'cisco_ios': 'write memory', # 或者 copy running-config startup-config
    'cisco_nxos': 'copy running-config startup-config',
    'cisco_xr': 'commit', # XR 通常需要 commit
    'cisco_asa': 'write memory',
    'hp_comware': 'save force', # H3C/HP Comware, force 避免交互
    'h3c': 'save force',        # H3C, force 避免交互
    'huawei': 'save',           # Huawei VRPv5/VRPv8 - 需要处理交互
    'huawei_vrp': 'save',       # Huawei VRPv5 - 需要处理交互
    'huawei_vrpv8': 'save',     # Huawei VRPv8 - 需要处理交互
    'juniper_junos': 'commit', # Juniper Junos
    'linux': 'echo "Save command not applicable for Linux config file"' # Linux 通常不需要特定保存命令
}


def get_batch_backup_dev_infos(filename='inventory.xlsx'):
  
    #读取Excel表格,加载登录网络设备的基本信息
    #:参数 filename: Excel表格文件名,默认为inventory.xlsx
    #:返回值: 返回一个字典，字典的键为设备名，值为字典，字典的值为登录设备所需的基本信息

    df = pd.read_excel(sibling_file_path)
    devs = df.to_dict(orient='records')

    #使用to_dict()方法将Pandas DataFrame转换为字典,orient='records'参数指定将每行转换为独立字典，最终形成列表
    #列名作为字典键，对应行的值作为字典值

    return devs

def network_device_backup(dev):
    """
    登录设备，获取当前配置并写入文件，然后执行保存配置命令。
    对于华为设备，会处理 'save' 命令的 [Y/N] 确认提示。

    :param dev: 网络设备的基本信息,字典类型,key与创建Netmiko连接所需的参数对应
    :return: 无返回值，只打印状态信息
    """
    host = dev.get('host', '未知设备')
    device_type = dev.get('device_type', '未知类型')
    conn = None # 初始化 conn 为 None

    try:
        print(f"开始处理设备: {host} ({device_type})")
        conn = ConnectHandler(**dev)

        # 1. 获取配置
        show_cmd = Show_config_cmd.get(device_type)
        if not show_cmd:
            print(f"错误：未找到设备类型 '{device_type}' 的显示配置命令。跳过 {host}。")
            return # 跳过此设备

        print(f"{host}: 正在执行 '{show_cmd}' 获取配置...")
        config_output = conn.send_command(show_cmd, read_timeout=120) # 增加超时以防配置过长

        # 2. 写入文件
        file_name = f"{host}.txt" # 使用 f-string 简化
        # 注意：这里假设脚本目录是期望的备份目录。如果需要不同目录，需调整 backup_path
        backup_path = script_dir / file_name # 将备份文件放在脚本同目录下
        print(f"{host}: 正在将配置写入文件: {backup_path}")
        with open(backup_path, mode='w', encoding='utf8') as f:
            f.write(config_output)
        print(f"{host}: 配置已成功备份到 {backup_path}")

        # 3. 保存配置
        save_cmd = Save_config_cmd.get(device_type)
        if not save_cmd:
            print(f"警告：未找到设备类型 '{device_type}' 的保存命令。跳过保存步骤。")
            return # 完成备份，但跳过保存

        print(f"{host}: 正在执行保存命令 '{save_cmd}'...")

        if device_type in ['huawei', 'huawei_vrp', 'huawei_vrpv8'] and save_cmd == 'save':
            # 特别处理华为的 'save' 命令交互
            # 发送 save 命令，并期待 [Y/N] 提示
            # 使用正则表达式匹配，忽略大小写，并允许提示前后有其他字符
            # 增加超时时间以防万一
            output_save_prompt = "" # 初始化为空字符串
            try:
                output_save_prompt = conn.send_command(
                    command_string=save_cmd,
                    expect_string=r'(Are you sure|confirm).*\s*\[Y/N\]', # 更精确匹配
                    strip_prompt=False, # 保留提示符以便调试
                    strip_command=False, # 保留命令本身以便调试
                    read_timeout=60
                )
                print(f"{host}: 'save' 命令输出 (等待确认): \n---\n{output_save_prompt}\n---")
            except Exception as save_prompt_e:
                 # 如果在等待 [Y/N] 时超时或出错 (例如配置无变化直接保存成功)
                 print(f"{host}: 等待 'save' 命令的 [Y/N] 确认提示时发生异常或超时: {save_prompt_e}")
                 # 尝试读取缓冲区看是否有成功信息
                 output_save_prompt = conn.read_channel()
                 print(f"{host}: 读取缓冲区内容: \n---\n{output_save_prompt}\n---")


            # 检查是否真的出现了确认提示 (在捕获的输出或异常后的读取中)
            # 使用 re.search 进行不区分大小写的匹配
            if re.search(r'\[Y/N\]', output_save_prompt, re.IGNORECASE):
                print(f"{host}: 检测到确认提示，发送 'Y'...")
                # 发送 'Y' 并等待最终的设备提示符 (通常是 > 或 # 或 ])
                try:
                    output_save_confirm = conn.send_command(
                        command_string='Y',
                        expect_string=r'[>#\]]', # 匹配常见的结束提示符
                        strip_prompt=False,
                        strip_command=False,
                        read_timeout=60
                    )
                    print(f"{host}: 'Y' 确认后输出: \n---\n{output_save_confirm}\n---")
                    print(f"{host}: 配置保存命令已发送并确认。")
                except Exception as confirm_e:
                    print(f"{host}: 发送 'Y' 确认时发生异常或超时: {confirm_e}")
                    # 即使确认失败，也可能已经保存，记录错误但继续
            else:
                # 如果没有出现 [Y/N]，可能配置没有更改，或者设备行为不同
                print(f"{host}: 'save' 命令执行后未检测到预期的 [Y/N] 确认提示。")
                # 检查输出中是否包含成功信息
                if "successfully" in output_save_prompt.lower() or "configuration is saved" in output_save_prompt.lower() or "Configuration has been saved" in output_save_prompt:
                     print(f"{host}: 输出中检测到成功信息，认为保存已完成。")
                else:
                     print(f"{host}: 未检测到成功信息，请检查设备状态。可能无需保存或设备行为不同。")


        elif save_cmd != 'echo "Save command not applicable for Linux config file"':
            # 对于其他设备或不需要交互的命令 (如 'save force', 'commit', 'write memory')
            try:
                output_save = conn.send_command(save_cmd, read_timeout=120) # 给commit等命令更长时间
                print(f"{host}: '{save_cmd}' 命令输出: \n---\n{output_save}\n---")
                print(f"{host}: 配置保存命令 '{save_cmd}' 已执行。")
            except Exception as other_save_e:
                print(f"{host}: 执行保存命令 '{save_cmd}' 时发生异常: {other_save_e}")
                print(traceback.format_exc())
        else:
            # 对于 Linux 的占位符命令
            print(f"{host}: {save_cmd}") # 打印信息性消息

    except Exception as e: # 捕获更具体的异常或所有异常
        print(f"错误：处理设备 {host} ({device_type}) 时发生异常:")
        print(traceback.format_exc()) # 打印完整的错误堆栈

    finally:
        if conn and conn.is_alive(): # 检查连接是否仍然存活
            try:
                conn.disconnect()
                print(f"{host}: 连接已关闭。")
            except Exception as e:
                print(f"错误：关闭 {host} 连接时发生异常: {e}")
        elif conn:
             print(f"{host}: 连接似乎已断开，无需显式关闭。")
        print("-" * 30) # 添加分隔符


def batch_backup(inventory_file='inventory.xlsx'):
    """
    读取表格中的网络设备进行批量配置备份和保存。
    :param inventory_file: 网络设备基本信息表格文件名,默认为inventory.xlsx
    :return: 无返回值，只打印
    """
    #通过函数获取设备列表
    devs = get_batch_backup_dev_infos(inventory_file)
    for dev in devs:
        network_device_backup(dev)
    print('所有设备的配置备份和保存尝试完成！') # 修改完成消息

if __name__ == '__main__':
    batch_backup()

