import os

from common.time_util import GetTime


class Data(object):
    """
    参数化全局变量存储空间
    """
    t = GetTime()
    tomorrow_time = t.get_tomorrow()
    today_time = t.get_today()
    day_after_tomorrow = t.get_the_day_after_tomorrow()
    nowtime_greater_than_now = t.get_nowtime_greater_than_now()
    yesterday_time = t.get_yesterday()
