# _*_ coding: utf-8 _*_

import configparser
import os

"""
从配置文件中获取参数
"""


class ConfigEngine(object):
    """
    从配置文件中获取参数
    """

    @staticmethod
    def get_config(section, key):
        """
        读取配置文件对应数据
        :param section: config的section（字符串格式，举例：[Excel]）
        :param key: config的key(字符串格式，举例：excel_path =)
        :return: 返回对应数据（字符串格式）
        """
        # 获取配置文件地址（路径+文件名）
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(basedir, "conf")
        file_path = os.path.join(config_path, "config.ini")

        # 实例化
        config = configparser.ConfigParser()
        # 读取配置文件
        config.read(file_path, encoding='utf-8')
        # 获取读取结果
        result = config.get(section, key)

        return result
