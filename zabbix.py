from zabbix_api import ZabbixAPI

# 创建 Zabbix API 连接
zapi = ZabbixAPI("http://10.200.37.6:8080/api_jsonrpc.php")
zapi.login("Admin", "zabbix")

# 获取主机的 ID
host_id = zapi.host.get(filter={"host": ["10.155.28.12"]},output=['hostid'])[0]["hostid"]

# 获取主机的所有接口
interfaces = zapi.hostinterface.get(hostids=host_id)

# 打印接口信息
for interface in interfaces:
    print(interface)