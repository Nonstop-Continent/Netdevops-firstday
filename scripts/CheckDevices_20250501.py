import traceback
from multiprocessing import Pool
import pandas as pd
from netmiko import ConnectHandler

# 各device_type对应设备是否进入enable模式
ENABLE_INFOS = {
    'huawei': False, 'cisco_ios': True, 'cisco_asa': False
}

def get_batch_config_dev_infos(filename='config_inventory.xlsx'):
    '''
    读取Excel表格，加载登录网络设备的基本信息
    :param filename: 表格名称，默认值是 inventory.xlsx
    :return: 设备登录信息（字典）列表
    '''
    df = pd.read_excel(filename)
    # 将表格中未填写的单元格全部用None代替
    df = df.replace({pd.NA: None})
    devs = df.to_dict(orient='records')
    return devs

def network_device_config(dev):
    """
    登录设备推送配置并保存
    :return: None 不返回，只打印
    """
    # 重新给session_log参数赋值，与设备IP关联
    session_log = '{}-session. log'.format(dev['host'])
    dev['session_log'] = session_log
    try:
        with ConnectHandler(**dev) as conn:
            print('{}的配置推送开始'.format(dev['host']))
            # 根据device_type判断是否进行提权操作
            enable = ENABLE_INFOS.get(dev['device_type'], False)
            if enable:
                conn.enable()
            # 获取配置下发文件并推送到网络设备保存配置
            config_file = '{}.config'.format(dev['host'])
            conn.send_config_from_file(config_file=config_file)
            conn.save_config()
            print('{host}的配置推送结束，详见{session_log}'.format(
                   host=dev['host']), session_log=session_log)
    except:
        print('{}的配置推送出现异常，请联系开发人员,错误堆栈如下：\n{}'.format(
              dev['host'], traceback.format_exc()))

def batch_config(config_inventory_file='config_inventory.xlsx'):
    print("----批量配置推送开始----")

    # 创建进程池，进程数不宜过大，可以设置为CPU数量的整数倍
    pool = Pool(4)
    # 读取设备信息
    dev_infos = get_batch_config_dev_infos(config_inventory_file)
    # 循环读取设备信息，放入进程池进行并行执行
    for dev_info in dev_infos:
        # 使用非阻塞的方法，并发执行函数，每次传入不同的参数，开启若干个进程
        pool.apply_async(network_device_config, args=(dev_info,))
    # 关闭进程池，不再接收新的请求
    pool.close()
    # 阻塞主进程，等待进程池的所有子进程完成，再继续执行接下来的代码
    pool.join()
    print('----全部任务执行完成----')

if __name__ == '__main__':
    batch_config()