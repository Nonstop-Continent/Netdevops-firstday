from netaddr import IPAddress
from netaddr import IPNetwork,NOHOST,spanning_cidr

# 1、使用IPAddress类创建IPv4与IPv6地址对象
ipaddr_v4 = IPAddress('192.168.137.200')
print(ipaddr_v4) # 输出 192.168.137.200
ipaddr_v6 = IPAddress('2001:da8:215:3c01::83bb')
print(ipaddr_v6) # 输出 2001:da8:215:3c01::83bb    
#如果给定的IP地址非法，程序在创建对象时会报错。网络工程师可以利用这个特性校验给定的IPv6地址是否合法 


# 2、使用IPNetwork类创建IPv4与IPv6网络对象
ip_network = IPNetwork('192.168.137.0/24')
print(ip_network) # 输出192.168.137.0/24
ip_network = IPNetwork('192.168.137.0/255.255.255.0')
print(ip_network) # 输出192.168.137.0/24

# 如果网络的地址中含有主机，可以将flags赋值为NOHOST（或者4）
ip_network = IPNetwork('192.168.137.100/24',flags=NOHOST)
# 创建的网络对象中就不再包含主机位信息
print(ip_network)# 输出 192.168.137.0/24

ip_network = IPNetwork('192.168.137.1/24')
# 获取网络地址，返回结果是IPAddress对象，根据需要可以强制转为str
ip_network_addr = ip_network.network
print(ip_network_addr, type(ip_network_addr))
# 输出 192.168.137.0 <class 'netaddr.ip.IPAddress'>
# 获取掩码，返回结果是IPAddress对象，根据需要可以强制转为str
ip_network_netmask = ip_network.netmask
print(ip_network_netmask, type(ip_network_netmask))
# 输出 255.255.255.0 <class 'netaddr.ip.IPAddress'>
# 获取掩码长度的表示方法, 输出为整数
ip_network_netmask_length = ip_network.prefixlen
print(ip_network_netmask_length) # 输出 24
# 获取主机地址,返回结果是IPAddress对象，根据需要可以强制转为str
ip_network_host = ip_network.ip
print(ip_network_host, type(ip_network_host))
# 输出 192.168.137.1 <class 'netaddr.ip.IPAddress'>
# 获取网络的第一个地址（整数格式）
first_ip = ip_network.first
print(first_ip) # 输出 3232270592

# 获取网络的最后一个地址（整数格式）
last_ip = ip_network.last
print(last_ip) # 输出 3232270847

# 获取网络的广播地址（IPAddress对象）
broadcast_ip = ip_network.broadcast
print(broadcast_ip) # 输出 192.168.137.255


# 3 网络展开及包含关系计算
ip_network = IPNetwork('192.168.137.0/24')
for host in ip_network:
    print(host, type(host))
# 当地址空间比较小的时候，可以考虑使用list强制转换为列表
ip_network = IPNetwork('192.168.137.0/24')
hosts = list(ip_network)
print(hosts, type(hosts))


# 4 使用in判断网络地址与网络的关系以及网络与网络的关系
ipaddr_1 = IPAddress('192.168.137.1')
ipaddr_2 = IPAddress('192.168.1.1')

ip_network_1 = IPNetwork('192.168.137.0/24')
ip_network_2 = IPNetwork('192.168.0.0/16')

# 判断 192.168.137.1 是否在网络 192.168.137.0/24
addr_in_network = ipaddr_1 in ip_network_1
print(addr_in_network)  # 输出 True

# 判断 192.168.1.1 是否在网络 192.168.137.0/24
addr_in_network = ipaddr_2 in ip_network_1
print(addr_in_network)  # 输出 False

# 判断网络 192.168.137.0/24 是否在网络 192.168.0.0/16
network_in_network = ip_network_1 in ip_network_2
print(network_in_network)  # 输出 True

# 判断网络 192.168.0.0/16 是否在网络 192.168.137.0/24
network_in_network = ip_network_2 in ip_network_1
print(network_in_network)  # 输出 False



# 5 使用subnet方法将掩16的地址空间划分为若干个掩24的子网
ip_network = IPNetwork('192.168.1.0/16')
subnets = ip_network.subnet(prefixlen=24)
# subnets仍是一个生成器，用户可以通过for循环访问，也可以强制转换为列表
print(subnets)  
# 输出 <generator object IPNetwork.subnet at 0x0000027E44531E40>

for subnet in subnets:
    print(subnet, type(subnet))
# 输出内容如下：
# 192.168.0.0/24 <class 'netaddr.ip.IPNetwork'>
# ...
# 192.168.255.0/24 <class 'netaddr.ip.IPNetwork'>


# 只要前三个子网
ip_network = IPNetwork('192.168.1.0/16')

# count赋值为3，只返回前3个子网
subnets = ip_network.subnet(prefixlen=24, count=3)

for subnet in subnets:
    print(subnet, type(subnet))
# 输出内容如下：
# 192.168.0.0/24 <class 'netaddr.ip.IPNetwork'>
# 192.168.1.0/24 <class 'netaddr.ip.IPNetwork'>
# 192.168.2.0/24 <class 'netaddr.ip.IPNetwork'>


# 6 使用netaddr的spanning_cidr函数合并网络和IP地址
ip_network_1 = IPNetwork('192.168.1.0/16')
ip_network_2 = '192.168.2.0/16'
ipaddr = '192.168.3.1'
items = [ip_network_1, ip_network_2, ipaddr]
# 调用spanning_cidr方法，传入要合并的地址和网络的列表
merge_net = spanning_cidr(items)
print(merge_net, type(merge_net))
# 输出 192.168.0.0/22 <class 'netaddr.ip.IPNetwork'>

