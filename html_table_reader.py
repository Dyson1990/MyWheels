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

    def table_tr_td(self, e_table, fill_method = None, start_row = 0):
        """
        :param e_table: bs4的table元素
        :param fill_method : 参数与fillna()中的method相同，选择填充方式，否则用None
        :return:
        """
        if not (isinstance(e_table, bs4.element.Tag) or isinstance(e_table, bs4.BeautifulSoup)):
            e_table = bs4.BeautifulSoup(e_table, 'html.parser')

        # 搭建表格框架
        df0 = pd.DataFrame(e_table.find_all('tr')[start_row:])
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
                    # 有些'colspan'会超出表格宽度
                    for j in xrange(1, min(col_count-c,int(e_td['colspan']))):
                        print df
                        df.iloc[r, c + j] = None
                # 竖向合并的单元格
                if e_td.has_attr('rowspan'):
                    # 有些'rowspan'会超出表格高度
                    for j in xrange(1, min(row_count-r,int(e_td['rowspan']))):
                        df.iloc[r + j, c] = None
                df.iloc[r, c] = e_td.get_text(strip=True)
                i = i + 1
            if has_colspan and fill_method:
                df.iloc[r,:] = df.iloc[r,:].fillna(method = fill_method)

        return df

    def title_standardize(self, df, delimiter='/\n/', b0 = True):
        """将数据的标题与数据分离，将有合并单元的行合并"""
        if b0 and df.iloc[0,:].hasnans and df.iloc[1,:].hasnans:# 假设第一排数据行没有横向合并单元格
            df.iloc[0, :] = df.iloc[0, :].fillna(method='ffill') + (delimiter + df.iloc[1,:]).fillna('')
            df = df.drop([1,], axis=0)

        df.columns = df.iloc[0,:]
        df.columns.name = None
        df = df.drop([0,], axis=0)

        df.index = range(len(df.index)) # 索引重新从0计算
        return df

    def data_standardize(self, df, delimiter=r'/\n/'):
        for r in xrange(df.shape[0]-1, 0, -1):
            if df.iloc[r,:].hasnans:
                df.iloc[r-1, :] = df.iloc[r-1, :] + (delimiter + df.iloc[r, :]).fillna('')
                df = df.drop(r,axis=0)
        df.index = range(len(df.index))  # 索引重新从0计算
        return df

    def standardize(self, df, delimiter=r'/\n/', b0 = True):
        df = self.title_standardize(df, delimiter, b0)
        df = self.data_standardize(df, delimiter)

        return df



if __name__ == '__main__':
    s = """
            <table style="border-bottom-color: #333333; border-top-color: #333333; border-collapse: collapse; border-right-color: #333333; font-size: 12px; border-left-color: #333333" width="100%" cellspacing="0" cellpadding="1" border="1">
                <tbody>
                    <tr>
                        <td style="width: 100px">宗地编号：</td>
                        <td style="width: 200px; word-break: break-all">&nbsp; 定海区招拍挂地块SF-2016-001号</td>
                        <td style="width: 100px">宗地面积：</td>
                        <td style="width: 90px">&nbsp;45097平方米</td>
                        <td style="width: 110px">宗地坐落：</td>
                        <td style="width: 200px">&nbsp;定海区干览镇（国际水产品产业园区）</td>
                    </tr>
                    <tr>
                        <td>出让年限：</td>
                        <td>&nbsp;40年</td>
                        <td>容积率：</td>
                        <td>&nbsp;1.3≤容积率≤1.5</td>
                        <td>建筑密度(%)：</td>
                        <td>&nbsp;≤50</td>
                    </tr>
                    <tr>
                        <td>绿化率(%)：</td>
                        <td>&nbsp;≥10</td>
                        <td>建筑限高(米)：</td>
                        <td>&nbsp;</td>
                        <td>土地用途：</td>
                        <td>&nbsp;批发零售用地</td>
                    </tr>
                    <tr>
                        <td>投资强度：</td>
                        <td>&nbsp;0万元/公顷</td>
                        <td>保证金：</td>
                        <td>&nbsp;1<a href="http://11" title="">11</a>3万元</td>
                        <td>土地估价备案号：</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td colspan="6">&nbsp;现状土地条件：交地时现状为净地</td>
                    </tr>
                    <tr>
                        <td>起始价：</td>
                        <td>&nbsp;5566.257万元</td>
                        <td>加价幅度：</td>
                        <td colspan="3">&nbsp;3.9477万元</td>
                    </tr>
                    <tr>
                        <td nowrap="nowrap">挂牌开始时间：</td>
                        <td>&nbsp;2016年02月27日09时00分</td>
                        <td>挂牌截止时间：</td>
                        <td colspan="3">&nbsp;2016年03月07日16时00分</td>
                    </tr>
                    <tr>
                        <td>备注：</td>
                        <td colspan="9">&nbsp;1、本宗地商务办公建筑面积不超过总建筑面积的45%，土地用途为批发零售用地、商务金融用地（40年），具体用途及土地面积须经项目竣工验收合格后，在土地登记时确定；2、其他具体土地使用条件按舟山市规划局出具的规划设计条件为准。</td>
                    </tr>
                </tbody>
            </table>"""
    html_table_reader = html_table_reader()
    df = html_table_reader.table_tr_td(s,None)
    #df.to_csv('df.csv', encoding='utf_8_sig')
    print df
    #print html_table_reader.standardize(df)