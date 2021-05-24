from zstack_obj.base_api import env_start


def CreateZone(name = None):
    zone = env_start.cli('CreateZone name={}'.format(name))
    return zone

def CreateCluster(name = None, zone_uuid = None):
    cluster = env_start.cli('CreateCluster name={} zoneUuid={} hypervisorType=KVM'.format(name, zone_uuid))
    return cluster

def AddKVMHost(host_ip = None, clusterUuid = None):
    managementIp = host_ip
    name = host_ip
    clusterUuid = clusterUuid
    host = env_start.cli('AddKVMHost managementIp={} username=root password=password name={} sshPort=22 clusterUuid={}'.format(managementIp, name, clusterUuid))
    return host

def AddImageStoreBackupStorage(hostname = None, zone_uuid = None, ImageStoreBackupStorage = None):
    hostname = hostname
    name = hostname
    if ImageStoreBackupStorage is None:
        ImageStoreBackupStorage = 'ImageStoreBackupStorage'
    else:
        ImageStoreBackupStorage = ImageStoreBackupStorage
    imagestorage = env_start.cli('AddImageStoreBackupStorage hostname={} name={} username=root password=password sshPort=22 url=/cloud_bs type={}'.format(hostname, name, ImageStoreBackupStorage))
    def AttachBackupStorageToZone():
        ims_uuid = imagestorage.uuid
        ims_to_zone = env_start.cli('AttachBackupStorageToZone backupStorageUuid={} zoneUuid={}'.format(ims_uuid, zone_uuid))
    AttachBackupStorageToZone()
    return imagestorage

def AddLocalPrimaryStorage(name = None, zoneUuid = None, clusterUuid = None):
    ps = env_start.cli('AddLocalPrimaryStorage name={} url=/cloud_ps zoneUuid={}'.format(name, zoneUuid))
    def AttachPrimaryStorageToCluster():
        ps_uuid = ps.uuid
        env_start.cli('AttachPrimaryStorageToCluster primaryStorageUuid={} clusterUuid={}'.format(ps_uuid, clusterUuid))
    AttachPrimaryStorageToCluster()
    return ps

def AddImage(name = None, url = None, backupStorageUuids = None):
    if url == None:
        url = 'http://172.20.1.27/mirror/diskimages/django.qcow2'
    image = env_start.cli('AddImage name={} url={} mediaType=RootVolumeTemplate system=false format=qcow2 platform=Linux backupStorageUuids={}'.format(name, url, backupStorageUuids))
    return image

def AddImage_vr(name = "vr", url = None, backupStorageUuids = None):
    if url == None:
        url = 'http://storage.zstack.io/mirror/vyos117_linux_4.0.0/latest/zstack-vrouter.qcow2'
    image = env_start.cli('AddImage name={} url={} mediaType=RootVolumeTemplate architecture=x86_64 system=true format=qcow2 platform=Linux backupStorageUuids={} systemTags="applianceType::vrouter"'.format(name, url, backupStorageUuids))
    return image

def AddImage_slb_vr(name = "slb_vr", url = None, backupStorageUuids = None):
    if url == None:
        url = 'http://storage.zstack.io/mirror/vyos117_linux_4.0.0/latest/zstack-vrouter.qcow2'
    image = env_start.cli('AddImage name={} url={} mediaType=RootVolumeTemplate architecture=x86_64 system=true format=qcow2 platform=Linux backupStorageUuids={} systemTags="applianceType::SLB"'.format(name, url, backupStorageUuids))
    return image


def CreateInstanceOffering(name = None,):
    InstanceOffering = env_start.cli('CreateInstanceOffering name={} cpuNum=1 memorySize=314572800 allocatorStrategy=LeastVmPreferredHostAllocatorStrategy'.format(name))
    return InstanceOffering

def CreateL2NoVlanNetwork(name = None, physicalInterface = None, zoneUuid = None, clusterUuid = None):
    l2_pub = env_start.cli('CreateL2NoVlanNetwork name={} type=L2NoVlanNetwork physicalInterface={} zoneUuid={}'.format(name, physicalInterface, zoneUuid))
    def AttachL2NetworkToCluster():
        l2NetworkUuid = l2_pub.uuid
        env_start.cli('AttachL2NetworkToCluster l2NetworkUuid={} clusterUuid={}'.format(l2NetworkUuid, clusterUuid))
    AttachL2NetworkToCluster()
    return l2_pub

