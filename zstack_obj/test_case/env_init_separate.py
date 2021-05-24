from zstack_obj.base_api import env_start, cli_start

host_1 = '172.24.248.155'
l3_pub_ip_range = ['172.24.244.210','172.24.244.219','172.24.0.1','255.255.0.0']
l3_man_ip_range = ['192.150.20.2','192.150.20.20','192.150.20.1','255.255.255.0']
physicalInterface = 'eth0'
physicalInterface1 = 'eth1'

if __name__ == '__main__':
    env_start.login_linux(host_1)
    env_start.login_admin()

    zone = cli_start.CreateZone(name ='ZONE-1')   # 创建区域
    cluster = cli_start.CreateCluster(name ='Cluster-1', zone_uuid = zone.uuid)    #创建集群
    host = cli_start.AddKVMHost(host_ip=host_1, clusterUuid=cluster.uuid)  # 添加物理机
    imagestorage = cli_start.AddImageStoreBackupStorage(hostname = host_1, zone_uuid=zone.uuid)   # 添加镜像服务器
    cli_start.AddLocalPrimaryStorage(name ='BS-1', zoneUuid = zone.uuid, clusterUuid = cluster.uuid)   # 添加主存储
    cli_start.AddImage(name='django', url = None, backupStorageUuids=imagestorage.uuid)  # 镜像
    cli_start.AddImage_vr(backupStorageUuids=imagestorage.uuid)  # vr镜像
    cli_start.AddImage_slb_vr(backupStorageUuids=imagestorage.uuid)  # slb镜像
    instanceoffing = cli_start.CreateInstanceOffering(name ='InstanceOffering')   #计算规格

    l2_man = cli_start.CreateL2NoVlanNetwork(name='l2_man', physicalInterface=physicalInterface1, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_pub = cli_start.CreateL2NoVlanNetwork(name='l2_pub', physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2501 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2501', vlan=2501, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2502 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2502', vlan=2502, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2503 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2503', vlan=2503, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2504 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2504', vlan=2504, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    # l2_vlan_2505 = start_job.CreateL2VlanNetwork(name='l2_vlan_2505', vlan=2505, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络

    l3_man = cli_start.CreateL3Network_pub(name='l3_man', l2NetworkUuid=l2_man.uuid, ip_range=l3_man_ip_range,category='man')
    l3_pub = cli_start.CreateL3Network_pub(name='l3_pub', l2NetworkUuid=l2_pub.uuid, ip_range=l3_pub_ip_range)
    l3_flat_1 = cli_start.CreateL3Network_flat(name='l3_flat_1', l2NetworkUuid=l2_vlan_2501.uuid, networkCidr='192.161.1.0/28')
    l3_flat_2 = cli_start.CreateL3Network_flat(name='l3_flat_2', l2NetworkUuid=l2_vlan_2502.uuid, networkCidr='192.161.2.0/28')
    l3_vpc_1 = cli_start.CreateL3Network_vpc(name='l3_vpc_1', l2NetworkUuid=l2_vlan_2503.uuid, networkCidr='192.161.3.0/28')
    l3_vpc_2 = cli_start.CreateL3Network_vpc(name='l3_vpc_2', l2NetworkUuid=l2_vlan_2504.uuid, networkCidr='192.161.4.0/28')
    env_start.logout()