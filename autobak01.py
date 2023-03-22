import paramiko
import openpyxl
import time
import zipfile
import os

# 读取excel表格中的交换机ip、用户名、密码信息，执行命令将结果打包发送至指定邮箱。
# excel内存在此三列：ip_address,username,password
def read_excel():
    wb = openpyxl.load_workbook('switch_info.xlsx')
    sheet = wb.active
    switch_info = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        switch_info.append(row)
    return switch_info

# 登录交换机并查看当前配置
def get_config(ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=22, username=username, password=password, timeout=3)
    stdin, stdout, stderr = ssh.exec_command('dis cpu-usage')
    config = stdout.read().decode()
    ssh.close()
    return config

# 保存配置到本地txt文件中,文件以ip地址命名，替换ip地址内的.为_
def save_config(ip, config):    
    file_name = f'{ip.replace(".", "_")}.txt'
    with open(file_name, 'w') as f:
        f.write(config)

if __name__ == '__main__':
    switch_info = read_excel()
    for info in switch_info:
        ip, username, password = info
        try:
            config = get_config(ip, username, password)
            save_config(ip, config)
            print(f'{ip}配置已保存')
        except:
            print(f'{ip}连接失败')


print('------------------------')

# 将运行目录下的txt文件打包为zip文件,以日期命名
import datetime
now = datetime.datetime.now()
zip_file_name = now.strftime("%Y-%m-%d_%H-%M-%S") + '.zip'
with zipfile.ZipFile(zip_file_name, 'w') as f:
    for file_name in os.listdir():
        if file_name.endswith('.txt'):
            f.write(file_name)

# 发送邮件
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

msg = MIMEMultipart()
msg['Subject'] = '交换机配置文件'
msg['From'] = 'sender@sss.com'
msg['To'] = 'rec@rec.com'

part = MIMEText('交换机配置文件')
msg.attach(part)

part = MIMEApplication(open(zip_file_name, 'rb').read())
part.add_header('Content-Disposition', 'attachment', filename=zip_file_name)
msg.attach(part)

try:
    smtp = smtplib.SMTP('smtp.xxx.com')
    smtp.login('sender@sss.com', '123456789')
    smtp.sendmail('sender@sss.com', 'rec@rec.com', msg.as_string())
    smtp.quit()
except:
    print(f'发送失败')
# 删除原txt文件
for file_name in os.listdir():
    if file_name.endswith('.txt'):
        os.remove(file_name)


