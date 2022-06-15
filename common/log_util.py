import os
import logging
from logging import Logger

from common.time_util import GetTime


class LoggerHandler(Logger):

    def __init__(self):
        get_today_time = GetTime().get_today()
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = os.path.join(basedir, "logs")
        # 日志名称和路径拼接
        log_file_name = os.path.join(log_dir, get_today_time + 'GMJK.log')
        file = log_file_name
        # 1、设置日志的名字、日志的收集级别
        super().__init__('GMJK', 'INFO')

        # 2、可以将日志输出到文件和控制台

        # 自定义日志格式(Formatter)
        fmt_str = "%(asctime)s %(name)s %(levelname)s %(filename)s [%(lineno)d] %(message)s"
        # 实例化一个日志格式类
        formatter = logging.Formatter(fmt_str)

        # 实例化渠道(Handle).
        # 控制台(StreamHandle)
        handle1 = logging.StreamHandler()
        # 设置渠道当中的日志显示格式
        handle1.setFormatter(formatter)
        # 将渠道与日志收集器绑定起来
        self.addHandler(handle1)

        if file:
            # 文件渠道(FileHandle)
            handle2 = logging.FileHandler(file, encoding="utf-8")
            # handle2 = ConcurrentRotatingFileHandler(file, maxBytes=20*1024*1024, backupCount=5,encoding="utf-8")
            # 设置渠道当中的日志显示格式
            handle2.setFormatter(formatter)
            self.addHandler(handle2)


logger = LoggerHandler()
