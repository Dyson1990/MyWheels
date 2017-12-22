# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: requests_manager.py
    @time: 2017/10/13 9:49
--------------------------------
"""
import sys
import os
import random
import requests
import urllib2, sys
import json

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')


user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

class requests_manager(object):
    def __init__(self):

        self.user_agent = random.choice(user_agent_list)
        self.headers = {'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Cache-Control': 'max-age=0',
                        'User-Agent': self.user_agent,
                        # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                        'Connection': 'keep-alive'
                        }

    def get_html(self, url):
        self.headers['User-Agent'] = random.choice(user_agent_list)
        print "user_agent:", self.headers['User-Agent']
        resp = requests.get(url, headers=self.headers)
        resp.encoding = resp.apparent_encoding
        resp.raise_for_status()
        html = resp.text
        resp.close()
        return html

if __name__ == '__main__':
    requests_manager = requests_manager()
    # print requests_manager.get_html('http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=002450+PEG')

    import pandas as pd
    import numpy as np
    import json
    import traceback
    import bs4
    import re
    import datetime
    import time

    stock_list = pd.read_csv('C:\Users\Administrator\Desktop\stock_list.csv', dtype=np.str)
    stock_list = stock_list.set_index("stock_code")

    output = pd.DataFrame([])
    for i in range(stock_list.shape[0]):
        try:
            stock_code = stock_list.index[i]
            print 'stock:', stock_code

            resp = requests_manager.get_html('http://data.eastmoney.com/dxf/q/%s.html' %stock_code)
            bs_obj = bs4.BeautifulSoup(resp, 'html.parser')
            e_table = bs_obj.find('div', class_='contentBox').table
            df = pd.read_html(e_table.prettify(encoding='utf8'), encoding='utf8')[0]
            df.columns = [u'序号', u'解除限售日期', u'占总股本比例%', u'数量（万股）',u'最新价（元）',u'当前市值（亿元）',u'限售股东一览']
            df['date'] = pd.to_datetime(df[u'解除限售日期']).copy()
            print df
            df = df[df['date'].between(datetime.datetime.now(), datetime.datetime(year=2200, month=1, day=1))]
            df = df.set_index('date')
            df = df.sort_index()
            print df


            s = ''
            for date in df.index:
                s = s + date.strftime(u'%Y/%m/%d') + u'：解禁' + str(df.loc[date, u'占总股本比例%']) + u'%\n'
            print s
            output = output.append({
                u'股票代码':stock_list.index[i],
                u'解禁期':s
            },
            ignore_index=True)
            output.to_excel(u'C:\\Users\\Administrator\\Desktop\\stock_解禁1.xlsx')




            # data_l = json.loads(resp)['Result']['pjtj']
            # # data_l = pd.read_json(data)
            # res = pd.DataFrame([])
            # for d in data_l:
            #     # print d
            #     d['stock_code'] = df.index[i]
            #     res = res.append(d,ignore_index=True)
            # output = output.append({
            #     u'股票代号':df.index[i],
            #     u'3月内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'3月内']['mr'].iloc[0], res[res['sjd'] == u'3月内']['zc'].iloc[0]),
            #     u'6月内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'6月内']['mr'].iloc[0], res[res['sjd'] == u'6月内']['zc'].iloc[0]),
            #     u'1年内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'1年内']['mr'].iloc[0], res[res['sjd'] == u'1年内']['zc'].iloc[0])
            # },
            # ignore_index=True)
            # print output
            # output.to_excel('C:\Users\Administrator\Desktop\stock_predict.xlsx')
        except:
            print traceback.format_exc()


    for i in range(stock_list.shape[0]):
        try:
            stock_code = stock_list['stock_type'].iloc[i] + stock_list.index[i]
            print 'stock:', stock_code

            resp = requests_manager.get_html('http://emweb.securities.eastmoney.com/PC_HSF10/ProfitForecast/ProfitForecastAjax?code=%s' %stock_code)
            data_l = json.loads(resp)['Result']['pjtj']
            # data_l = pd.read_json(data)
            res = pd.DataFrame([])
            for d in data_l:
                # print d
                d['stock_code'] = stock_list.index[i]
                res = res.append(d,ignore_index=True)
            output = output.append({
                u'股票代号':stock_list.index[i],
                u'3月内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'3月内']['mr'].iloc[0], res[res['sjd'] == u'3月内']['zc'].iloc[0]),
                u'6月内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'6月内']['mr'].iloc[0], res[res['sjd'] == u'6月内']['zc'].iloc[0]),
                u'1年内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'1年内']['mr'].iloc[0], res[res['sjd'] == u'1年内']['zc'].iloc[0])
            },
            ignore_index=True)
            print output
            output.to_excel('C:\Users\Administrator\Desktop\stock_predict1.xlsx')
        except:
            print traceback.format_exc()

    # # 东方财富网研报
    # with open('url.txt', 'r') as f:
    #     s = f.read()
    #
    # l = [s0.split(',') for s0 in s.split('","')]
    # ori_data = pd.DataFrame(l).dropna()
    # ori_data[1] = pd.to_datetime(ori_data[1]).copy()
    # print ori_data
    # for i in range(ori_data.shape[0]):
    #     try:
    #         url = 'http://data.eastmoney.com/report/%s/hy,%s.html' %(ori_data[1].iloc[i].strftime('%Y%m%d'), ori_data[2].iloc[i])
    #         resp = requests_manager.get_html(url)
    #         # with open('test.html','w') as f:
    #         #     f.write(resp)
    #         print url
    #         bs_obj = bs4.BeautifulSoup(resp,'html.parser')
    #         e_div = bs_obj.find('div', class_='newsContent')
    #         title = bs_obj.find('div', class_='report-title').get_text(strip=True)
    #         organization = ori_data[4].iloc[i]
    #
    #         file_name = "(%s%s)%s.txt" %(ori_data[1].iloc[i].strftime(u'%Y%m%d'), organization, title)
    #         with open(file_name,'w') as f:
    #             f.write(title+'\n')
    #             f.write(organization+'\n')
    #             f.write(ori_data[1].iloc[i].strftime(u'%Y%m%d')+'\n')
    #             f.write(e_div.get_text())
    #         time.sleep(1)
    #     except:
    #         print traceback.format_exc()






# http://dc.simuwang.com/ranking/get?page=1&condition=fund_type%3A1%2C6%2C4%2C3%2C8%2C2%3Bret%3A1%3Brating_year%3A1%3Bstrategy%3A1%3Bistiered%3A0%3Bcompany_type%3A1%3Bsort_name%3Aprofit_col2%3Bsort_asc%3Adesc%3Bkeyword%3A
# http://dc.simuwang.com/ranking/get?page=1&condition=fund_type%3A7%3Bret%3A1%3Brating_year%3A1%3Bstrategy%3A1%3Bistiered%3A0%3Bcompany_type%3A1%3Bsort_name%3Aprofit_col2%3Bsort_asc%3Adesc%3Bkeyword%3A
