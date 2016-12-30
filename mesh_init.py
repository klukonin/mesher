

import ipaddress
from getpass import getpass
from time import sleep
import paramiko
from scp import SCPClient
from sys import exit



host_list = ['192.168.1.119', '192.168.1.118', '192.168.1.117', '192.168.1.116']
#Нужно тут ормально обрабатывать кортэж как результат ввода. Пока захардкожено



# Глобальные переменные и параметры для подключения по SSH
node = paramiko.SSHClient()
node.load_system_host_keys()
node.set_missing_host_key_policy(paramiko.AutoAddPolicy())



# Глобальные значения вместо uci. Будут использованы позже
# К ним нужно прибавлять в кавычках конактом значения. Сами значения ОБЯЗАТЕЛЬНО должны быть в ординарных кавычках
# Например wifi_power_2_Ghz + "'18'" выставляет значение 18дБм
network_restart = '/etc/init.d/network restart'
wifi_commit = 'uci commit wireless'
wifi_power_2_Ghz = 'uci set wireless.radio0.txpower='
wifi_channel_2_Ghz = 'uci set wireless.channel='
wifi_power_5_Ghz = 'uci set wireless.radio1.txpower='
wifi_channel_5_Ghz = 'uci set wireless.channel='


# Это типа переменная с дефолтным конфигом для беспроводной части в виде uci команд
# Нахуяривается при сбросе
default_wireless_config = '''
uci set wireless.radio0=wifi-device
uci set wireless.radio0.type='mac80211'
uci set wireless.radio0.path='platform/ar933x_wmac'
uci set wireless.radio0.htmode='HT20'
uci set wireless.radio0.hwmode='11ng'
uci set wireless.radio0.require_mode='n'
uci set wireless.radio0.country='RU'
uci set wireless.radio0.disabled='0'
uci set wireless.radio0.ht_capab='SHORT-GI-20 SHORT-GI-40 RX-STBC1'
uci set wireless.radio0.log_level='1'
uci set wireless.radio0.channel='13'
uci set wireless.radio0.txpower='18'
uci set wireless.radio0.basic_rate='24000 28900  57800 72200'
uci set wireless.radio0.supported_rates='24000 26000 28900 36000 39000 43300 48000 52000 54000 57800 58500 65000 72200'
uci set wireless.@wifi-iface[0]=wifi-iface
uci set wireless.@wifi-iface[0].device='radio0'
uci set wireless.@wifi-iface[0].ifname='ap0'
uci set wireless.@wifi-iface[0].network='lan'
uci set wireless.@wifi-iface[0].mode='ap'
uci set wireless.@wifi-iface[0].ssid='IDECO_mesh'
uci set wireless.@wifi-iface[0].encryption='psk2'
uci set wireless.@wifi-iface[0].key='youmeshmytralala'
uci set wireless.@wifi-iface[0].wmm='1'
uci set wireless.@wifi-iface[0].ieee80211w='0'
uci set wireless.@wifi-iface[0].maxassoc='40'
uci set wireless.@wifi-iface[0].disassoc_low_ack='1'
uci set wireless.@wifi-iface[0].basic_rate='26000 28900'
uci set wireless.@wifi-iface[0].supported_rates='26000 28900 39000 43300 52000 57800 58500 65000 72200'
uci set wireless.@wifi-iface[0].mcast_rate='24000'
uci set wireless.@wifi-iface[1]=wifi-iface
uci set wireless.@wifi-iface[1].device='radio0'
uci set wireless.@wifi-iface[1].ifname='mesh0'
uci set wireless.@wifi-iface[1].macaddr='C0:4A:00:9F:C9:FF'
uci set wireless.@wifi-iface[1].network='batnet'
uci set wireless.@wifi-iface[1].mode='adhoc'
uci set wireless.@wifi-iface[1].ssid='BatMesh'
uci set wireless.@wifi-iface[1].encryption='psk2'
uci set wireless.@wifi-iface[1].key='testmesh'
uci set wireless.@wifi-iface[1].ieee80211w='1'
uci set wireless.@wifi-iface[1].mcast_rate='11000'
'''
new_config = ''''''

user = input('Admin Login:')
passwd = getpass()


def deployment_upload() -> str:
    for host in host_list :
        if ipaddress.ip_address(host).is_multicast == False :
            node.load_system_host_keys()
            node.connect(hostname = host,
                         username = user,
                         password = passwd,
                         timeout = 10 )
            node.exec_command( wifi_power_2_Ghz + "'18'" )
            node.exec_command( new_config )
            node.exec_command( wifi_commit )
            print ('Нахуярили конфиг в ноду  ' + host)
            node.close()
    print('Все конфиги нахуярены. Начинаем применять')

def deployment_enable() -> str:
    for host in host_list :
        if ipaddress.ip_address(host).is_multicast == False :
            node.load_system_host_keys()
            node.connect(hostname = host,
                         username = user,
                         password = passwd,
                         timeout = 10 )
            node.exec_command( network_restart )
            print ('Применен конфиг к ноде ноде  ' + host)
            node.close()
            sleep(10)
    print('Все конфиги применили. Возрадуемся')

def file_upload() -> str:
    for host in host_list :
        if ipaddress.ip_address(host).is_multicast == False:
            node.load_system_host_keys()
            node.connect(hostname=host,
                         username=user,
                         password=passwd)
            scp = SCPClient(node.get_transport())
            scp.put('/home/klukonin/TEST/TEST','/tmp/TEST')
            print('Файл записан на ноду  ' + host)
            scp.close()
            sleep(2)
    print('Все файлы записаны')


deployment_upload()
deployment_enable()
file_upload()
exit(0)
