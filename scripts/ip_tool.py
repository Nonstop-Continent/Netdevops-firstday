# import argparse # 保留导入，但不再直接使用其解析功能
from netaddr import IPAddress, IPNetwork, NOHOST, spanning_cidr, AddrFormatError
from netaddr import core # 导入 core 模块

def validate_ip(ip_str):
    """验证 IP 地址是否合法"""
    try:
        ip = IPAddress(ip_str)
        print(f"'{ip_str}' 是一个合法的 {ip.version} 地址.")
        return True
    except AddrFormatError:
        print(f"错误: '{ip_str}' 不是一个合法的 IP 地址格式。")
        return False
    except Exception as e:
        print(f"验证 '{ip_str}' 时发生未知错误: {e}")
        return False

def get_network_info(network_str):
    """获取并显示网络信息"""
    try:
        ip_network = IPNetwork(network_str)
        print(f"网络: {ip_network}")
        print(f"  - 网络地址: {ip_network.network}")
        print(f"  - 掩码: {ip_network.netmask}")
        print(f"  - 掩码长度: /{ip_network.prefixlen}")
        if ip_network.version == 4:
            print(f"  - 广播地址: {ip_network.broadcast}")
            print(f"  - 总地址数: {ip_network.size}")
            # 注意: .first 和 .last 返回整数表示
            print(f"  - 第一个地址 (整数): {ip_network.first}")
            print(f"  - 最后一个地址 (整数): {ip_network.last}")
            # 获取可用主机范围 (排除网络和广播地址)
            if ip_network.prefixlen < 31: # /31 和 /32 没有传统意义上的可用主机
                 host_range = list(ip_network.iter_hosts())
                 if host_range:
                     print(f"  - 可用主机范围: {host_range[0]} - {host_range[-1]}")
                     print(f"  - 可用主机数: {len(host_range)}")
                 else:
                     print("  - 可用主机范围: 无 (网络太小)")
            else:
                 print("  - 可用主机范围: 无 (点对点或单个地址)")

        else: # IPv6
             print(f"  - 总地址数: {ip_network.size}")
             # IPv6 通常不计算广播地址和传统意义的主机范围

    except (AddrFormatError, ValueError) as e: # 使用 ValueError 替代 NetmaskValueError
        print(f"错误: '{network_str}' 不是一个合法的网络表示: {e}")
    except Exception as e:
        print(f"获取网络 '{network_str}' 信息时发生未知错误: {e}")

def list_hosts(network_str, max_hosts=None):
    """列出网络中的主机地址"""
    try:
        ip_network = IPNetwork(network_str)
        print(f"网络 '{network_str}' 中的主机地址:")
        count = 0
        # iter_hosts() 会自动排除网络地址和广播地址 (对于IPv4)
        for i, host in enumerate(ip_network.iter_hosts()):
            if max_hosts is not None and i >= max_hosts:
                print(f"... (超过最大显示数量 {max_hosts})")
                break
            print(f"  - {host}")
            count += 1
        if count == 0:
             print("  - (此网络没有可用的主机地址)")

    except (AddrFormatError, ValueError) as e: # 使用 ValueError 替代 NetmaskValueError
        print(f"错误: '{network_str}' 不是一个合法的网络表示: {e}")
    except Exception as e:
        print(f"列出网络 '{network_str}' 主机时发生未知错误: {e}")

def check_containment(item1_str, item2_str):
    """检查 IP 或网络是否包含在另一个网络中"""
    try:
        item1 = IPNetwork(item1_str) if '/' in item1_str else IPAddress(item1_str)
        item2 = IPNetwork(item2_str) # 第二个参数必须是网络

        if item1 in item2:
            print(f"'{item1_str}' 包含在网络 '{item2_str}' 中。")
        else:
            print(f"'{item1_str}' 不包含在网络 '{item2_str}' 中。")

    except (AddrFormatError, ValueError) as e: # 使用 ValueError 替代 NetmaskValueError
        print(f"错误: 输入的 IP 或网络格式不合法: {e}")
    except Exception as e:
        print(f"检查包含关系时发生未知错误: {e}")

