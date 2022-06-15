# _*_ coding: utf-8 _*_

"""
响应断言类
"""
import json
import jsonpath


class Assert(object):
    """
    响应断言
    """

    def equals(self, expected_result, real_result):
        """
        响应断言相等判断
        :param real_result: 实际响应结果
        :param expected_result: 期望响应结果
        :return: 响应断言相等
        """
        return expected_result == real_result

    def contains(self, real_result, expected_result):
        """
        响应断言包含判断
        :param expected_result: 期望响应结果（需要断言的部分）
        :param real_result: 实际响应结果
        :return: 响应断言包含
        """
        return expected_result in real_result

    def re_matches(self, real_result, expected_result, json_path):
        """
        响应断言正则判断
        :param expected_result: 期望响应结果（需要断言的部分需正则表达式显示）
        :param real_result: 实际响应结果
        :param json_path: jsonpath表达式
        :return: 响应断言正则判断
        """

        # str数据转json数据
        result_json = json.loads(real_result)

        # jsonpath提取校验数据
        match = jsonpath.jsonpath(result_json, json_path)

        if match:
            if match[0] == expected_result:
                return True
            else:
                return False
        else:
            return False

