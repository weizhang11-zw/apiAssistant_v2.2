import re
from common.global_data import Data
from faker import Faker
import time
from common.dataBase_util import MysqlDb
from common.log_util import logger


class Parametric(object):
    """
    参数化
    """

    def headers_parametric(self, headers_str, replaced_marks_list, data_obj):
        """
        请求头参数化（从全局变量Data类中获取属性变量的值）
        :param replaced_marks_list:
        :param headers_str: 请求头内容（str格式）
        :param marks_list: 请求头参数化全部变量列表
        :param data_obj: 全局变量Data类
        :return: 参数化处理后请求头
        """
        # 从全局变量Data类当中取值来替换标识符
        for index, mark in enumerate(replaced_marks_list):
            # 如果全局变量Data类有mark这个属性名
            if hasattr(data_obj, mark):
                # 使用全局变量Data类的mark属性值，去替换测试用例当中的#mark#
                headers_str = headers_str.replace("${{mark}}".replace("{mark}", mark), getattr(data_obj, str(mark)))

            else:
                logger.info('******报错：请求头%s的提取值为空！******' % mark)

        return headers_str

    def requestparam_parametric(self, requestparam_str, replaced_marks_list, data_obj):
        """
        请求体参数化
        1、固定全局变量的值（常见有：获取random随机数，获取time时间，获取数据库数据）
        2、全局变量Data类中获取属性变量的值
        :param requestparam_str:
        :param replaced_marks_list:
        :param data_obj:
        :return:
        """
        # 如果有random_str，则要生成一个随机数，然后再替换掉它
        if "random_str" in replaced_marks_list:
            # 生成随机数：今天的日期_20个随机字母
            cur_time = time.strftime("%Y%m%d", time.localtime())
            cur_str = Faker().pystr()
            random_str = cur_time + "_" + cur_str
            # logger.info(f"有${{random_str}}标识符，需要生成随机字符串: {random_str}")
            requestparam_str = requestparam_str.replace("${random_str}", random_str)

        elif "time" in replaced_marks_list:
            # 生成时间戳
            cur_time = str(time.time())
            # logger.info("有${{time}}标识符，需要生成随机字符串: {}".format(cur_time))
            requestparam_str = requestparam_str.replace("${time}", cur_time)

        # 遍历标识符mark，如果标识符是全局变量Data类的属性名，则用属性值替换掉mark
        for index, mark in enumerate(replaced_marks_list):
            # 如果全局变量Data类有mark这个属性名
            if hasattr(data_obj, mark):
                # 使用全局变量Data类的mark属性值，去替换测试用例当中的#mark#
                requestparam_str = requestparam_str.replace("${{mark}}".replace("{mark}", mark), getattr(data_obj, str(mark)))
                # 获取数据库中数据
            if "SELECT" in mark:
                result = MysqlDb().query_one(mark)[0]
                MysqlDb().close()
                logger.info("将标识符 {} 替换为 {}".format(mark, result))
                # 使用全局变量Data类的mark属性值，去替换测试用例当中的#mark#
                requestparam_str = requestparam_str.replace(f"${{mark}}".replace("mark", mark), str(result))

        return requestparam_str
