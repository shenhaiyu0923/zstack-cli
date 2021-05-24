from zstack_obj.base_api import env_start
import time


def clear_license():
    env_start.ctl('zstack-ctl clear_license')

def get_lincense_longtime(license_requests):
    clear_license()
    cmd1 = "curl http://172.20.12.1:7000/getTempLargeLicense -X POST -d customer_name=ZStack -d user_name=jian.wang@zstack.io -d unit_num=500 -d license_type=prepaid -d duration=2 -d unit_type=CPU -d vmware=20 -d baremetal=20 -d arm64=20 -d project-management=20 -d disaster-recovery=20 -d v2v=20 -d elastic-baremetal=20 -d hybrid=20 -d hybrid -d request_key="
    cmd = cmd1+license_requests
    file_path = env_start.local_shell(cmd)
    file_name = file_path.replace('"','').split('/')[-1]
    cmd_wget = "wget {}".format(file_path.replace('"',''))
    env_start.local_shell(cmd_wget)
    time.sleep(2)
    return file_name

def get_lincense_shorttime(license_requests):
    clear_license()
    cmd1 = 'curl http://172.20.12.1:7000/getLicense -X POST -d customer_name=ZStack -d user_name=jian.wang@zstack.io -d unit_num=20 -d license_type=prepaid -d duration=30 -d unit_type=CPU -d vmware=20 -d baremetal=20 -d arm64=20 -d project-management=20 -d disaster-recovery=20 -d v2v=20 -d elastic-baremetal=20 -d hybrid=20 -d hybrid -d request_key='
    cmd = cmd1+license_requests
    file_path = env_start.local_shell(cmd)
    file_name = file_path.replace('"','').split('/')[-1]
    cmd_wget = "wget {}".format(file_path.replace('"',''))
    env_start.local_shell(cmd_wget)
    time.sleep(2)
    return file_name

def license_install(file):
    ret = env_start.ctl('zstack-ctl install_license --license {}'.format(file))
    return ret

def get_zstack_bin(url):
    cmd = 'zstack-ctl stop'
    cmd2 = 'rm -rf /usr/local/zstack*'
    cmd3 = 'wget {}'.format(url)
    env_start.local_shell(cmd)
    env_start.local_shell(cmd2)
    env_start.local_shell(cmd3)

def zstack_install(file):
    cmd = 'bash {} -D'.format(file)
    env_start.local_shell(cmd)



