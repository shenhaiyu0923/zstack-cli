from zstack_obj.base_api import env_start
from zstack_obj.base_api import cli_start
from zstack_obj.base_api import ctl_start
host_1 = '172.24.194.246'
physicalInterface = 'eth0'
if __name__ == '__main__':
    env_start.login_linux(host_1)
    env_start.login_admin()
    request_license = cli_start.ReloadLicense().licenseRequest
    license_name = ctl_start.get_lincense_shorttime(request_license)
    ctl_start.license_install(license_name)
    # ctl_start.clear_license()
    cli_start.ReloadLicense()
