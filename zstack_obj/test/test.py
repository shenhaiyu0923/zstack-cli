from zstack_obj.base_api import env_start, cli_start,ctl_start

host_1 = '172.24.228.204'
l3_pub_ip_range = ['172.24.244.90','172.24.244.99','172.24.0.1','255.255.0.0']
physicalInterface = 'eth0'
if __name__ == '__main__':
    env_start.login_linux(host_1)
    # url = "http://172.20.198.234/mirror/zstack_4.0.0_c76/520/ZStack-enterprise-installer-4.0-2103050914-520.bin"
    # ctl_start.get_zstack_bin(url)
    # ctl_start.zstack_install()
    # cmd = 'wget http://172.20.198.234/mirror/zstack_4.0.0_c76/520/ZStack-enterprise-installer-4.0-2103050914-520.bin'
    #
    #
    cmd = 'ls'
    env_start.local_shell(cmd)
    env_start.login_admin()

    # env_start.local_shell('python a.py')

