#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
网络设备配置备份程序
支持思科、华为、华三、锐捷和aruba的路由器、交换机、防火墙及无线产品
"""

import os
import sys
import time
import traceback
import pandas as pd
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

# 各设备类型对应的配置备份命令模板
BACKUP_CMDS = {
    # 思科设备
    'cisco_ios': 'show running-config',
    'cisco_xe': 'show running-config',
    'cisco_xr': 'show running-config',
    'cisco_nxos': 'show running-config',
    'cisco_asa': 'show running-config',
    'cisco_wlc': 'show run-config',
    
    # 华为设备
    'huawei': 'display current-configuration',
    'huawei_vrpv8': 'display current-configuration',
    
    # 华三设备
    'hp_comware': 'display current-configuration',
    'hp_procurve': 'show running-config',
    
    # 锐捷设备
    'ruijie_os': 'show running-config',
    
    # Aruba设备
    'aruba_os': 'show running-config',
    'aruba_osswitch': 'show running-config',
}

# 备份结果统计
BACKUP_STATS = {
    'total': 0,
    'success': 0,
    'failed': 0,
    'failed_devices': []
}

# 备份输出目录
BACKUP_DIR = 'backup_configs'

def validate_template():
    """
    验证配置模板是否可用
    :return: 布尔值，表示模板是否有效
    """
    if not BACKUP_CMDS:
        print("错误: 配置模板为空，请检查BACKUP_CMDS字典")
        return False
    
    print("配置模板验证成功，当前支持以下设备类型:")
    for device_type in BACKUP_CMDS.keys():
        print(f"  - {device_type}: {BACKUP_CMDS[device_type]}")
    
    return True

def add_device_template(device_type, command):
    """
    添加新的设备类型模板
    :param device_type: 设备类型
    :param command: 备份命令
    :return: None
    """
    if device_type in BACKUP_CMDS:
        print(f"警告: 设备类型 '{device_type}' 已存在，将被覆盖")
    
    BACKUP_CMDS[device_type] = command
    print(f"成功添加设备类型 '{device_type}' 的备份命令: '{command}'")

def load_device_inventory(filename):
    """
    读取设备清单文件
    :param filename: 设备清单文件名(xlsx或csv)
    :return: 设备信息列表
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(filename):
            print(f"错误: 设备清单文件 '{filename}' 不存在")
            return None
        
        # 根据文件扩展名决定读取方式
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext == '.xlsx':
            df = pd.read_excel(filename)
        elif file_ext == '.csv':
            df = pd.read_csv(filename)
        else:
            print(f"错误: 不支持的文件格式 '{file_ext}'，请使用.xlsx或.csv文件")
            return None
        
        # 检查必要的列是否存在
        required_columns = ['device_type', 'host', 'username', 'password']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"错误: 设备清单缺少必要的列: {', '.join(missing_columns)}")
            return None
        
        # 检查设备类型是否在支持列表中
        unsupported_types = set(df['device_type']) - set(BACKUP_CMDS.keys())
        if unsupported_types:
            print(f"警告: 发现不支持的设备类型: {', '.join(unsupported_types)}")
            print("这些设备将被跳过，请检查设备类型是否正确或添加相应的模板")
        
        # 转换为字典列表
        devices = df.to_dict(orient='records')
        print(f"成功加载设备清单，共 {len(devices)} 台设备")
        return devices
    
    except Exception as e:
        print(f"加载设备清单时出错: {str(e)}")
        print(traceback.format_exc())
        return None

def backup_device(device):
    """
    备份单个设备的配置
    :param device: 设备信息字典
    :return: 布尔值，表示备份是否成功
    """
    host = device.get('host', 'unknown')
    device_name = device.get('device_name', host)
    device_type = device.get('device_type')
    
    # 更新统计信息
    BACKUP_STATS['total'] += 1
    
    # 检查设备类型是否支持
    if device_type not in BACKUP_CMDS:
        print(f"跳过设备 {device_name} ({host}): 不支持的设备类型 '{device_type}'")
        BACKUP_STATS['failed'] += 1
        BACKUP_STATS['failed_devices'].append({
            'host': host,
            'device_name': device_name,
            'reason': f"不支持的设备类型: {device_type}"
        })
        return False
    
    print(f"正在备份设备 {device_name} ({host})...")
    
    try:
        # 连接设备
        with ConnectHandler(**device) as conn:
            # 获取备份命令
            cmd = BACKUP_CMDS[device_type]
            # 执行备份命令
            output = conn.send_command(command_string=cmd)
            
            # 确保备份目录存在
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)
            
            # 生成备份文件名
            file_name = f"{BACKUP_DIR}/{device_name}_{host}.txt"
            
            # 写入备份文件
            with open(file_name, mode='w', encoding='utf8') as f:
                f.write(output)
            
            print(f"设备 {device_name} ({host}) 备份成功，配置已保存到 {file_name}")
            BACKUP_STATS['success'] += 1
            return True
            
    except NetMikoTimeoutException:
        error_msg = f"连接超时"
        print(f"设备 {device_name} ({host}) 备份失败: {error_msg}")
        
    except NetMikoAuthenticationException:
        error_msg = f"认证失败，请检查用户名和密码"
        print(f"设备 {device_name} ({host}) 备份失败: {error_msg}")
        
    except Exception as e:
        error_msg = str(e)
        print(f"设备 {device_name} ({host}) 备份失败: {error_msg}")
        print(traceback.format_exc())
    
    # 如果执行到这里，说明备份失败
    BACKUP_STATS['failed'] += 1
    BACKUP_STATS['failed_devices'].append({
        'host': host,
        'device_name': device_name,
        'reason': error_msg
    })
    return False

def batch_backup(inventory_file):
    """
    批量备份设备配置
    :param inventory_file: 设备清单文件
    :return: None
    """
    # 验证配置模板
    if not validate_template():
        return
    
    # 加载设备清单
    devices = load_device_inventory(inventory_file)
    if not devices:
        return
    
    # 重置统计信息
    BACKUP_STATS['total'] = 0
    BACKUP_STATS['success'] = 0
    BACKUP_STATS['failed'] = 0
    BACKUP_STATS['failed_devices'] = []
    
    # 开始备份
    print("\n开始批量备份设备配置...")
    start_time = time.time()
    
    for device in devices:
        backup_device(device)
    
    # 备份完成，打印统计信息
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n备份任务完成!")
    print(f"总计备份设备: {BACKUP_STATS['total']} 台")
    print(f"成功备份: {BACKUP_STATS['success']} 台")
    print(f"备份失败: {BACKUP_STATS['failed']} 台")
    print(f"总耗时: {elapsed_time:.2f} 秒")
    
    # 打印失败设备清单
    if BACKUP_STATS['failed'] > 0:
        print("\n备份失败的设备清单:")
        for i, device in enumerate(BACKUP_STATS['failed_devices'], 1):
            print(f"{i}. {device['device_name']} ({device['host']}): {device['reason']}")

def main():
    """
    主函数
    """
    print("=" * 60)
    print("网络设备配置备份程序")
    print("支持思科、华为、华三、锐捷和aruba的网络设备")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        inventory_file = sys.argv[1]
    else:
        # 默认使用inventory.xlsx
        inventory_file = "inventory.xlsx"
        print(f"未指定设备清单文件，将使用默认文件: {inventory_file}")
    
    # 执行批量备份
    batch_backup(inventory_file)

if __name__ == "__main__":
    main()