def CreateL2VlanNetwork(name = None, vlan = None, physicalInterface = None, zoneUuid = None, clusterUuid = None):
    l2_vlan = env_start.cli('CreateL2VlanNetwork name={} vlan={} type=L2NoVlanNetwork physicalInterface={} zoneUuid={}'.format(name, vlan, physicalInterface, zoneUuid))
    def AttachL2NetworkToCluster():
        l2NetworkUuid = l2_vlan.uuid
        env_start.cli('AttachL2NetworkToCluster l2NetworkUuid={} clusterUuid={}'.format(l2NetworkUuid, clusterUuid))
    AttachL2NetworkToCluster()
    return l2_vlan

def QueryNetworkServiceProvider():
    global l3_server_dict
    l3_server_dict = {}

    l3_server = env_start.cli('QueryNetworkServiceProvider')
    for i in l3_server:
        if i['type'] == 'SecurityGroup':
            # 'networkServiceTypes': ['SecurityGroup']
            SecurityGroup_uuid = i['uuid']
            l3_server_dict['SecurityGroup_uuid'] = SecurityGroup_uuid
        if i['type'] == 'Flat':
            # 'networkServiceTypes': ['VipQos', 'DNS', 'HostRoute', 'Userdata', 'Eip', 'DHCP']
            Flat_uuid = i['uuid']
            l3_server_dict['Flat_uuid'] = Flat_uuid
        if i['type'] == 'VirtualRouter':
            # 'networkServiceTypes': ['DNS', 'SNAT', 'LoadBalancer', 'PortForwarding', 'Eip', 'DHCP']
            VirtualRouter_uuid = i['uuid']
            l3_server_dict['VirtualRouter_uuid'] = VirtualRouter_uuid
        if i['type'] == 'vrouter':
            # 'networkServiceTypes': ['IPsec', 'VRouterRoute', 'CentralizedDNS', 'VipQos', 'DNS', 'SNAT', 'LoadBalancer', 'PortForwarding', 'Eip', 'DHCP']
            vrouter_uuid = i['uuid']
            l3_server_dict['vrouter_uuid'] = vrouter_uuid
    return l3_server_dict

def CreateL3Network_flat(name = None, l2NetworkUuid = None, networkCidr = None,):

    l3_flat = env_start.cli('CreateL3Network name={} l2NetworkUuid={} category=Private type=L3BasicNetwork'.format(name, l2NetworkUuid, ))
    def AddIpRangeByNetworkCidr(name = l3_flat.name, l3NetworkUuid = l3_flat.uuid):
        env_start.cli('AddIpRangeByNetworkCidr name={} networkCidr={} l3NetworkUuid={}'.format(name, networkCidr, l3NetworkUuid))
    def AddDnsToL3Network(l3NetworkUuid = l3_flat.uuid):
        env_start.cli('AddDnsToL3Network dns=223.5.5.5 l3NetworkUuid={}'.format(l3NetworkUuid))
    def AttachNetworkServiceToL3Network(l3NetworkUuid = l3_flat.uuid):
        l3_server_dict = QueryNetworkServiceProvider()
        l3_service_sg = "{'%s': ['SecurityGroup',]}" % l3_server_dict['SecurityGroup_uuid']
        l3_service_ft = "{'%s': ['VipQos', 'DNS', 'HostRoute', 'Userdata', 'Eip', 'DHCP']}"% l3_server_dict['Flat_uuid']
        l3_service_vrouter = "{'%s': ['LoadBalancer',]}"% l3_server_dict['vrouter_uuid']
        env_start.cli('''AttachNetworkServiceToL3Network l3NetworkUuid={} networkServices="{}"'''.format(l3NetworkUuid, l3_service_sg))
        env_start.cli('''AttachNetworkServiceToL3Network l3NetworkUuid={} networkServices="{}"'''.format(l3NetworkUuid, l3_service_ft))
        env_start.cli('''AttachNetworkServiceToL3Network l3NetworkUuid={} networkServices="{}"'''.format(l3NetworkUuid, l3_service_vrouter))
    AddIpRangeByNetworkCidr()
    AddDnsToL3Network()
    AttachNetworkServiceToL3Network()
    return l3_flat

