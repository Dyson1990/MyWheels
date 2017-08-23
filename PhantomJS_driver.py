# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: PhantomJS_driver.py
    @time: 2017/8/23 15:56
--------------------------------
"""
import sys
import os
import selenium.webdriver

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')


class PhantomJS_driver(object):
    def __init__(self):
        pass

    def initialization(self):
        # 初始化浏览器
        desired_capabilities = selenium.webdriver.DesiredCapabilities.PHANTOMJS.copy()

        for key, value in self.headers.iteritems():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        desired_capabilities['phantomjs.page.customHeaders.User-Agent'] ='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

        return selenium.webdriver.PhantomJS(desired_capabilities=desired_capabilities)

    def get_html(self, url):
        driver = self.initialization()
        driver.get(url)
        return driver.page_source

if __name__ == '__main__':
    pass