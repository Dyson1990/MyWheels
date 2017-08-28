# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: spider_func.py
    @time: 2017/8/24 17:48
--------------------------------
"""
import sys
import os
import json
import html_table_reader
import re
import pandas as pd
import bs4
html_table_reader = html_table_reader.html_table_reader()

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')

with open(os.getcwd() + r'\spider_args.json') as f:
    spider_args = json.load(f, encoding='utf8')

class spider_func(object):
    def __init__(self):
        with open(os.getcwd() + r'\spider_args.json') as f:
            self.spider_args = json.load(f, encoding='utf8')

    def df_output(self, bs_obj, spider_id, parcel_status):
        spider_args = self.spider_args[spider_id]
        if isinstance(bs_obj, bs4.element.Tag) and bs_obj.name == spider_args['table_tag']:
            e_table = bs_obj
        else:
            e_table = bs_obj.find(spider_args['table_tag'], attrs=spider_args['table_attrs'])
        df = html_table_reader.table_tr_td(e_table)
        monitor_extra = ''
        if parcel_status == 'onsell' and 'extra' in spider_args:
            func = getattr(self,spider_args['extra_func'])
            monitor_extra = func(bs_obj, spider_args['extra'])
        content_detail = df
        return content_detail,monitor_extra

    def extra_parse(self, bs_obj, extra_agrs):
        if not bs_obj:
            return

        e_ps = bs_obj.find(extra_agrs['tag'],attrs=extra_agrs['attrs']).find_all(extra_agrs['row_tag'])
        s_list = [e_p.get_text(strip=True) for e_p in e_ps if re.search(ur'时间',e_p.get_text(strip=True))]
        return pd.DataFrame({'date_info': ur'\n'.join(s_list)}, index=[0,])

if __name__ == '__main__':
    pass