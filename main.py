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
    except subprocess.CalledProcessError as e:
        return False

# в виде словаря вписать IP адреса
server_ip_address = {'8.8.8.8': 0}


# запуск программы
def start():
    while True:
        for key in server_ip_address:
            ping_out = ping_ip(key)
            print(ping_out)
            if ping_out:
                server_ip_address[key] = 0
            # добавляется единица в словаре к IP сервера если первый раз не пингуется
            elif not ping_out and server_ip_address[key] < 1:
                server_ip_address[key] += 1
            else: # репорт что сервер не пингуется второй раз
                win.ReportEvent('pingIP', 10112, eventType=win32evtlog.EVENTLOG_WARNING_TYPE, strings=f'Сервер {key} не пингуется!')
        time.sleep(300)

start()
