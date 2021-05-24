import time
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.dirname(current_dir)
timestamp = time.time()
time_local = time.localtime(timestamp)
dt = time.strftime("%Y-%m-%d-%H-%M-%S",time_local)

def obj_print(*args,):
    file_log = '{}\log\{}.log'.format(str(parent_path),dt)
    f = open(file_log, 'a+')
    print(*args, file = f)
    print(*args)
    f.close()

# # 此函数数据结构有点问题没处理
# def obj_print1(*args,):
#     file = 'C:\project\zstack_cli\zstack_obj\log\{}.log'.format(dt)
#     print(file)
#     with open(file,'a+') as f:
#         [f.write(str(arg)) for arg in args]
#         print(*args)
