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

        # 运行pretreatment中的函数
        if 'pretreatment' in spider_args:
            for s in spider_args['pretreatment']:
                func = getattr(self,s)
                bs_obj = func(bs_obj,parcel_status)

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

        if isinstance(bs_obj, bs4.element.Tag) and bs_obj.name == extra_agrs['tag']:
            e_ps = bs_obj
        else:
            e_ps = bs_obj.find(extra_agrs['tag'], attrs=extra_agrs['attrs']).find_all(extra_agrs['row_tag'])

        s_list = [e_p.get_text(strip=True) for e_p in e_ps if isinstance(e_p, bs4.element.Tag) and re.search(ur'时间',e_p.get_text())]
        return pd.DataFrame({'date_info': ur'\n'.join(s_list)}, index=[0,])

    def the_last_table(self,bs_obj,parcel_status):
        e_table = bs_obj
        while e_table.table:
            e_table = e_table.table
        return e_table

    def shaoxing(self,bs_obj,parcel_status):
        if parcel_status == 'sold':
            bs_obj = bs_obj.find('td', attrs={'id': 'TDContent', 'class': 'infodetail'})
        return bs_obj

    def hangzhouyuhang(self,bs_obj,parcel_status):
        return bs_obj.find("div", class_="TRS_Editor")

