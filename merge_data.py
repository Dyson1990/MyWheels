# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: merge__data.py
    @time: 2017/9/7 14:50
--------------------------------
"""
import sys
import os
import pandas as pd

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')

class merge_data(object):
    def __init__(self):
        pass

    def get_filenames(self, path, extension):
        """返回一个文件夹下所有的对应扩展名的文件名"""
        all_files = os.listdir(path) # 全部文件名
        # 获取扩展名，筛选扩展名是不是所需要的
        #print [os.path.splitext(s)[1] for s in all_files]
        filenames = filter(lambda s:os.path.splitext(s)[1] == extension, all_files)
        # 合并路径和文件名
        return [os.path.join(path, s) for s in filenames]

    def merge_xls(self, filenames, output_path, output_filename):
        df = pd.DataFrame([])
        for filename in filenames:
            df = df.append(pd.read_excel(filename))
        df.index = range(df.shape[0])
        df.to_excel(os.path.join(output_path,output_filename))

if __name__ == '__main__':
    merge_data = merge_data()
    path = r'C:\Users\lenovo\Desktop\huzhou'
    filenames = merge_data.get_filenames(path, '.xls')
    merge_data.merge_xls(filenames, path, r'output.xls')
