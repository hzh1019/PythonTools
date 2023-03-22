import threading
import subprocess
import time
import openpyxl

def ping(ip):
    result = subprocess.call('ping -n 1 -w 1000 %s' % ip, stdout=subprocess.PIPE)
    if result == 0:
        return True
    else:
        return False

def ping_range(start_ip, end_ip):
    ips = []
    for i in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1])+1):
        ips.append(start_ip.rsplit('.', 1)[0] + '.' + str(i))
    return ips

def ping_ips(ips):
    results = []
    for ip in ips:
        if ping(ip):
            results.append(ip)
    return results

def ping_ips_with_progress(ips):
    results = []
    for i, ip in enumerate(ips):
        if ping(ip):
            results.append(ip)
        progress = (i+1) / len(ips) * 100
        print('Progress: %.2f%%' % progress)
    return results

def ping_ips_with_threads(ips, num_threads=20):
    results = []
    def ping_ips_thread(ips):
        for ip in ips:
            if ping(ip):
                results.append(ip)
    threads = []
    for i in range(num_threads):
        thread_ips = ips[i::num_threads]
        thread = threading.Thread(target=ping_ips_thread, args=(thread_ips,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return results

def save_results_to_excel(results, filename):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'Ping Results'
    sheet['A1'] = 'IP Address'
    for i, ip in enumerate(results):
        sheet.cell(row=i+2, column=1, value=ip)
    wb.save(filename)

if __name__ == '__main__':
    start_ip = '192.168.1.1'
    end_ip = '192.168.1.60'
    ips = ping_range(start_ip, end_ip)
    #指定线程数
    results = ping_ips_with_threads(ips, num_threads=20)
    save_results_to_excel(results, 'ping_results.xlsx')