if __name__ == '__main__':
    spider_func = spider_func()
    s = """<body>
    <div class="main-body" id="container">
<table class="yhZFNu05" width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td>
   <!--head-->
<link href="../../../../images/yuhang.ico" rel="SHORTCUT ICON">
<style type="text/css">
.menuColor{
	color:#7c9bbc;font-weight:bold;
}
.menuColor a{
	color:#7c9bbc;font-weight:bold;
}
.menuHover a:hover{
	color:#7c9bbc;
}

.CHANNELID_617 a{
			color:#7c9bbc;font-weight:bold;
		}
.CHANNELID_505 a{
			color:#7c9bbc;font-weight:bold;
		}
</style>

<script language="javascript" src="../../../../images/js.js"></script>

<script language="javascript">

var iStartNum = 0;
var aParent = new Array();
aParent[0] = "土地";
aParent[1] = "公告公示";
aParent[2] = "信息公开";
aParent[3] = "";
aParent[4] = "";
aParent[5] = "";

function menubs(sValue,sNum,nStyleName){

	if(iStartNum==0){
		for(i=0;i&lt;=5;i++){
			if(aParent[i]==sValue){			
			    document.getElementById("MENU_"+sNum).className=nStyleName;
			    iStartNum++;
				document.getElementById("MENU_"+sNum).parentNode.style.display="block";				
			    break;
			}		
		}
	}	
	
}

</script>
<script language="javascript">
//切换标签 TRS-YAN 
//参数(名字,当前签,共几签,选中样式,未选样式,更多名字,更多值)
function setTab(name,cursel,n,style1,style2,hrefname,hrefvale){
 var temp=1;
 if(cursel==0){
 	temp=0;
 }else if(document.getElementById(name+"0")!=null){
 	document.getElementById(name+"0").className="";
 } 
  for(i=temp;i&lt;=n;i++){
  var menu=document.getElementById(name+i);
  var con=document.getElementById("con_"+name+"_"+i);
  menu.className=i==cursel?style1:style2;
  if(hrefname!='null'){
 	 var ahref = document.getElementById(hrefname);
 	 ahref.setAttribute('href',hrefvale);
  }
  
  con.style.display=i==cursel?"block":"none";
    
 }
  document.getElementById("one2").className='first';
  if(cursel==0){
 	document.getElementById("con_"+name+"_2").style.display="block";
  }
}




//设为首页 TRS-YAN
function homePage(obj) {
    var url = window.location.href;
    try {
        obj.style.behavior = 'url(#default#homepage)';
        obj.setHomePage(url);
        }catch(e){

        if (window.netscape) {
            try {
                netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
            }catch(e) {
                alert("此操作被浏览器拒绝！\n请在浏览器地址栏输入“about:config”并回车\n然后将 [signed.applets.codebase_principal_support]的值设置为'true',双击即可。");
            }
            var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components.interfaces.nsIPrefBranch);
            prefs.setCharPref('browser.startup.homepage', url);
        }
    }
}
//加入收藏 TRS-YAN
function add() {
    var url = window.location.href;
    try {
        window.external.addFavorite(url, document.title);
       }catch(e) {
        try {
            window.sidebar.addPanel(document.title, url, "");
        } catch(e) {
            alert("加入收藏失败，请使用Ctrl+D进行添加");
        }
    }
}

function trim(str){   
     return str.replace(/^(\s|\u00A0)+/,'').replace(/(\s|\u00A0)+$/,'');   
}
function stripscript(s) 
{ 
var pattern = new RegExp("[`~!@#$^&amp;*()=|{}':;',\\[\\].&lt;&gt;/?~！@#￥……&amp;*（）&amp;mdash;&mdash;|{}【】‘；”“'。，、？]") 
var rs = ""; 
for (var i = 0; i &lt; s.length; i++) { 
rs = rs+s.substr(i, 1).replace(pattern, ''); 
} 
return rs; 
} 
function checkInput()
{
        if (trim(document.searchform.searchword.value)==''){
            document.searchform.searchword.focus();
            alert("检索条件不能为空");
			return false;
        }
    document.searchform.searchword.value=stripscript(document.searchform.searchword.value);	
   return true;
        /*else{
			document.searchform.submit();
        }*/
}

</script>  
 
<table class="Top01" width="1000" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td height="32" width="365">&nbsp;&nbsp;<a href="#" onclick="homePage(this)">设为首页</a> | <a href="#" onclick="add()">加入收藏</a> | <a href="../../../../rss.html" target="_blank">RSS订阅</a></td>
    <td width="261"></td>
    <td width="375" align="right">
       <a href="javascript:zh_tran('s');" class="zh_click" id="zh_click_s">简体</a>
       <a href="javascript:zh_tran('t');" class="zh_click" id="zh_click_t">繁体</a>
<!--<a href='../../../../index/'>简体中文</a> | <a target="_blank" href='http://115.28.93.188/gate/big5/www.yuhang.gov.cn/'>繁体中文</a> | --><a href="../../../../English/">英文版</a> | <a target="_blank" href="../../../../sjb/">手机版</a> | <a href="javascript:;" onclick="kqNav()">无障碍浏览</a>
<script type="text/javascript" src="../../../../images/wzall.js"></script>
 <!-- | <a target="_blank" href='http://2008.yuhang.gov.cn'>回到旧版</a> -->
</td>
  </tr>
</tbody></table>
    <table width="1000" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td><img src="../../../../images/xxGKn01.jpg"></td>
  </tr>
</tbody></table>



<table width="1000" cellspacing="0" cellpadding="0" border="0" background="../../../../images/ZjYhN04.gif" align="center">
  <tbody><tr>
    <td width="9"><img src="../../../../images/ZjYhN02.gif"></td>
    <td width="686">  
    <table class="yhZFNu03 xxGK01" width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
	<td id="one0" onmouseover="setTab('one',0,4,'first firstAlpha','','null','null')" class="" width="90" align="center"><a href="../../../../index/">首页</a></td>
    <td id="one1" onmouseover="setTab('one',1,4,'first firstAlpha','','null','null')" class="" width="90" align="center"><a href="../../../../zjyh/">走进余杭</a></td>
    <td id="one2" onmouseover="setTab('one',2,4,'first','','null','null')" class="first" width="90" align="center"><a href="../../../">信息公开</a></td>
    <td id="one3" onmouseover="setTab('one',3,4,'first firstAlpha','','null','null')" class="first firstAlpha" width="90" align="center"> <a href="../../../../zmhd/">公众参与</a></td>
    <td width="90" align="center"><a href="http://hzyh.zjzwfw.gov.cn/" target="_blank">网上办事</a></td>
    <td id="one4" onmouseover="setTab('one',4,4,'first firstAlpha','','null','null')" class="" width="90" align="center"><a href="../../../../ggfw/">公共服务</a></td>
    <td width="90" align="center"><a href="../../../../yhly/">畅游余杭</a></td>
  </tr>
</tbody></table>
    </td>
    <td width="5"></td>
    <td width="267">
        <form name="searchform" action="/was5/web/search" method="post" target="_blank">
        <table width="100%" cellspacing="0" cellpadding="0" border="0">
          <tbody><tr>
            <td width="7%"><img src="../../../../images/yhZFn011.gif"></td>
            <td class="yhZFNu01-1" width="47%">
            <input name="channelid" value="223053" type="hidden">
            <input name="perpage" value="" type="hidden">
            <input name="templet" value="" type="hidden">
            <input name="token" value="" type="hidden">
            <input id="textfield" name="searchword" class="yhZFNu02-1" type="text">
        </td>
        <td width="20%"><input src="../../../../images/yhZFn09.gif" onclick="return checkInput();" type="image"></td>
        <td width="26%"><!--<a target="_blank" href="http://www.yuhang.gov.cn/index/Search/"><img src="../../../../images/yhZFn010.gif" /></a>--></td>
      </tr>
    </tbody></table>
   </form>

    </td>
    <td width="12" align="right"><img src="../../../../images/ZjYhN03.gif"></td>
  </tr>
</tbody></table>
<table style="border-top:0;" class="yhZFNu04 ZjYhN01 menuHover" width="1000" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td width="990">
           <!--标签切换二级-->
<table id="con_one_1" style="display:none" width="98%" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td height="35">
   
			
				<a href="../../../../zjyh/ldzc/">领导致辞</a>  |
			
   
			
				<a href="../../../../zjyh/jryh/">今日余杭</a>  |
			
   
			
				<a href="../../../../zjyh/yhgl/">余杭概览</a>  |
			
   
			
				<a href="../../../../zjyh/jianshe/">经济建设</a>  |
			
   
			
				<a href="../../../../zjyh/rwfg/">人文风光</a>  |
			
   
			
				<a href="../../../../zjyh/sthj/">生态环境</a>  |
			
   
			
				<a href="../../../../zjyh/qznj/">区志年鉴</a>  |
			
   
			
				<a href="../../../../zjyh/tjgb/">统计公报</a>  |
			
   
			
				<a href="../../../../zjyh/yhyh/">音画余杭</a>  |
			
   
			
				<a href="../../../../zjyh/zsyz/">招商引资</a>  |
			
   
			
				<a href="../../../../zjyh/yhmap/">电子地图</a>  |
			
   
			
				<a href="../../../../zjyh/ztzl/">专题专栏</a>  |
			
   
    </td>
  </tr>
</tbody></table>

<table id="con_one_2" style="display: none;" width="98%" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td height="35">
	<div id="con_xxgk_1" style="display: block;">
	
			
				 
				 <span id="MENU_501"><a href="../../../ldxx/">领导信息</a>
				 </span>   |
<script>menubs("领导信息","501","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_502"><a href="../../../zzjg/">组织机构</a>
				 </span>   |
<script>menubs("组织机构","502","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_12356"><a href="http://www.yuhang.gov.cn/zjyh/jryh/dzdt/">党政动态</a>
				 </span>   |
<script>menubs("党政动态","12356","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_503"><a href="../../../zcfg/">政策法规</a>
				 </span>   |
<script>menubs("政策法规","503","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_515"><a href="../../../ghjh/">规划计划</a>
				 </span>   |
<script>menubs("规划计划","515","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_505" class="menuColor"><a href="../../">公告公示</a>
				 </span>   |
<script>menubs("公告公示","505","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_507"><a href="../../../czxx/">财政信息</a>
				 </span>   |
<script>menubs("财政信息","507","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_504"><a href="../../../rsxx/">人事信息</a>
				 </span>   |
<script>menubs("人事信息","504","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_12313"><a href="../../../zfcg/">政府采购</a>
				 </span>   |
<script>menubs("政府采购","12313","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_509"><a href="../../../zdly/">重点领域</a>
				 </span>   |
<script>menubs("重点领域","509","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_517"><a href="../../../gzbg/">政府工作报告</a>
				 </span>   |
<script>menubs("政府工作报告","517","menuColor","MENU_");</script>

			
		
   
			
				 
				 <span id="MENU_14350"><a href="../../../zfssgc/">政府实事工程</a>
				 </span>   |
<script>menubs("政府实事工程","14350","menuColor","MENU_");</script>

			
		
   
    <span class="menuColor"><a href="#" onclick="setDiv('xxgk',2,2);"> &gt;&gt; </a></span>
   </div>
   <div id="con_xxgk_2" style="display:none;">
   
			
				 <span id="MENU_510"><a href="../../../yjgl/">应急管理</a></span>   |
<script>menubs("应急管理","510","menuColor","MENU_");</script>

			
   
			
				 <span id="MENU_511"><a href="../../../jdjc/">监督检查</a></span>   |
<script>menubs("监督检查","511","menuColor","MENU_");</script>

			
   
			
				 <span id="MENU_508"><a href="../../../tjxx/">统计信息</a></span>   |
<script>menubs("统计信息","508","menuColor","MENU_");</script>

			
   
			
				 <span id="MENU_514"><a href="../../../jzqz/">社会救助</a></span>   |
<script>menubs("社会救助","514","menuColor","MENU_");</script>

			
   
			
				 <span id="MENU_12318"><a href="../../../sqgl/">社区管理</a></span>   |
<script>menubs("社区管理","12318","menuColor","MENU_");</script>

			
   
			
				 <span id="MENU_516"><a href="../../../jhwl/">讲话文论</a></span>   |
<script>menubs("讲话文论","516","menuColor","MENU_");</script>

			
   
			
				 <span id="MENU_12277"><a href="../../../xwfbh/">新闻发布会</a></span>   |
<script>menubs("新闻发布会","12277","menuColor","MENU_");</script>

			
   
			
				 <span id="MENU_16493"><a href="../../../zywj/">中央及省、市委公开文件</a></span>   |
<script>menubs("中央及省、市委公开文件","16493","menuColor","MENU_");</script>

			
   
  <span class="menuColor"> <a href="#" onclick="setDiv('xxgk',1,2);"> &lt;&lt; </a></span>
   </div> 
   
    
    </td>
  </tr>
</tbody></table>

<script language="javascript">

function setDiv(name,cursel,n){
 for(i=1;i&lt;=n;i++){ 
  var con=document.getElementById("con_"+name+"_"+i);
  con.style.display=i==cursel?"block":"none";  
 }
}

var isONE = document.getElementById("con_xxgk_1").style.display=="block";
var isTWO = document.getElementById("con_xxgk_2").style.display=="block";
if(isONE||isTWO){
	
}else{
	document.getElementById("con_xxgk_1").style.display = "block";
}

</script>

<table id="con_one_3" style="display: block;" width="98%" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td height="35">
    <div id="con_gccy_1" style="display: block;">
                                            
                                                    <span id="MENU_1"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/fsxf.aspx?classid=1">
                                                        网上12345</a></span> |
                                                    
                                                
                                                    <span id="MENU_8"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/wsjb/wsjb.aspx?classid=8">
                                                        网上举报</a></span> |
                                                    
                                                 
                                                    <span id="MENU_9"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/ysqgk/ysqgk.aspx?classid=9">
                                                        依申请公开</a></span> |

                                                    <span id="MENU_7"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/bmfw/bmfw.aspx?classid=7">
                                                        便民服务</a></span> |                     
                                               
                                                    <span id="MENU_6"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/flyz/flyz.aspx?classid=6">
                                                        法律援助</a></span> |
                                                    
                                                
                                                    <span id="MENU_5"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/xlzx/xlzx.aspx?classid=5">
                                                        心理咨询</a></span> |
                                                    
                                                
                                                   <!-- <span id="MENU_19"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/bmfw/bmfw.aspx?classid=19">
                                                        消费者咨询</a></span> |-->
                                                    
                                                
                                                    <span id="MENU_10"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/bmxx/bmxx.aspx?classid=10">
                                                        大家来帮忙</a></span> |


                                              <!--      <span id="MENU_20"><a href="http://zqhd.yuhang.gov.cn/page/">
                                                        政企互动</a></span> |   -->
                                                
                                                    <span id="MENU_11"><a href="http://www.yuhang.gov.cn/zhhd/zmhd/xzfy/xzfy.aspx?classid=11">
                                                        行政复议</a></span> |
                                                    
                                                 
                                                    <!--<span id="MENU_12"><a href="http://www.yuhang.gov.cn/zmhd/jgpy1/">
                                                        机关评议</a></span> |-->
                                                    
                                                
                                                    <span id="MENU_13"><a href="http://www.yuhang.gov.cn/zmhd/wlwz/">
                                                        网络问政</a></span> |
                                                    
                                                
                                                    <span id="MENU_14"><a href="http://www.yuhang.gov.cn/zmhd/yian/">
                                                        议案提案</a></span> |
                                                    <span class="menuColor"><a href="#" onclick="setDiv('gccy',2,2);">&gt;&gt; </a></span></div> <div id="con_gccy_2" style="display: none;"> <span class="menuColor"><a href="#" onclick="setDiv('gccy',1,2);">&lt;&lt; </a></span>
                                                
                                                    <!--<span id="MENU_15"><a href="http://www.yuhang.gov.cn/zmhd/fangtan/">
                                                        在线访谈</a></span> |
                                                    
                                                
                                                    <span id="MENU_16"><a href="http://www.yuhang.gov.cn/zmhd/zhibo/">
                                                        网络直播</a></span> |-->
                                                    
                                                
                                                    <span id="MENU_17"><a href="http://www.yuhang.gov.cn/zmhd/mydc/">
                                                        民意调查</a></span> |
                                                    
                                                
                                        </div>
    </td>
  </tr>
</tbody></table>

<!--table width="98%" border="0" cellspacing="0" cellpadding="0" align="center" id="con_one_4" style="display:none">
  <tr>
    <Td height="35">
   
   
			
				<a href="../../../../wsbs/scene/">场景式服务</a>  |
			
   

    </Td>
  </tr>
</table-->

<table id="con_one_4" style="display:none" width="98%" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td height="35">
    <div id="con_ggfw_1">
    
			
				<a href="../../../../ggfw/shenghuo/">生活信息</a>  |
			
   
			
				<a href="../../../../ggfw/jypx/">教育培训</a>  |
			
   
			
				<a href="../../../../ggfw/shbz/">社会保障</a>  |
			
   
			
				<a href="../../../../ggfw/ldjy/">劳动就业</a>  |
			
   
			
				<a href="../../../../ggfw/ylws/">医疗卫生</a>  |
			
   
			
				<a href="../../../../ggfw/jtcx/">交通出行</a>  |
			
   
			
				<a href="../../../../ggfw/gysy/">公用事业</a>  |
			
   
			
				<a href="../../../../ggfw/ggfwcx/">公共服务查询</a>  |
			
   
			
				<a href="http://jhyy.zjmz.gov.cn/">预约婚姻登记</a>  |
			
   
   <span class="menuColor"><a href="#" onclick="setDiv('ggfw',2,2);"> &gt;&gt; </a></span>
   </div>
   <div id="con_ggfw_2" style="display:none;">
   
   <span class="menuColor"><a href="#" onclick="setDiv('ggfw',1,2);"> &lt;&lt; </a></span>
   </div>
    </td>
  </tr>
</tbody></table>

<!--table width="98%" border="0" cellspacing="0" cellpadding="0" align="center" id="con_one_6" style="display:none">
  <tr>
    <Td height="35">
   
			
				<a href="../../../../yhly/syjd/">首页焦点</a>  |
			
   
			
				<a href="../../../../yhly/lydt/">旅游动态</a>  |
			
   
			
				<a href="../../../../yhly/jdyh/">解读余杭</a>  |
			
   
			
				<a href="../../../../yhly/wzyh/">玩在余杭</a>  |
			
   
			
				<a href="../../../../yhly/rdtj/">热点推荐</a>  |
			
   
			
				<a href="../../../../yhly/jdlx/">经典路线</a>  |
			
   
			
				<a href="../../../../yhly/lxbz/">旅行帮助</a>  |
			
   
			
				<a href="../../../../yhly/lyjq/">旅游节庆</a>  |
			
   
			
				<a href="../../../../yhly/lxgl/">旅行攻略</a>  |
			
   
    </Td>
  </tr>
</table-->
<span id="con_one_0" style="display:none"></span>




<!--标签切换二级-->
    </td>
    <td width="5">
     
    </td>
  </tr>
</tbody></table>
    <table width="1000" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td height="6"></td>
  </tr>
</tbody></table>
<!--head-->
<table width="988" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td class="ZjYhN03 xxGK015" height="550" width="232" valign="top">
      <table width="100%" cellspacing="0" cellpadding="0" border="0" background="../../../../images/xxGKn019.jpg">
       <tbody><tr>
         <td class="yhZFNu013 xxGK03" height="33" align="center">信息公开</td>
       </tr>
      </tbody></table>
     <table width="100%" cellspacing="0" cellpadding="0" border="0">
      <tbody><tr>
       <td height="9"></td>
      </tr>
     </tbody></table>
<table width="180" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td class="xxGK014"><a href="../../">公告公示</a></td>
  </tr>
  <tr><td height="10"></td></tr>
 
 <tr>
<td class="CHANNELID_613" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../zbgg/">招标公告</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td>  <div id="ID_615" style="display:none">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../zbgg/zfcg/">采购项目</a> </div></td>	
</tr>



 <tr>
<td>  <div id="ID_827" style="display:none">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../zbgg/jsgc/">建设工程</a> </div></td>	
</tr>



 <tr>
<td class="CHANNELID_614" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../zbggs/">中标公告</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td>  <div id="ID_826" style="display:none">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../zbggs/zfcg1/">采购项目</a> </div></td>	
</tr>



 <tr>
<td>  <div id="ID_828" style="display:none">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../zbggs/jsgc1/">建设工程</a> </div></td>	
</tr>



 <tr>
<td class="CHANNELID_12689" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../rsrc/">人事人才</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_12678" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../jypx/">教育培训</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_379" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../gdfw/">供电</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_378" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../gsfw/">供水</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_625" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../xf/">信访</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_12690" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../ws/">卫生</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_12691" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../zf/">住房</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_617" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../">土地</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_12692" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../jt/">交通</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_624" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../hbgg/">环保</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_12693" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../js/">建设</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_825" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../hb/">征集</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

 <tr>
<td class="CHANNELID_626" height="10">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../../../../images/ZjYhN018.gif">&nbsp;<a href="../../qt/">其他</a></td>	
</tr>
<tr><td height="10"></td></tr>

 

</tbody></table>
<script language="javascript">

</script>

    </td>
    <td class="ZjYhN014" width="756" valign="top">
     <table width="100%" cellspacing="0" cellpadding="0" border="0" background="../../../../images/ZjYhN06.gif">
  <tbody><tr>
    <td height="29" width="4%" align="center"><img src="../../../../images/ZjYhN017.gif"></td>
    <td width="96%">当前位置：<a href="../../../../" target="_blank" class="CurrChnlCls">首页</a>&nbsp;&gt;&nbsp;<a href="../../../" target="_blank" class="CurrChnlCls">信息公开</a>&nbsp;&gt;&nbsp;<a href="../../" target="_blank" class="CurrChnlCls">公告公示</a>&nbsp;&gt;&nbsp;<a href="../" target="_blank" class="CurrChnlCls">土地</a></td>
  </tr>
</tbody></table>
   
<table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td class="GgFwN015" height="45" align="center">余政储出【2017】14、15号国有建设用地使用权挂牌出让公告</td>
  </tr>
</tbody></table>
<table width="97%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td height="5" background="../../../../images/GgFwN013.gif"></td>
  </tr>
  <tr><td class="GgFwN016" height="35" align="center">发布时间：2017-08-02    来源：国土余杭分局&nbsp;点击率：<span id="hiscount">1575</span></td></tr>
</tbody></table>


<table style="table-layout: fixed; word-break: break-all;overflow: hidden;" class="ZjYhN019 ZjYhN020" width="95%" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td> 
<div class="TRS_Editor">
    <style type="text/css">.TRS_Editor P{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}.TRS_Editor DIV{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}.TRS_Editor TD{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}.TRS_Editor TH{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}.TRS_Editor SPAN{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}.TRS_Editor FONT{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}.TRS_Editor UL{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}.TRS_Editor LI{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}.TRS_Editor A{margin-top:10px;margin-bottom:10px;line-height:2;font-family:宋体;font-size:10.5pt;}</style><div class="TRS_Editor"><p><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; 根据国家有关法律、法规的规定，依据城市规划，经杭州市人民政府批准，杭州市国土资源局余杭分局对下列地块采用挂牌方式出让。现将有关事宜公告如下：<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>一、挂牌出让地块位置及规划指标概况：</span></span></p><p align="center"></p><table style="width: 417.75pt; border-collapse: collapse; margin-left: 6.75pt; margin-right: 6.75pt; mso-table-layout-alt: fixed; mso-padding-alt: 0.0000pt 5.4000pt 0.0000pt 5.4000pt" class="MsoNormalTable">    <tbody>        <tr style="height: 32.9pt">            <td style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; padding-bottom: 0pt; padding-left: 5.4pt; width: 52.85pt; padding-right: 5.4pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: 0.5000pt solid windowtext; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="70" valign="middle">            <p style="text-align: center; line-height: 14pt; mso-line-height-rule: exactly" class="MsoBodyText"><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-spacerun: 'yes'; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">地块</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-spacerun: 'yes'; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">&nbsp;&nbsp;</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-spacerun: 'yes'; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">编号</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 85.2pt; padding-right: 5.4pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="113" valign="middle">            <p style="text-align: center; line-height: 14pt; mso-line-height-rule: exactly" class="MsoBodyText"><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-spacerun: 'yes'; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">地块坐落</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 65.95pt; padding-right: 5.4pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="87" valign="middle">            <p style="text-align: center; line-height: 14pt; mso-line-height-rule: exactly" class="MsoBodyText"><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-spacerun: 'yes'; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">出让面积</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            <p style="text-align: center; line-height: 14pt; mso-line-height-rule: exactly" class="MsoBodyText"><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">（</span><span style="font-family: 黑体; font-size: 12pt; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt; mso-ascii-font-family: 'Times New Roman'; mso-hansi-font-family: 'Times New Roman'">M</span><span style="font-family: 黑体; font-size: 12pt; vertical-align: super; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt; mso-ascii-font-family: 'Times New Roman'; mso-hansi-font-family: 'Times New Roman'">2</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">）</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 75pt; padding-right: 5.4pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="100" valign="middle">            <p style="text-align: center; line-height: 14pt; mso-line-height-rule: exactly" class="MsoBodyText"><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-spacerun: 'yes'; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">土地用途</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 75.75pt; padding-right: 5.4pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="101" valign="middle">            <p style="text-align: center; line-height: 14pt; mso-line-height-rule: exactly" class="MsoBodyText"><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-spacerun: 'yes'; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">地上建筑面积（</span><span style="font-family: 黑体; font-size: 12pt; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt; mso-ascii-font-family: 'Times New Roman'; mso-hansi-font-family: 'Times New Roman'">M</span><span style="font-family: 黑体; font-size: 12pt; vertical-align: super; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt; mso-ascii-font-family: 'Times New Roman'; mso-hansi-font-family: 'Times New Roman'">2</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">）</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 63pt; padding-right: 5.4pt; border-top: windowtext 0.5pt solid; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="84" valign="middle">            <p style="text-align: center; line-height: 14pt; mso-line-height-rule: exactly" class="MsoBodyText"><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-spacerun: 'yes'; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt">土地出让年限</span><span style="font-family: 宋体; font-size: 10.5pt; font-weight: bold; mso-bidi-font-family: 'Times New Roman'; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>        </tr>        <tr style="page-break-inside: avoid; height: 68.75pt">            <td style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; padding-bottom: 0pt; padding-left: 5.4pt; width: 52.85pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: 0.5000pt solid windowtext; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="70" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">余政储出〔201</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt">7</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">〕&nbsp;</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">14</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt">号</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 85.2pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="113" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">临平新城</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">（临平新城</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">杭乔路以东、天万路以北</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">拟招拍挂</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">地块</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">）；</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">东至规划支路、南至天万路、西至杭乔路、北至翁梅街</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 65.95pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="87" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'">64505</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 75pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="100" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'">商住用地</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 75.75pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="101" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'">141911</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 63pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="84" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">70年、&nbsp;&nbsp;40年</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>        </tr>        <tr style="page-break-inside: avoid; height: 68.75pt">            <td style="border-bottom: windowtext 0.5pt solid; border-left: windowtext 0.5pt solid; padding-bottom: 0pt; padding-left: 5.4pt; width: 52.85pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: 0.5000pt solid windowtext; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="70" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">余政储出〔201</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt">7</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">〕&nbsp;</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">15</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt">号</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 85.2pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="113" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">良渚街道</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt">（</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">良渚街道古墩路北、郎斗路东住宅地块</span><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">）；东至张家坝港、南至古墩路、西至郎斗路、北至玉鸟路</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 65.95pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="87" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'">53212</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 75pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="100" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'">住宅用地</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 75.75pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="101" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'">133030</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt; mso-hansi-font-family: 'Times New Roman'"><o:p></o:p></span></p>            </td>            <td style="border-bottom: windowtext 0.5pt solid; border-left: medium none; padding-bottom: 0pt; padding-left: 5.4pt; width: 63pt; padding-right: 5.4pt; border-top: medium none; border-right: windowtext 0.5pt solid; padding-top: 0pt; mso-border-left-alt: none; mso-border-right-alt: 0.5000pt solid windowtext; mso-border-top-alt: 0.5000pt solid windowtext; mso-border-bottom-alt: 0.5000pt solid windowtext" width="84" valign="middle">            <p style="text-align: center" class="MsoNormal"><span style="font-family: 宋体; font-size: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">&nbsp;70年</span><span style="font-family: 宋体; font-size: 10.5pt; mso-font-kerning: 1.0000pt"><o:p></o:p></span></p>            </td>        </tr>    </tbody></table><p></p><!--EndFragment--><p><span style="font-size: 16px"><span style="font-family: 宋体"><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>注：上述宗地具体情况以《挂牌出让文件》和出让合同为准。<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>二、挂牌出让土地受让对象：凡中华人民共和国境内自然人、法人、其他组织均可参加国有建设用地使用权挂牌出让活动。境外企业要求参加竞买的，可先在境内依法设立公司，也可直接参加竞买。具体竞买申请要求详见挂牌出让文件。<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>竞得者必须严格按照土地出让合同规定的条件进行开发建设（每一幅地块参加竞价的条件和规划条件详见各宗地挂牌文件）。<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>三、竞买人确定方式：本次挂牌出让地块设定土地上限价格；当土地竞价溢价率达到50%时，不再接受更高报价，转入竞投自持比例；当有两个或两个以上的竞买人投报自持面积比例为100%时，转入现场投报配建养老服务用房面积的程序并按投报面积最高确定竞得人。具体详见地块挂牌出让文件。<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>四、本次挂牌出让地点<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>本次土地挂牌报名、报价地点：杭州市余杭区公共资源交易中心，详细地址：余杭区临平南大街265号时代广场市民之家二楼H16窗口。咨询电话：0571-89360802。挂牌现场会地点：杭州市余杭区公共资源交易中心，详细地址：余杭区临平南大街265号时代广场市民之家三楼。咨询电话：0571-89360802<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>五、本次挂牌报价时间自2017年8月23日 9:00起至2017年9月1日14:30 止（工作时间）。<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>报名时间：参加挂牌竞买的竞买人可在 2017年8月23日9:00至2017年9月1日11：45（工作时间）提交挂牌须知规定应提交的有关文件，并填写挂牌出让报名表，向杭州市国土资源局余杭分局缴纳保证金（以到账为准）后，办理挂牌申请手续。<br><span style="font-size: 16px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp; </span></span>六、本次挂牌出让详细资料请参阅挂牌出让文件。有关挂牌出让文件资料可自2017年8月14日后到杭州市余杭区公共资源交易中心（余杭区临平南大街265号时代广场市民之家二楼）H16号窗口索取。</span></span></p><p style="text-align: right"><span style="font-size: 16px"><span style="font-family: 宋体">杭州市国土资源局余杭分局、杭州市余杭区公共资源交易中心<br>2017年8月2日</span></span></p></div></div>	<table width="100%">
	 
	 
	  
	 <!--
	 -->
	</table>
	
    </td>
  </tr>
</tbody></table>

<table style="display:none;" id="zxplhead" width="90%" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td>
    <table width="678" cellspacing="0" cellpadding="0" border="0" align="center">
    <tbody><tr><td colspan="2" height="5"></td></tr>
  <tr>
    <td class="CyYhN07 GgFwN019" height="35" width="10%" align="center">在线评论</td>
    <td class="CyYhN07 GgFwN019" width="90%">&nbsp;</td>
  </tr>
</tbody></table>    
<div id="zxpl" style="display:none;">
<form name="newscomment" action="http://www.yuhang.gov.cn/comment/comment?newsid=1095855&amp;encoding=UTF-8&amp;data=ABC4rwAAAAcAAANkAAAAAQBN5L2Z5pS_5YKo5Ye644CQMjAxN-OAkTE044CBMTXlj7flm73mnInlu7rorr7nlKjlnLDkvb_nlKjmnYPmjILniYzlh7rorqnlhazlkYoAAAAAAAAAAAAAAC4wLAIUH7qXO48b1Au58GouIzH2QedaBIUCFCI-TRH9VpPmIjVGys0sVAZnSAuW" method="post"> 
<table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr><td colspan="5" height="5"></td></tr>
  <tr>
    <td height="27" width="10%">用户昵称：</td>
    <td width="20%"><input name="nickname" class="GgFwN021" type="text"></td>
    <td width="4%"><input value="1" name="anonymous" type="checkbox"></td>
    <td width="57%">匿名(如选择匿名发表观点时，您的昵称将不出现在评论列表中)</td>
    <td width="9%">&nbsp;</td>
  </tr>
</tbody></table>
<table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  <td colspan="5" height="88"><p>&nbsp;请遵纪守法并注意语言文明（字数在200字内） </p>
    <p>
      <textarea name="content" rows="18" cols="60" class="GgFwN022"></textarea>
    </p></td>
  </tr>
</tbody></table>
<table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td height="40" width="10%">验证码：</td>
    <td width="20%">
    <input id="txtCheckingCode" name="CheckingCode" value="" class="GgFwN021" type="text">&nbsp;
				
				<input name="FromJSP" value="1" type="hidden">
    </td>
    <td width="11%"><img style="display:" alt="验证码" id="imgCheckout" src="http://www.yuhang.gov.cn/comment/cn/randCodeGen.jsp" border="0" align="absmiddle"></td>
    <td width="7%"><input value="发表" type="submit">
                    <input name="anonymous" value="0" type="hidden"> 
					<input name="action" value="post" type="hidden">
				    <input name="my_encoding" value="UTF-8" type="hidden"></td>
    <td width="52%"><a style="color:#ff0000;" target="_blank" href="http://www.yuhang.gov.cn/comment/comment?newsid=1095855&amp;encoding=UTF-8&amp;data=ABC4rwAAAAcAAANkAAAAAQBN5L2Z5pS_5YKo5Ye644CQMjAxN-OAkTE044CBMTXlj7flm73mnInlu7rorr7nlKjlnLDkvb_nlKjmnYPmjILniYzlh7rorqnlhazlkYoAAAAAAAAAAAAAAC4wLAIUWa1Cwj6u7nqwmMg4nqlBvQ65WQACFHDZu22IEBNxG-fiu91LctXxnaPR">【查看评论】</a></td>
  </tr>
</tbody></table>
</form>
</div>
<table id="zck" style="display:none;" width="100%" cellspacing="0" cellpadding="0" border="0">
<tbody><tr>
<td height="15"></td>  
</tr>
<tr>
<td><a style="color:#ff0000;" target="_blank" href="http://www.yuhang.gov.cn/comment/comment?newsid=1095855&amp;encoding=UTF-8&amp;data=ABC4rwAAAAcAAANkAAAAAQBN5L2Z5pS_5YKo5Ye644CQMjAxN-OAkTE044CBMTXlj7flm73mnInlu7rorr7nlKjlnLDkvb_nlKjmnYPmjILniYzlh7rorqnlhazlkYoAAAAAAAAAAAAAAC4wLAIUWdQj9kWifPl01rjkruIQqKtUOaYCFFcd1GKBFJB-D5xWm6jrZzKU8419">【查看评论】</a> </td>  
</tr>

</tbody></table>

    <script>
         var zxpl= "";
 	if("打开"==zxpl){         
         document.getElementById("zxplhead").style.display = "block";
    	document.getElementById("zxpl").style.display = "block";
	}else if("只查看"==zxpl){
         document.getElementById("zxplhead").style.display = "block";
         document.getElementById("zck").style.display = "block";
         }
    </script>



<table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td height="10"></td>
  </tr>
</tbody></table>

    </td>
  </tr>
</tbody></table>


<table class="GgFwN017" width="97%" cellspacing="0" cellpadding="0" border="0">
<tbody><tr>
   <td height="20" align="center"><script language="JavaScript">
&lt;!--
function createPageHTML(_nPageCount, _nCurrIndex, _sPageName, _sPageExt){
 if(_nPageCount == null || _nPageCount&lt;=1){
  return;
 }

 var nCurrIndex = _nCurrIndex || 0;
 // 1 输出首页和上一页
 // 1.1 当前页是首页
 if(nCurrIndex == 0){
  document.write("&lt;span&gt;上一页 &lt;/span&gt;&lt;span&gt;【1】&lt;/span&gt;");
 }
 //1.2 当前页不是首页
 else{
  var nPreIndex = nCurrIndex - 1;
  var sPreFileExt = nPreIndex == 0 ? "" : ("_" + nPreIndex);

  
  document.write("&lt;a href=\"" + _sPageName + sPreFileExt + "."+_sPageExt+"\"&gt;上一页 &lt;/a&gt;");
  document.write("&lt;a href=\""+_sPageName+"."+_sPageExt+"\"&gt;【1】&lt;/a&gt;");
 }

 // 2 输出中间分页
 for(var i=1; i&lt;_nPageCount; i++){
  if(nCurrIndex == i)
   document.write("&amp;nbsp;&lt;span&gt;"+(i+1) + "&lt;/span&gt;");
  else
   document.write("&amp;nbsp;&lt;a href=\""+_sPageName+"_" + i + "."+_sPageExt+"\"&gt;【"+(i+1)+"】&lt;/a&gt;");
 }

 // 3 输出下一页和尾页
 // 3.1 当前页是尾页
 if(nCurrIndex == (_nPageCount-1)){
  document.write("&lt;span&gt; 下一页&lt;/span&gt;");
 }
 // 3.2 当前页不是尾页
 else{
  var nNextIndex = nCurrIndex + 1;
  var sPreFileExt = nPreIndex == 0 ? "" : ("_" + nPreIndex);

  document.write("&lt;a href=\""+_sPageName+"_" + nNextIndex + "."+_sPageExt+"\"&gt; 下一页&lt;/a&gt;&amp;nbsp;");
  
 }
}
//--&gt;
</script>
<script>createPageHTML(1, 0, "t20170803_1095855", "html")</script></td>
</tr>
  <tr><td height="45" align="right"><a href="#">【返回顶部】</a> <a href="javascript:window.print();">【打印本页】</a> <a onclick="window.close()" href="#">【关闭窗口】</a></td></tr>
</tbody></table>

<table class="ZjYhN019 ZjYhN020" width="93%" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td> 
    <font size="2.5pt">相关新闻：</font>
    </td>
  </tr>
  <tr>
  <td align="center">
  
		<script>
                    var newNum = 0;
                </script>
		<table class="ZjYhN019 ZjYhN020" width="95%" border="0" align="center">
		  
		  <tbody><tr>
		    
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201707/t20170721_1094492.html" title="临平老城区有机更新一期工程测绘工作招标公告"&gt;临平老城区有机更新一期工程测绘工作招...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201707/t20170721_1094492.html" title="临平老城区有机更新一期工程测绘工作招标公告"&gt;临平老城区有机更新一期工程测绘工作招...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		     
            
                       <script>	

			var chname='186';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../zjyh/jryh/mnews/201707/t20170713_1093453.html" title="现房销售取消 杭州主城宅地挂牌启用新规则"&gt;现房销售取消 杭州主城宅地挂牌启用新规则&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../zjyh/jryh/mnews/201707/t20170713_1093453.html" title="现房销售取消 杭州主城宅地挂牌启用新规则"&gt;现房销售取消 杭州主城宅地挂牌启用新规则&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script></tr><tr><td width="50%" align="left"><li><font size="2pt"><a href="../../../../zjyh/jryh/mnews/201707/t20170713_1093453.html" title="现房销售取消 杭州主城宅地挂牌启用新规则">现房销售取消 杭州主城宅地挂牌启用新规则</a></font></li></td>	            
			
		     
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201707/t20170712_1093268.html" title="余政储出【2017】9、10号国有建设用地使用权挂牌出让公告"&gt;余政储出【2017】9、10号国有建设用地使...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201707/t20170712_1093268.html" title="余政储出【2017】9、10号国有建设用地使用权挂牌出让公告"&gt;余政储出【2017】9、10号国有建设用地使...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		     
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201707/t20170711_1093122.html" title="余政储出【2017】11、12、13号国有建设用地使用权挂牌出让公告"&gt;余政储出【2017】11、12、13号国有建设...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201707/t20170711_1093122.html" title="余政储出【2017】11、12、13号国有建设用地使用权挂牌出让公告"&gt;余政储出【2017】11、12、13号国有建设...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		     
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170619_1090327.html" title="余政储出[2017]8号地块挂牌结果公示"&gt;余政储出[2017]8号地块挂牌结果公示&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170619_1090327.html" title="余政储出[2017]8号地块挂牌结果公示"&gt;余政储出[2017]8号地块挂牌结果公示&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		     
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170620_1090401.html" title="关于对《余杭区仓前街道梦想小镇安置区块选址论证报告》进行公示的说明"&gt;关于对《余杭区仓前街道梦想小镇安置区...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170620_1090401.html" title="关于对《余杭区仓前街道梦想小镇安置区块选址论证报告》进行公示的说明"&gt;关于对《余杭区仓前街道梦想小镇安置区...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		     
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170616_1090103.html" title="余政储出[2017]7号地块挂牌结果公示"&gt;余政储出[2017]7号地块挂牌结果公示&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170616_1090103.html" title="余政储出[2017]7号地块挂牌结果公示"&gt;余政储出[2017]7号地块挂牌结果公示&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		     
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170619_1090163.html" title="中建首入临平新城以自持5%拿下临平新城西区块L-41地块"&gt;中建首入临平新城以自持5%拿下临平新城...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170619_1090163.html" title="中建首入临平新城以自持5%拿下临平新城西区块L-41地块"&gt;中建首入临平新城以自持5%拿下临平新城...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		     
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170613_1089480.html" title="余政储出[2017]6号地块挂牌结果公示"&gt;余政储出[2017]6号地块挂牌结果公示&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201706/t20170613_1089480.html" title="余政储出[2017]6号地块挂牌结果公示"&gt;余政储出[2017]6号地块挂牌结果公示&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		     
            
                       <script>	

			var chname='868';
			if(chname!=868 &amp;&amp; chname!=2566){
                                newNum = newNum + 1;
                                if(newNum % 2 ==0){
				     document.write(
				     '&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201705/t20170525_1087665.html" title="国土分局主动上门对接征迁清零和土地出让工作"&gt;国土分局主动上门对接征迁清零和土地出...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );
                                }else{
                                    document.write(
				     '&lt;/tr&gt;&lt;tr&gt;&lt;td align="left" width="50%"&gt;&lt;li&gt;&lt;font size="2pt" &gt;'+
				     '&lt;a href="../../../../index/oatest/201705/t20170525_1087665.html" title="国土分局主动上门对接征迁清零和土地出让工作"&gt;国土分局主动上门对接征迁清零和土地出...&lt;/a&gt;'+
				     '&lt;\/font&gt;&lt;\/li&gt;&lt;\/td&gt;	'
				     );                                
                                }
			}else{document.write('')}	
		
			</script>            
			
		   
		   </tr>
			
		</tbody></table>	
		
  </td>
  </tr>
</tbody></table>




    </td>
  </tr>
</tbody></table>
    <table width="1000" cellspacing="0" cellpadding="0" border="0" align="center">
  <tbody><tr>
    <td height="6"></td>
  </tr>
</tbody></table>
<!--foot-->
<table width="1000" cellspacing="0" cellpadding="0" border="0" bgcolor="#cfcfcf" align="center">
  <tbody><tr>
    <td height="33" align="center">
    <a href="../../../../wzxx/sitemap/" target="_blank">网站地图</a>  |  <a href="../../../../wzxx/aboutus/" target="_blank">关于我们</a>  |  <a href="../../../../wzxx/statement/" target="_blank">郑重声明</a>  |  <a href="../../../../wzxx/privacy/" target="_blank">隐私保护</a>  |  <a href="../../../../wzxx/sitehelp/" target="_blank">使用帮助</a>  |  <a href="../../../../wzxx/yjzj/" target="_blank">网站意见征集</a></td>
  </tr>
</tbody></table>
<table class="xxGK012 yhZFNu014" width="1000" cellspacing="0" cellpadding="0" border="0" align="center">
<tbody><tr><td height="10"></td></tr>
  <tr>
    <td height="30" align="center">杭州市余杭区委、区人大、区政府、区政协主办 杭州市余杭区信息化管理中心 承办 备案编号：浙ICP备05000021</td>
  </tr>
    <tr>
    <td height="30" align="center">建议使用IE6.0以上浏览器，1024*768以上分辨率浏览
    <script type="text/javascript">
var cnzz_protocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cspan id='cnzz_stat_icon_1000062031'%3E%3C/span%3E%3Cscript src='" + cnzz_protocol + "s22.cnzz.com/z_stat.php%3Fid%3D1000062031%26show%3Dpic' type='text/javascript'%3E%3C/script%3E"));
</script><span id="cnzz_stat_icon_1000062031"><a href="http://www.cnzz.com/stat/website.php?web_id=1000062031" target="_blank" title="站长统计"><img src="http://icon.cnzz.com/img/pic.gif" hspace="0" vspace="0" border="0"></a></span><script src=" http://s22.cnzz.com/z_stat.php?id=1000062031&amp;show=pic" type="text/javascript"></script><script src="http://c.cnzz.com/core.php?web_id=1000062031&amp;show=pic&amp;t=z" charset="utf-8" type="text/javascript"></script>
    </td>
  </tr>
  <tr><td height="10"></td></tr>
</tbody></table>
<script type="text/javascript" src="../../../../images/jquery-1.8.3.min.js"></script>
<script>
jQuery(function() {
if(jQuery("#hiscount").length&gt;0){
jQuery.ajax({
type : 'POST',
url : "/wcm/XMail/hitsstat.jsp",
dataType : 'json',
data : 'docId=1095855',
success : function(data) {
if (data == "fail") {
//加载失败
jQuery("#hiscount").html(0);
} else {
//加载成功
jQuery("#hiscount").html(data);
}
},
error : function(data) {
jQuery("#hiscount").html(0);
}
});
}
});
</script>
<!--foot-->
    
    </td>
  </tr>
</tbody></table>
    </div>

</body>"""
    bs_obj = bs4.BeautifulSoup(s,'html.parser')
    print spider_func.df_output(bs_obj,'511699','onsell')