def CreateL3Network_vpc(name = None, l2NetworkUuid = None, networkCidr = None,):

    l3_vpc = env_start.cli('CreateL3Network name={} l2NetworkUuid={} category=Private type=L3VpcNetwork'.format(name, l2NetworkUuid, ))
    def AddIpRangeByNetworkCidr(name = l3_vpc.name, l3NetworkUuid = l3_vpc.uuid):
        env_start.cli('AddIpRangeByNetworkCidr name={} networkCidr={} l3NetworkUuid={}'.format(name, networkCidr, l3NetworkUuid))
    def AddDnsToL3Network(l3NetworkUuid = l3_vpc.uuid):
        env_start.cli('AddDnsToL3Network dns=223.5.5.5 l3NetworkUuid={}'.format(l3NetworkUuid))
    def AttachNetworkServiceToL3Network(l3NetworkUuid = l3_vpc.uuid):
        l3_server_list = QueryNetworkServiceProvider()
        l3_service_sg = "{'%s': ['SecurityGroup',]}" % l3_server_dict['SecurityGroup_uuid']
        l3_service_ft = "{'%s': ['Userdata', 'DHCP']}"% l3_server_dict['Flat_uuid']
        l3_service_vrouter = "{'%s': ['IPsec','VRouterRoute','CentralizedDNS','VipQos','DNS','SNAT','LoadBalancer','PortForwarding','Eip']}"% l3_server_dict['vrouter_uuid']
        env_start.cli('''AttachNetworkServiceToL3Network l3NetworkUuid={} networkServices="{}"'''.format(l3NetworkUuid, l3_service_sg))
        env_start.cli('''AttachNetworkServiceToL3Network l3NetworkUuid={} networkServices="{}"'''.format(l3NetworkUuid, l3_service_ft))
        env_start.cli('''AttachNetworkServiceToL3Network l3NetworkUuid={} networkServices="{}"'''.format(l3NetworkUuid, l3_service_vrouter))
    AddIpRangeByNetworkCidr()
    AddDnsToL3Network()
    AttachNetworkServiceToL3Network()
    return l3_vpc

def CreateL3Network_pub(name = None, l2NetworkUuid = None, ip_range = None, category = None,):
    if category :
        category = 'System system=true'
    else:
        category = 'Public'
    l3_pub = env_start.cli('CreateL3Network name={} l2NetworkUuid={} category={} type=L3BasicNetwork'.format(name, l2NetworkUuid, category))
    # def AddIpRangeByNetworkCidr(name = l3_pub.name, l3NetworkUuid = l3_pub.uuid):
    #     env_start.cli('AddIpRangeByNetworkCidr name={} networkCidr={} l3NetworkUuid={}'.format(name, networkCidr, l3NetworkUuid))
    def AddIpRange():
        env_start.cli('AddIpRange name={} l3NetworkUuid={} startIp={} endIp={} gateway={} netmask={}'.format(name, l3_pub.uuid, ip_range[0], ip_range[1], ip_range[2], ip_range[3]))
    def AddDnsToL3Network(l3NetworkUuid = l3_pub.uuid):
        env_start.cli('AddDnsToL3Network dns=223.5.5.5 l3NetworkUuid={}'.format(l3NetworkUuid))
    def AttachNetworkServiceToL3Network(l3NetworkUuid = l3_pub.uuid):
        l3_server_dict = QueryNetworkServiceProvider()
        l3_service_sg = "{'%s': ['SecurityGroup',]}" % l3_server_dict['SecurityGroup_uuid']
        l3_service_ft = "{'%s': ['Userdata', 'DHCP','HostRoute']}"% l3_server_dict['Flat_uuid']
        env_start.cli('''AttachNetworkServiceToL3Network l3NetworkUuid={} networkServices="{}"'''.format(l3NetworkUuid, l3_service_sg))
        env_start.cli('''AttachNetworkServiceToL3Network l3NetworkUuid={} networkServices="{}"'''.format(l3NetworkUuid, l3_service_ft))
    # AddIpRangeByNetworkCidr()
    AddIpRange()
    AddDnsToL3Network()
    AttachNetworkServiceToL3Network()
    return l3_pub

def ReloadLicense():
    ReloadLicense = env_start.cli('ReloadLicense')
    return ReloadLicense


