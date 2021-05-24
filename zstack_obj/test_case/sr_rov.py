from zstack_obj.base_api import env_start, cli_start

host_1 = '172.25.15.105'
l3_pub_ip_range = ['172.25.101.32','172.25.101.63','172.25.0.1','255.255.0.0']
physicalInterface = 'zsn0'
if __name__ == '__main__':
    env_start.login_linux(host_1)
    env_start.login_admin()

    zone = cli_start.CreateZone(name ='ZONE-1')   # 创建区域
    cluster = cli_start.CreateCluster(name ='Cluster-1', zone_uuid = zone.uuid)    #创建集群
    host = cli_start.AddKVMHost(host_ip=host_1, clusterUuid=cluster.uuid)  # 添加物理机
    imagestorage = cli_start.AddImageStoreBackupStorage(hostname = host_1, zone_uuid=zone.uuid)   # 添加镜像服务器
    cli_start.AddLocalPrimaryStorage(name ='BS-1', zoneUuid = zone.uuid, clusterUuid = cluster.uuid)   # 添加主存储
    cli_start.AddImage(name='django', url = None, backupStorageUuids=imagestorage.uuid)  # 镜像
    instanceoffing = cli_start.CreateInstanceOffering(name ='InstanceOffering')   #计算规格

    l2_pub = cli_start.CreateL2VlanNetwork(name='l2_pub', vlan=31, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2501 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2501', vlan=2501, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2502 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2502', vlan=2502, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2503 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2503', vlan=2503, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2504 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2504', vlan=2504, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络
    l2_vlan_2505 = cli_start.CreateL2VlanNetwork(name='l2_vlan_2505', vlan=2505, physicalInterface=physicalInterface, zoneUuid = zone.uuid, clusterUuid = cluster.uuid)  # 二层网络

    l3_pub = cli_start.CreateL3Network_pub(name='l3_pub', l2NetworkUuid=l2_pub.uuid, ip_range=l3_pub_ip_range)
    l3_flat_1 = cli_start.CreateL3Network_flat(name='l3_flat_1', l2NetworkUuid=l2_vlan_2501.uuid, networkCidr='192.160.1.0/28')
    l3_flat_2 = cli_start.CreateL3Network_flat(name='l3_flat_2', l2NetworkUuid=l2_vlan_2502.uuid, networkCidr='192.160.2.0/28')
    l3_vpc_1 = cli_start.CreateL3Network_vpc(name='l3_vpc_1', l2NetworkUuid=l2_vlan_2503.uuid, networkCidr='192.160.3.0/28')
    l3_vpc_2 = cli_start.CreateL3Network_vpc(name='l3_vpc_2', l2NetworkUuid=l2_vlan_2504.uuid, networkCidr='192.160.4.0/28')

    env_start.logout()