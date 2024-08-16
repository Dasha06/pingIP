import platform
import subprocess
import time


# пинг IP адресов
def ping_ip(ip_address):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, str(1), ip_address]
        return subprocess.run(command, stdout=subprocess.PIPE).returncode == 0
    except subprocess.CalledProcessError as e:
        return False


server_ip_address = {'8.8.8.8': 0}


# запуск программы
def start():
    while True:
        for key in server_ip_address:
            ping_out = ping_ip(key)
            print(ping_out)
            if ping_out:
                pass
            elif not ping_out and server_ip_address[key] < 2:
                server_ip_address[key] += 1
            else:
                pass
        time.sleep(300)
