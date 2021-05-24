import paramiko
import json
from zstack_obj.base_api.obj_print import obj_print as print
import threading
# from pprint import pprint as print
ZSTACK_RESULT_INVENTORY_KEY = "inventory"
ZSTACK_RESULT_INVENTORYS_KEY = "inventories"
ZSTACK_UUID_KEY = "uuid"
ADMIN_PASSWORD ='password'
threading_list=[]

def dict_to_object(dictObj):
    class Dict(dict):
        __setattr__ = dict.__setitem__
        __getattribute__ = dict.__getitem__
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst

def login_linux(ip):
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip,port=22,username="root",password="password")

# cmd = 'cd /root/test; python prj_alarm_test.py'

def run_shell(cmd):

    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode('utf8')
    errput = stderr.read().decode('utf8')
    if errput != '':
        print(errput)
    return output

def local_shell(cmd):

    print('root #'+cmd)
    print()
    res = run_shell(cmd)
    print(res)
    return res

def cli(cli_cmd):
    from zstack_obj.base_api.obj_print import obj_print as print
    print("admin>>>"+ cli_cmd)
    cmd = 'zstack-cli ' + cli_cmd
    if 'query' in cli_cmd.lower():
        ret = run_shell(cmd)
        res_inv = json.loads(ret)[ZSTACK_RESULT_INVENTORYS_KEY]
        print(res_inv)
        print('=' * 300)
        res_inv = dict_to_object(res_inv)
        return res_inv
    else:
        ret = run_shell(cmd)
        if ZSTACK_RESULT_INVENTORY_KEY in ret:
            print(json.loads(ret)[ZSTACK_RESULT_INVENTORY_KEY])
            print('=' * 300)
            ret = json.loads(ret)[ZSTACK_RESULT_INVENTORY_KEY]
            ret = dict_to_object(ret)
            return ret
        else:
            print(ret)
            print('=' * 300)
            ret = dict_to_object(ret)
            return ret

def ctl(ctl_cmd):
    print("root~#  " + ctl_cmd)
    if 'zstack-ctl' not in ctl_cmd:
        cmd = 'zstack-ctl' + ctl_cmd
    else:
        cmd = ctl_cmd
    print("root~#  " + cmd)
    ret = run_shell(cmd)
    print(ret)
    print('=' * 300)
    return ret


def login_admin():
    print('=' * 300)
    #cli('LogInByAccount accountName=admin password=%s systemTags=%s' % (ADMIN_PASSWORD, SYSTEM_TAGS))
    cli('LogInByAccount accountName=admin password=%s' % (ADMIN_PASSWORD))
    print('='*300)

def logout():
    print('=' * 300)
    cli('LogOut')
    ssh.close()

# def create_prj_alarms(i):
#     prj = cli('CreateVip l3NetworkUuid=a1bcac74f74c4f27a968e581f95f1cde name=111-%s' % i)
#
# def cteate_pro_many(num):
#     l = range(1,num+1)
#     for i in l:
#         t = threading.Thread(target=create_prj_alarms, args=(i,))
#         t.start()
#         threading_list.append(t)
#     for t in threading_list:
#         t.join()

def create_vm(i,):
    vm_vpc = test_stub.create_vm(vm_name="vm_vpc_{}".format(i), image_name="image_with_network_tools", l3_name=l3_vpc_name)
    vm_vpc.check()
    test_obj_dict.add_vm(vm_vpc)

def threadinc_create(target,num):
    threading_list=[]
    l = range(1,num+1)
    for i in l:
        t = threading.Thread(target=create_vm, args=(i,))
        t.start()
        threading_list.append(t)
    [t.join() for t in threading_list]