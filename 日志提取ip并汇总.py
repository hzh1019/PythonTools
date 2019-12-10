#服务器日志保存在数据库内，从数据库读取日志并将日志内的ip提取汇总后降序输出，便于快速发现可疑设备

import pyodbc 
import re
from collections import Counter

server = '192.168.0.1,1433' 
database = 'DbName' 
username = 'user' 
password = 'pass' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

#列表去重并统计次数，以字典形式返回
def get_count_by_counter(l):    
    count=Counter(l)    
    count_dict=dict(count)
    return count_dict

#Ip识别正则表达式
p1 =  r'(?:(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])'

iplistAll=[]
cursor = cnxn.cursor()
cursor.execute("select server,logMessage FROM LogDetails;") 
row = cursor.fetchone() 
while row: 
    # 提取ip
    iplist = re.findall(p1,row[1])              
    # 将ip合并至汇总列表
    iplistAll+=iplist    
    row = cursor.fetchone()
# 汇总列表去重并汇总
dest = get_count_by_counter(iplistAll)
#字典排序，降序
destList = sorted(dest.items(),key=lambda x:x[1],reverse=True)
print(destList)
