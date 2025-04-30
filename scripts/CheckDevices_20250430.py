import traceback
from multiprocessing import Pool
import pandas as pd
from netmiko import ConnectHandler

# 各device_type对应的巡检项
INFO_COLLECT_INFOS = {
    'huawei': [{'name': 'version',
                'cmd': 'display version',
                'textfsm_file': 'huawei_version.textfsm'},
               {'name': 'interface_brief',
                'cmd': 'display interface brief',
                'textfsm_file': 'huawei_interface_brief.textfsm'}
               ],
    'cisco_ios': [{'name': 'version',
                   'cmd': 'show version',
                   'textfsm_file': 'ciso_ios_version.textfsm'}],
    'h3c': [{'name': 'version',
                 'cmd': 'display version',
                 'textfsm_file': 'h3c_version.textfsm'},
                {'name': 'interface_brief',
                 'cmd': 'display interface brief',
                 'textfsm_file': 'h3c_interface_brief.textfsm'}
                ],
}

def get_batch_collect_dev_infos(filename='inventory.xlsx'):
    '''
    读取 Excel 表格，加载登录网络设备的基本信息
    :param filename: 表格名称，默认值是 inventory.xlsx
    :return: 设备登录信息（字典）列表
    '''
    df = pd.read_excel(filename)
    devs = df.to_dict(orient='records')
    return devs

def network_device_info_collect(dev):
    """
    登录网络设备并执行命令，解析出格式化数据，并将其写入指定表格
    :param dev: 设备的基础信息，字典类型，key 与创建Netmiko连接所需的参数对应
    :return: None 不返回，只打印
    """
    try:
        with ConnectHandler(**dev) as conn:
            # 通过设备的device_type匹配巡检的相关信息
            collections = INFO_COLLECT_INFOS[dev['device_type']]
            # 创建表格writer，用于持续写入数据
            writer = pd.ExcelWriter('{}.xlsx'.format(dev['host']),
                                    engine='openpyxl')

            # 循环采集解析并写入数据
            for collection in collections:
                # 获取命令和巡检项名称、解析模板
                cmd = collection['cmd']
                name = collection['name']
                textfsm_file = collection['textfsm_file']

                # 采集并解析
                data = conn.send_command(command_string=cmd,
                                         use_textfsm=True,
                                         textfsm_template=textfsm_file)
                # 判断data数据类型，如果是列表，那么代表解析成功
                if isinstance(data, list):
                    # 构建DataFrame数据
                    df = pd.DataFrame(data)
                    # 将数据写入指定的页签
                    df.to_excel(writer, sheet_name=name, index=False)
                    print('{}的{}巡检项巡检成功'.format(dev['host'], name))
                else:
                    print('{}的{}巡检项内容为空，请确认解析模板无误'.format(
                           dev['host'], name))
            # 调用writer的close方法，关闭并保存表格文件
            writer.close()

    except:
        print('{}的巡检出现异常，请联系开发人员,错误堆栈如下：\n{}'.format(
              dev['host'], traceback.format_exc()))

def batch_info_collect(inventory_file='inventory.xlsx'):
    print("----批量信息巡检开始----")

    # 创建进程池，进程数不宜过大，可以设置为CPU数量的整数倍
    pool = Pool(4)
    # 读取设备信息
    dev_infos = get_batch_collect_dev_infos(inventory_file)
    # 循环读取设备信息，放入进程池中并行执行
    for dev_info in dev_infos:
        # 使用非阻塞的方法，并发执行函数，每次传入不同的参数，开启若干个进程
        pool.apply_async(network_device_info_collect, args=(dev_info,))
    # 关闭进程池，不再接收新的请求
    pool.close()
    # 阻塞主进程，等待进程池的所有子进程完成，再继续执行接下来的代码
    pool.join()
    print('----全部任务执行完成----')

if __name__ == '__main__':
    batch_info_collect()