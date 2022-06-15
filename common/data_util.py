# _*_ coding: utf-8 _*_

"""
数据处理类（数据格式转换、json解析）
"""
from jsonpath_rw import parse
import json


class DataProcess(object):
    """
    数据处理类（数据格式转换、json解析）
    """

    def json_data_analysis(self, pattern, str_data):
        """
        获取接口响应结果返回的字段值
        :param pattern:
        :param str_data:
        :return:
        """
        # str_data数据转化为dict数据
        dict_data = json.loads(str_data)

        # 将pattern(提取接口响应结果返回字段的模式)转换为json格式（pattern举例：data[0].issue）
        json_exe = parse(pattern)  # 把我们需要的key值通过parse转换一下，即json_exe = parse(pattern)

        # 通过转换后的find方法到整个返回的数据中去寻找
        madle = json_exe.find(dict_data)

        # 通过以上得到的数据其实是一个各个值的路径，然后通过列表生成器取出来
        result = [math.value for math in madle]
        # for math in madle： 通过这个拿到的math是一个对象，该对象中会把要查找的value值单独列出来，同时也会把value值所在的路径一层一层列出来
        # math.value：当我们通过for循环拿到math的值后，然后通过“.”方式拿value的值，因为是列表生成器，此时拿到的是一个列表：[‘201110025’]。要拿到列表中的值，只需要通过下标就可以，如果存在多个值，就用不同的下标即可

        if result is None or result == []:
            return None
        else:
            return result[0]

    def str_to_json(self, strs):
        """
        序列化：将python对象编码成Json字符串
        :param strs: excel读取的数据，格式为str
        :return: Json字符串
        """
        result = json.dumps(strs, ensure_ascii=False, sort_keyss=True, indent=2)
        return result

    def json_to_str(self, jsons):
        """
        反序列化：将Json字符串解码成python对象
        :param jsons: Json字符串
        :return: excel读取的数据，格式为str
        """
        result = json.loads(jsons)
        return result


