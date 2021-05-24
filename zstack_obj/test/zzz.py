# from itertools import izip_longest
from paramiko import SSHClient
from paramiko import AutoAddPolicy


class MySSHClient(SSHClient):

    def run(self, command, callback):
        stdin, stdout, stderr = self.exec_command(
            command, bufsize=1
        )

        stdout_iter = iter(stdout.readline, '')
        stderr_iter = iter(stderr.readline, '')

        for out, err in zip(stdout_iter, stderr_iter):
            if out: callback(out.strip())
            if err: callback(err.strip())

        return stdin, stdout, stderr

def console(text):
    print(text)

ssh = MySSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect("172.24.245.126", 22, "root", "password")
stdin, stdout, stderr = ssh.run("ping www.baidu.com", console)

print(stdout.channel.recv_exit_status())

# import subprocess
# import shlex
#
# def run_command(command):
#     process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
#     while True:
#         output = process.stdout.readline()
#         if output == '' and process.poll() is not None:
#             break
#         if output:
#             print("writing websockets")
#             print(output.strip())
#     rc = process.poll()
#     return rc
#
#
# if __name__ == '__main__':
#     command = """ping www.baidu.com"""
#     run_command(command)

