import requests
from fake_useragent import UserAgent
import time
import random
import xlsxwriter

ua = UserAgent()

headers = {
    'User-Agent': ua.random,
    'Referer': 'https://www.toutiao.com/ch/news_hot/',
    'Cookie': 'tt_webid=1234567890123456789; tt_webid=1234567890123456789; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=abcdefghijklmnopqrstuvwxyz012345; csrftoken=abcdefghijklmnopqrstuvwxyz012345; s_v_web_id=abcdefghijklmnopqrstuvwxyz012345',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'www.toutiao.com'
}

from tqdm import tqdm

#模拟翻页，爬取指定页面的信息
def get_hot_news(page_num):
    for i in range(page_num):
        url = f'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1C5B9C9C9F9E5F&cp=5D5C9C5C5C5F5e1&page_num={i}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            news = response.json()['data']
            for item in tqdm(news):
                source_url = item['source_url'].replace('/group', 'https://www.toutiao.com/article')
                yield [item['title'], item['source'], source_url]
                time.sleep(random.randint(1, 3))

import pandas as pd

if __name__ == '__main__':
    news = get_hot_news(7)
    if news:
        data = []
        for item in news:
            data.append(item)
        df = pd.DataFrame(data, columns=['标题', '来源', '链接'])
        writer = pd.ExcelWriter('hot_news.xlsx', engine='xlsxwriter')
        df.to_excel(writer, index=False)

        # Add hyperlink format to the workbook
        workbook = writer.book
        hyperlink_format = workbook.add_format({'font_color': 'blue', 'underline': 1})
        worksheet = writer.sheets['Sheet1']

        # Iterate through the '链接' column and add hyperlinks
        for row_num in range(1, len(df)+1):
            worksheet.write_url(row_num, 2, df.loc[row_num-1, '链接'], hyperlink_format)

        writer.save()
    else:
        print('Failed to get hot news.')

