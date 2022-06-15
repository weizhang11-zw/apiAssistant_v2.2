import datetime
import random
import re
import time


class GetTime(object):
    """
    获取各种时间
    """

    def get_today(self):
        """
        获取今天日期
        :return: 格式2022-05-26
        """
        today = time.strftime('%Y-%m-%d')
        return today

    def get_nowtime(self):
        """
        获取当前时间
        :return: 格式'%Y-%m-%d %H_%M_%S'
        """
        # 方法一：return time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time()))
        # 方法二：
        now_time = time.strftime('%Y-%m-%d %H_%M_%S')
        return now_time

    def get_nowtime_greater_than_now(self):
        """
        获取当前时间大于当前时间
        :return: 格式2022-05-25 16:43:37
        """
        now_time = datetime.datetime.now()
        now_time_greater_than_now = (now_time + datetime.timedelta(seconds=+500)).strftime('%Y-%m-%d %H:%M:%S')
        return now_time_greater_than_now

    def get_tomorrow(self):
        """
        获取明天日期
        :return: 格式2022-05-27
        """
        now_time = datetime.datetime.now()
        tomorrow = (now_time + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        return tomorrow

    def get_tomorrow_time(self):
        """
        获取明天时间
        :return: 格式2022-05-27 16:43:37.686947
        """
        now_time = datetime.datetime.now()
        tomorrow_time = (now_time + datetime.timedelta(days=+1)).strftime('%Y-%m-%d %H_%M_%S')
        return tomorrow_time

    def get_yesterday(self):
        """
        获取昨天日期
        :return: 格式2022-05-25
        """
        now_time = datetime.datetime.now()
        yesterday = (now_time + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
        return yesterday

    def get_yesterday_time(self):
        """
        获取昨天时间
        :return: 格式2022-05-25
        """
        now_time = datetime.datetime.now()
        yesterday_time = (now_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d %H_%M_%S')
        return yesterday_time

    def get_the_day_after_tomorrow(self):
        """
        获取后天日期
        :return: 格式2022-05-27
        """
        now_time = datetime.datetime.now()
        the_day_after_tomorrow = (now_time + datetime.timedelta(days=+2)).strftime("%Y-%m-%d")
        return the_day_after_tomorrow


if __name__ == '__main__':
    print(GetTime().get_the_day_after_tomorrow())
