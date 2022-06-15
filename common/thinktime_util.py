# author = weizhang
# time: 2022/5/31 13:55

from threading import Timer


class ThinkTime(object):
    """思考时间：测试用例之间的等待时间"""

    def __init__(self, func):
        """
        初始化
        :param set_time: 思考时间（秒，分，时）,格式整数
        :param func: 思考时间后执行的函数方法
        """
        """"""
        self.func = func

    def seconds(self, set_time):
        """
        自定义思考时间（单位：秒）
        :param set_time: X秒
        :return:
        """
        # 创建定时器
        s = Timer(int(set_time), self.func)
        # 使用线程方式执行
        s.start()
        # 等待线程执行结束
        s.join()

    def minute(self, set_time):
        """
        自定义思考时间（单位：分钟）
        :param set_time: X分钟
        :return:
        """
        s = Timer(int(set_time) * 60, self.func)
        s.start()
        s.join()

    def hour(self, set_time):
        """
        自定义思考时间（单位：小时）
        :param set_time: X小时
        :return:
        """
        s = Timer(int(set_time) * 3600, self.func)
        s.start()
        s.join()


# if __name__ == '__main__':
#     ThinkTime(GetTime().get_nowtime).minute(1)
