# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: timer.py
    @time: 2017/7/20 11:01
--------------------------------
"""
import time
import os
import sched
import sys
import datetime

# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')

class mytimer(object):
    # 被周期性调度触发的函数
    def execute_command(self, cmd, inc):
        '''''
        终端上显示当前计算机的连接情况
        '''
        print u'报时：%s' % datetime.datetime.now()
        os.system(cmd)
        schedule.enter(inc, 0, self.execute_command, (cmd, inc))

    def cmd_timer(self, cmd, inc=60):
        # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
        # 给该触发函数的参数（tuple形式）
        schedule.enter(0, 0, self.execute_command, (cmd, inc))
        schedule.run()

if __name__ == '__main__':
    mytimer = mytimer()
    mytimer.cmd_timer("netstat -an", 60)
