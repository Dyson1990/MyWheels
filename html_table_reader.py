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
import re

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
        if df.empty:
            df = pd.read_html(e_table.prettify(), encoding='utf8')
        return df

    def title_standardize(self, df, delimiter='=>', b0 = True, fillna_method='ffill'):
        """将数据的标题与数据分离，将有合并单元的行合并"""
        if b0 and df.iloc[0,:].hasnans and df.iloc[1,:].hasnans:# 假设第一排数据行没有横向合并单元格
            if fillna_method:
                df.iloc[0, :] = df.iloc[0, :].fillna(method=fillna_method) + (delimiter + df.iloc[1,:]).fillna('')
            else:
                df.iloc[0, :] = df.iloc[0, :].fillna('') + (delimiter + df.iloc[1,:]).fillna('')
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
<table class="publicityCss" id="_ctl9_dataGrid" style="width:100%;border-collapse:collapse;" cellspacing="0" border="0">
	<tbody><tr class="thead even">
		<td>项目名称</td><td style="width:115px;">公示类别</td><td style="width:80px;">公示日期</td><td style="width:80px;">截止日期</td>
	</tr><tr class="DGtable_item odd">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10369.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10369" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10369" target="_blank">
                            钱江商城（水晶城购物中心）地下非机动车库改...<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-30</td><td align="center">2017-10-14</td>
	</tr><tr class="DGtable_item even">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10374.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10374" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10374" target="_blank">
                            杭政储出（2016）37号地块商品住宅兼容商业商...<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item odd">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10373.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10373" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10373" target="_blank">
                            丁桥单元JG0406-06地块<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item even">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10372.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10372" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10372" target="_blank">
                            杭州市丁桥单元JG0405-11地块<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item odd">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10371.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10371" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10371" target="_blank">
                            杭州市丁桥单元JG0405-12地块<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item even">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10370.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10370" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10370" target="_blank">
                            汽车南站和望江东路公交首末站临时过渡工程<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item odd">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10368.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10368" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10368" target="_blank">
                            彭埠单元B1/B2-22地块<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item even">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10367.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10367" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10367" target="_blank">
                            杭州市滨江区西兴北单元M1-11地块<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item odd">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10366.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10366" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10366" target="_blank">
                            杭州朕昊企业管理有限公司车间二（补办）项目<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item even">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10365.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10365" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10365" target="_blank">
                            杭州市萧山区南阳街道黄山庙迁建项目<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item odd">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10364.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10364" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10364" target="_blank">
                            杭州迪威机械有限公司旧厂区（房）改造项目<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-13</td>
	</tr><tr class="DGtable_item even">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10355.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10355" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10355" target="_blank">
                            杭州萧山胜达新建厂房项目<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-29</td><td align="center">2017-10-14</td>
	</tr><tr class="DGtable_item odd">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10363.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10363" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10363" target="_blank">
                            滨江区东冠单元C6-02地块<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-28</td><td align="center">2017-10-12</td>
	</tr><tr class="DGtable_item even">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10362.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10362" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10362" target="_blank">
                            彭埠单元R21-19地块<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-28</td><td align="center">2017-10-12</td>
	</tr><tr class="DGtable_item odd">
		<td align="left">
                        <div src="http://www.hzplanning.gov.cn/winstarframework/desktopmodules/PointerPic/10361.jpg" link="http://map.hzplanning.gov.cn/module/index.html?lx=XM_PQGS&amp;value=10361" style="display: none;">
                        </div>
                        <img src="../../../Themes/Skins/Spring/Citizen/ico.gif" border="0">
                        <a href="/DesktopModules/GHJ.PlanningNotice/PublicityInfoPQGS.aspx?GUID=10361" target="_blank">
                            彭埠单元（城东新城范围）B1/B2-17地块<img src="../../images/new.gif"></a>
                    </td><td align="left">
                        建设工程规划公示
                    </td><td align="center">2017-09-28</td><td align="center">2017-10-12</td>
	</tr>
</tbody></table>"""
    html_table_reader = html_table_reader()
    df = html_table_reader.table_tr_td(s,None)
    #df.to_csv('df.csv', encoding='utf_8_sig')
    print df
    #print df.empty
    #print df.iloc[0,0].replace(u'\xa0','')
    #print html_table_reader.standardize(df)
    #print pd.read_html(s,encoding='utf8')