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
            i = 0 # 为了跳过已经填好None值的单元格，直接用列序号会报错
            has_colspan = False
            for c in xrange(col_count):
                if pd.isnull(df.iloc[r,c]):
                    continue
                if i > len(e_tds)-1 and df.iloc[r,c]==0:
                    df.iloc[r, c] = None
                    continue
                e_td = e_tds[i]
                # 横向合并的单元格
                if e_td.has_attr('colspan'):
                    has_colspan = True
                    # 有些'colspan'会超出表格宽度
                    for j in xrange(1, min(col_count-c,int(e_td['colspan']))):
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
        # 防止在读写json的时候出现顺序问题
        #df.index = [str(i) for i in df.index]
        #df.columns = [str(i) for i in df.columns]
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
<table style="border-color:#333333;font-size:12px;" width="100%" cellspacing="0" cellpadding="4" border="1">
		<tbody>
			<tr>
				<td>
					地块编号
				</td>
				<td>
					地块位置
				</td>
				<td>
					土地面积(公顷)
				</td>
				<td>
					土地用途
				</td>
				<td>
					出让年限
				</td>
				<td>
					成交价(万元)
				</td>
				<td>
					受让单位
				</td>
			</tr>
			<tr>
				<td>
					金西东区D-003-02号
				</td>
				<td>
					金西东区琳湖街东侧
				</td>
				<td>
					0.3918
				</td>
				<td>
					工业用地
				</td>
				<td>
					50
				</td>
				<td>
					176.31
				</td>
				<td>
					金华市海纳工具有限公司
				</td>
			</tr>
			<tr>
				<td>
					土地使用条件：
				</td>
				<td colspan="6">
					详见《建设用地规划条件书》
				</td>
			</tr>
			<tr>
				<td>
					备注：
				</td>
			</tr>
		</tbody>
	</table>"""
    html_table_reader = html_table_reader()
    df = html_table_reader.table_tr_td(s,None)
    #df.to_csv('df.csv', encoding='utf_8_sig')
    print df
    #print html_table_reader.standardize(df)