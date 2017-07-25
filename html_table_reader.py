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

if __name__ == '__main__':
    s = """<table bordercolor="#000000" border="1">
		<tbody>
			<tr>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">地块坐落</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">土地面积</span>
					</p>
					<p>
						<span style="font-family:SimSun;font-size:14px;">（㎡）</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">容积率</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">建筑密度</span>
					</p>
					<p>
						<span style="font-family:SimSun;font-size:14px;">（%）</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">绿地率</span>
					</p>
					<p>
						<span style="font-family:SimSun;font-size:14px;">（%）</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">起始价</span>
					</p>
					<p>
						<span style="font-family:SimSun;font-size:14px;">（万元）</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">保证金</span>
					</p>
					<p>
						<span style="font-family:SimSun;font-size:14px;">（万元）</span>
					</p>
				</td>
			</tr>
			<tr>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">刘英小学南侧1号地块</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">4309</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">1.0-1.1</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">≤48</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">≥12</span>
					</p>
				</td>
				<td rowspan="3">
					<p>
						<span style="font-family:SimSun;font-size:14px;">2630</span>
					</p>
				</td>
				<td rowspan="3">
					<p>
						<span style="font-family:SimSun;font-size:14px;">1500</span>
					</p>
				</td>
			</tr>
			<tr>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">刘英小学南侧2号地块</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">4118</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">1.0-1.1</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">≤55</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">≥6.5</span>
					</p>
				</td>
			</tr>
			<tr>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">刘英小学南侧3号地块</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">2893</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">1.0-1.1</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">≤40</span>
					</p>
				</td>
				<td>
					<p>
						<span style="font-family:SimSun;font-size:14px;">≥12</span>
					</p>
				</td>
			</tr>
		</tbody>
	</table>"""
    html_table_reader = html_table_reader()
    df = html_table_reader.table_tr_td(s,None)
    #df.to_csv('df.csv', encoding='utf_8_sig')
    print html_table_reader.title_standardize(df)#.to_csv('df.csv', encoding='utf_8_sig')