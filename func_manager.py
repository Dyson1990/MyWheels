# -*- coding:utf-8 -*-  

import bs4
import requests_manager

mod_dict = {
    "bs4":bs4,
    "requests_manager":requests_manager
}

class func_manager(object):
    def get_func(self, s):
        # 分解类似bs4.BeautifulSoup.get_text这样中间不需要参数的函数
        func_list = s.split(".")
        func = mod_dict[func_list[0]]
        if len(func_list) == 1:
            return func
        else:
            for s in func_list[1:]:
                func = getattr(func, s)
        return func

    def run_func(self, s, args):
        """
        分解类似bs4.BeautifulSoup(str, 'html.parser').find('td', attrs={"class":"normal"})这样中间需要参数的函数

        args = {
           "BeautifulSoup":{
               "l":["str", 'html.parser']
           } ,
           "find":{
               "l":['td'],
               "d":{
                   "attrs":{"class":"normal"}
               }
           }
        }
        """
        func_list = s.split(".")
        func = mod_dict[func_list[0]]
        if len(func_list) == 1:
            return func
        else:
            for s in func_list[1:]:
                func = getattr(func, s)

                if "l" not in args[s]:
                    l = []
                else:
                    l = args[s]["l"]
                if "d" not in args[s]:
                    d = {}
                else:
                    d = args[s]["d"]

                func = func(*l,**d)
        return func

if __name__ == "__main__":
    func_manager = func_manager()
    s = """'<p>\n\t<span style="font-size:14px;"><strong>\xe6\x95\x99\xe6\x8e\x88\xe5\xb2\x97</strong></span><span style="font-size:14px;">\xef\xbc\x9a</span> \n</p>'"""
    #bs4.BeautifulSoup(s,'html.parser').find('td', "attrs": {"class": "normal"})
    args = {
        "BeautifulSoup": {
            "l": [s, 'html.parser']
        },
        "find": {
            "l": ['span'],
            "d": {
                "attrs": {"style": "font-size:14px;"}
            }
        }
    }
    print func_manager.run_func("bs4.BeautifulSoup.find", args)

