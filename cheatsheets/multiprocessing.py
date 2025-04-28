def batch_backup(inventory_file='inventory.xlsx'):
    print("----批量配置备份开始----")

    # 创建进程池，进程数不宜过大，可以设置为CPU数量的整数倍
    pool = Pool(4)
    # 读取设备信息列表
    dev_infos = get_batch_backup_dev_infos(inventory_file)
    # 循环读取设备信息，放入进程池进行并行执行
    for dev_info in dev_infos:
        # 使用非阻塞的方法，并发执行函数，每次传入不同的参数，开启若干个进程
        pool.apply_async(network_device_backup, args=(dev_info,))
    # 关闭进程池，不再接收新的请求
    pool.close()
    # 阻塞主进程，等待进程池的所有子进程完成，再执行后续代码
    pool.join()
    print('----全部任务执行完成----')

'''
multiprocessing是Python内置的标准模块，用于实现多进程功能。
代码清单使用了multiprocessing模块的Pool类来创建多进程的资源池（进程池）​。
循环读取设备信息的部分代码不变，在调用单台设备配置备份时，使用了进程池对象pool的apply_async方法。
它可以创建出多个子进程来执行指定的函数，从而实现多进程的并发功能。apply_async方法具有两个参数

• func：被调用的函数，由于是第一个参数，所以此处省略了参数名，直接按位置赋值为函数network_device_backup。
• args：被调用函数的参数，以列表或者元组方式按顺序传入多个参数，此处代码中使用了元组形式，并传入了设备登录信息。

多进程版本使用multiprocessing模块的Pool类创建了进程池，通过for循环创建多个子进程，并发执行get_batch_backup_dev_infos函数。
在创建完众多子进程后，执行进程池对象pool的close方法和join方法，实现进程池的关闭和主进程的阻塞
'''