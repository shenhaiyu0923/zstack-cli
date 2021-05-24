from zstack_obj.base_api import env_start, cli_start

host_1 = '172.24.244.50'

physicalInterface = 'eth0'
physicalInterface1 = 'eth1'

if __name__ == '__main__':
    env_start.login_linux(host_1)

