# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: html_table_reader.py
    @time: 2017/7/19 16:35
    @instruction: table_tr_td => 解析html中tabel>tr>td这种格式的表格
                  standardize => 将解析过存储在df中的表格按需求做DIY
--------------------------------
"""
import sys
import bs4
import pandas as pd
import numpy as np

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')

class html_table_reader(object):
    def __init__(self):
        pass

    def table_tr_td(self, e_table, fill_method = None):
        """
        :param e_table: bs4的table元素
        :param fill_method : 参数与fillna()中的method相同，选择填充方式，否则用None
        :return:
        """
        if not (isinstance(e_table, bs4.element.Tag) or isinstance(e_table, bs4.BeautifulSoup)):
            e_table = bs4.BeautifulSoup(e_table, 'html.parser')

        # 搭建表格框架
        df0 = pd.DataFrame(e_table.find_all('tr'))
        df0[1] = df0[0].apply(lambda e:len(e.find_all('td')))
        col_count = max(df0[1])
        row_count = len(df0.index)
        df = pd.DataFrame(np.zeros([row_count, col_count]), dtype=int)

        # 根据网页中的表格，还原在dataframe中，有合并单元格现象的
        # 值填在第一个单元格中，其他的用None填充
        e_trs = df0[0].tolist()
        for r in xrange(row_count):
            row = e_trs[r]
            e_tds = row.find_all('td')
            i = 0
            has_colspan = False
            for c in xrange(col_count):
                if pd.isnull(df.iloc[r,c]):
                    continue
                e_td = e_tds[i]
                # 横向合并的单元格
                if e_td.has_attr('colspan'):
                    has_colspan = True
                    for j in xrange(1, int(e_td['colspan'])):
                        df.iloc[r, c + j] = None
                # 竖向合并的单元格
                if e_td.has_attr('rowspan'):
                    for j in xrange(1, int(e_td['rowspan'])):
                        df.iloc[r + j, c] = None
                df.iloc[r, c] = e_td.get_text(strip=True)
                i = i + 1
            if has_colspan and fill_method:
                df.iloc[r,:] = df.iloc[r,:].fillna(method = fill_method)

        return df

    def standardize(self, df, delimiter='/\n/', b0 = True):
        """将数据的标题与数据分离，将有合并单元的行合并"""
        if b0 and df.iloc[0,:].hasnans and df.iloc[1,:].hasnans:# 假设第一排数据行没有横向合并单元格
            df.iloc[0, :] = df.iloc[0, :].fillna(method='ffill') + (delimiter + df.iloc[1,:]).fillna('')
            df.columns = df.iloc[0]
            df.columns.name = None
            df = df.drop([0,1], axis=0)

        for r in xrange(df.shape[0]-1, 0, -1):
            if df.iloc[r,:].hasnans:
                df.iloc[r-1, :] = df.iloc[r-1, :] + (delimiter + df.iloc[r, :]).fillna('')
                df = df.drop(r,axis=0)

        df.index = range(len(df.index)) # 索引重新从0计算
        return df

if __name__ == '__main__':
    s = """<table width="711" cellspacing="0" cellpadding="0"><tbody><tr style="PAGE-BREAK-INSIDE: avoid; HEIGHT: 29px"><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: windowtext 1px solid; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" rowspan="2" height="29" width="62"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">编号</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" rowspan="2" height="29" width="93" valign="top"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">&nbsp;</span></p><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">土地位置</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" rowspan="2" height="29" width="48" valign="top"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">&nbsp;</span></p><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">土地面积（m<sup>2</sup>）</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" rowspan="2" height="29" width="48"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">土地用途</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" colspan="5" height="29" width="259"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">主要规划指标要求</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" rowspan="2" height="29" width="56"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">使用年期（年）</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" rowspan="2" height="29" width="56"><p><span style="FONT-FAMILY: 仿宋">建设时间（年）</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" rowspan="2" height="29" width="46"><p><span style="FONT-FAMILY: 仿宋">起始价（万元）</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: windowtext 1px solid; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" rowspan="2" height="29" width="41"><p><span style="FONT-FAMILY: 仿宋">竞买保证金(万元)</span></p></td></tr><tr style="PAGE-BREAK-INSIDE: avoid; HEIGHT: 10px"><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="10" width="48"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">容积率</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="10" width="47" valign="top"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">建筑密度</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="10" width="56" valign="top"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">建筑面积（m<sup>2</sup>）</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="10" width="58" valign="top"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">建筑高度（m）</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="10" width="51"><p><span style="FONT-FAMILY: 仿宋">绿地率</span></p></td></tr><tr style="PAGE-BREAK-INSIDE: avoid; HEIGHT: 71px"><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: windowtext 1px solid; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="62"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">衢市储</span><span style="FONT-FAMILY: 仿宋">﹙2016﹚13 </span><span style="FONT-FAMILY: 仿宋">号</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="93"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">双桥乡双桥村、塔太线以东、双桥水产养殖基地的衢江区杜泽镇Ｂ2016-1号地块</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="48"><p><span style="FONT-FAMILY: 仿宋">4627</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="48"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">商业服务业设施用地</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="48"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≤1.5</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="47"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≤65%</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="56"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≤6940.5</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="58"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≤20</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="51"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≥10%</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="56"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">40</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="56"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">2</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="46"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">550</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="41"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">150</span></p></td></tr><tr style="PAGE-BREAK-INSIDE: avoid; HEIGHT: 71px"><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: windowtext 1px solid; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="62"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋; FONT-SIZE: 12px">衢市储（2016）14号</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="93"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">双桥乡双桥村、塔太线以东、双桥水产养殖基地的衢江区杜泽镇Ｂ2016-2号地块</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="48"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">6673</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="48"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">公园绿地</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="48"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≤0.1</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="47"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≤10%</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="56"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≤667.3</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="58"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≤5</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="51"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">≥80%</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="56"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">40</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="56"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">2</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="46"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">190</span></p></td><td style="BORDER-BOTTOM: windowtext 1px solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0px; BACKGROUND-COLOR: transparent; PADDING-LEFT: 7px; PADDING-RIGHT: 7px; BORDER-TOP: #f0f0f0; BORDER-RIGHT: windowtext 1px solid; PADDING-TOP: 0px" height="71" width="41"><p style="TEXT-ALIGN: center"><span style="FONT-FAMILY: 仿宋">50</span></p></td></tr></tbody></table>"""
    html_table_reader = html_table_reader()
    df = html_table_reader.table_tr_td(s,None)
    df.to_csv('df.csv', encoding='utf_8_sig')
    #html_table_reader.standardize(df).to_csv('df.csv', encoding='utf_8_sig')