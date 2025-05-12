from netmiko import ConnectHandler
from getpass import getpass

# H3C设备连接信息
h3c_device = {
    'device_type': 'hp_comware',
    'host': '192.168.1.1',  # 替换为你的H3C交换机IP
    'username': 'admin',    # 替换为你的登录用户名
    'password': getpass(), # 运行时会提示输入密码
    'secret': '',         # 初始留空，如果需要提权，netmiko会自动处理
}

# 提权密码 (如果与登录密码不同)
# 如果登录后直接是管理员权限，或者提权命令不需要额外密码，可以将此设置为空字符串或与登录密码相同
privilege_password = getpass(prompt='Enter privilege mode password: ') # 运行时会提示输入提权密码

print(f"Connecting to device {h3c_device['host']}...")
try:
    # 建立SSH连接
    net_connect = ConnectHandler(**h3c_device)

    # 检查是否已经是特权模式
    # H3C的特权模式提示符通常是尖括号，例如 <H3C>
    # 用户模式提示符通常是方括号，例如 [H3C]
    # Netmiko的 `check_enable_mode()` 对Comware可能不完美，我们手动检查
    
    prompt = net_connect.find_prompt()
    print(f"Initial prompt: {prompt}")

    if '[' in prompt: # 假设方括号表示用户模式
        print("Attempting to enter privilege mode...")
        # 对于H3C，通常使用 'super' 命令进入特权模式（system-view）
        # netmiko的enable()方法会尝试通用命令，可能不适用于所有H3C配置
        # 我们可以直接发送 'super' 命令，然后处理密码提示
        
        # net_connect.enable() # 使用netmiko的enable方法，它会尝试发送 'enable' 命令
        # 对于H3C，更常见的提权命令是 'super' 或者直接进入 'system-view'
        # 如果 'super' 需要密码，netmiko的 enable() 应该能处理，前提是 secret 参数已设置
        # 如果 'super' 不需要密码，或者密码与登录密码相同，enable() 也能工作
        
        # 尝试使用 netmiko 的 enable() 方法，它会使用 h3c_device 中的 'secret'
        # 如果 'secret' 为空，它可能会提示输入
        # 为了更明确地控制，我们可以先设置 secret
        if not h3c_device.get('secret') and privilege_password:
            h3c_device['secret'] = privilege_password
            # 重新连接或更新连接对象的 secret (如果支持)
            # 对于初次连接后提权，通常在 ConnectHandler 时提供 secret
            # 如果 ConnectHandler 时没有提供 secret，enable() 会尝试
            # 如果 enable() 失败，可以尝试手动发送命令

        # 确保 secret 参数被 enable() 方法使用
        net_connect.secret = privilege_password if privilege_password else h3c_device['password']
        
        try:
            net_connect.enable() # enable() 会尝试发送 'super' 或 'enable' 并提供 secret
            prompt_after_enable = net_connect.find_prompt()
            print(f"Prompt after attempting enable: {prompt_after_enable}")
            if '[' not in prompt_after_enable: # 假设进入特权模式后提示符不再包含方括号
                 print("Successfully entered privilege mode.")
            else:
                print("Failed to enter privilege mode with enable(). Trying 'system-view'...")
                # 如果enable()不工作，尝试直接发送 system-view
                # H3C的 system-view 通常不需要额外密码，如果需要，则上述逻辑需要调整
                output = net_connect.send_command("system-view", expect_string=r"\]|>", strip_prompt=False, strip_command=False)
                print(f"Output of 'system-view':\n{output}")
                prompt_after_system_view = net_connect.find_prompt()
                print(f"Prompt after 'system-view': {prompt_after_system_view}")
                if ']' not in prompt_after_system_view and '[' in prompt_after_system_view: # [H3C] 变为 [H3C-system]
                    print("Successfully entered system-view (privilege mode).")
                elif '<' in prompt_after_system_view: # 或者直接变为 <H3C>
                     print("Successfully entered system-view (privilege mode).")
                else:
                    print("Failed to enter system-view or already in a different mode.")
        except Exception as e_enable:
            print(f"Error during enable or system-view: {e_enable}")
            print("Could not enter privilege mode.")

    elif '<' in prompt:
        print("Already in privilege mode.")
    else:
        print(f"Unrecognized prompt: {prompt}. Assuming privilege mode or unable to determine.")

    # 在这里可以执行需要管理员权限的命令
    # 例如: output = net_connect.send_command('display current-configuration')
    # print(output)

    # 断开SSH连接
    net_connect.disconnect()
    print(f"Disconnected from {h3c_device['host']}.")

except Exception as e:
    print(f"An error occurred: {e}")