import threading
import socket
import time
import openpyxl
from openpyxl import Workbook
from tqdm import tqdm

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return True
        else:
            return False
        sock.close()
    except:
        pass

def scan(ip, ports, results):
    for port in tqdm(ports):
        if scan_port(ip, port):
            results.append(port)

def main():
    ip = input("请输入要扫描的IP地址：")
    start_port = int(input("请输入起始端口号："))
    end_port = int(input("请输入结束端口号："))
    ports = range(start_port, end_port+1)
    threads = []
    results = [[] for _ in range(10)]
    for i in range(10):
        t = threading.Thread(target=scan, args=(ip, ports[i::10], results[i]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    results = sum(results, [])
    wb = Workbook()
    ws = wb.active
    ws.append(['开放端口'])
    for port in results:
        ws.append([port])
    wb.save('portscan.xlsx')
    print('扫描完成！')


if __name__ == '__main__':
    main()