def create_subnets(network_str, prefixlen, count=None):
    """将网络划分子网"""
    try:
        ip_network = IPNetwork(network_str)
        print(f"将网络 '{network_str}' 划分为 /{prefixlen} 的子网:")

        subnets_generator = ip_network.subnet(prefixlen=prefixlen, count=count)

        subnet_list = list(subnets_generator) # 将生成器转换为列表以便打印

        if not subnet_list:
             print("  - 无法生成子网 (可能是目标前缀长度不合适)")
             return

        for i, subnet in enumerate(subnet_list):
            print(f"  - {subnet}")
            if count is not None and i + 1 == count:
                break # 如果指定了数量，达到后停止

    except (AddrFormatError, ValueError) as e: # 使用 ValueError 替代 NetmaskValueError
        print(f"错误: '{network_str}' 不是一个合法的网络表示: {e}")
    # 由于前面已经捕获了 ValueError，这里不需要重复捕获
        print(f"错误: 无法划分子网: {e}")
    except Exception as e:
        print(f"划分子网时发生未知错误: {e}")

def merge_items(items_str_list):
    """合并 IP 地址和网络"""
    try:
        items = []
        for item_str in items_str_list:
            # 尝试解析为 IPNetwork 或 IPAddress
            try:
                items.append(IPNetwork(item_str))
            except (AddrFormatError, ValueError): # 使用 ValueError 替代 NetmaskValueError
                try:
                    items.append(IPAddress(item_str))
                except AddrFormatError:
                    print(f"警告: 跳过无法解析的项目 '{item_str}'")

        if not items:
            print("错误: 没有提供有效的 IP 地址或网络进行合并。")
            return

        print(f"合并以下项目: {', '.join(map(str, items))}")
        merged_network = spanning_cidr(items)
        print(f"合并后的网络: {merged_network}")

    except Exception as e:
        print(f"合并项目时发生未知错误: {e}")


def display_menu():
    """显示操作菜单"""
    print("\n--- IP 地址管理工具 ---")
    print("请选择操作:")
    print("1. 验证 IP 地址")
    print("2. 获取网络信息")
    print("3. 列出网络中的主机地址")
    print("4. 检查 IP/子网 是否包含在网络中")
    print("5. 划分子网")
    print("6. 合并 IP/网络")
    print("0. 退出")
    print("-----------------------")

def main():
    """主交互循环"""
    while True:
        display_menu()
        choice = input("请输入选项编号: ")

        if choice == '1':
            ip_str = input("请输入要验证的 IP 地址: ")
            validate_ip(ip_str)
        elif choice == '2':
            network_str = input("请输入网络地址 (例如 192.168.1.0/24): ")
            get_network_info(network_str)
        elif choice == '3':
            network_str = input("请输入网络地址 (例如 192.168.1.0/24): ")
            max_hosts_str = input("最多显示多少个主机? (直接回车表示显示全部): ")
            max_hosts = None
            if max_hosts_str.isdigit():
                max_hosts = int(max_hosts_str)
            list_hosts(network_str, max_hosts)
        elif choice == '4':
            item_str = input("请输入要检查的 IP 或子网 (例如 192.168.1.5 或 192.168.1.0/25): ")
            network_str = input("请输入包含的网络 (例如 192.168.1.0/24): ")
            check_containment(item_str, network_str)
        elif choice == '5':
            network_str = input("请输入要划分的网络 (例如 192.168.0.0/16): ")
            prefixlen_str = input("请输入目标子网的掩码长度 (例如 24): ")
            count_str = input("要生成多少个子网? (直接回车表示生成所有可能的子网): ")
            try:
                prefixlen = int(prefixlen_str)
                count = None
                if count_str.isdigit():
                    count = int(count_str)
                create_subnets(network_str, prefixlen, count)
            except ValueError:
                print("错误: 掩码长度必须是数字。")
        elif choice == '6':
            items_input = input("请输入要合并的 IP 或网络列表 (用空格分隔): ")
            items_str_list = items_input.split()
            merge_items(items_str_list)
        elif choice == '0':
            print("正在退出工具...")
            break
        else:
            print("无效的选项，请重新输入。")

        input("\n按 Enter 键继续...") # 暂停，等待用户按回车

if __name__ == "__main__":
    main()