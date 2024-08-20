import platform
import subprocess
import time
import win32evtlogutil as win
import win32evtlog


# пинг IP адресов
def ping_ip(ip_address):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, str(1), ip_address]
        return subprocess.run(command, stdout=subprocess.PIPE).returncode == 0
    except subprocess.CalledProcessError:
        return False

# в виде словаря вписать IP адреса как на примере
server_ip_address = {'8.8.8.8': 0}

# проверка IP адресов на то, не отвечают ли они два раза
def need_to_log(key):
    return server_ip_address[key] == 2

# запуск программы
def start():
    while True:
        pin = list(filter(need_to_log, server_ip_address.keys()))
        for key in server_ip_address:
            ping_out = ping_ip(key)
            print(ping_out)
            if ping_out:
                server_ip_address[key] = 0
            # добавляется единица в словаре к IP сервера если первый раз не пингуется
            elif not ping_out and server_ip_address[key] < 1:
                server_ip_address[key] += 1
            elif len(pin) == 2: # репорт что сервер не пингуется второй раз
                win.ReportEvent('pingIP', 10112, eventType=win32evtlog.EVENTLOG_WARNING_TYPE, strings=f'Сервера не пингуются!')

        time.sleep(300)

start()

