# _*_ coding: utf-8 _*_

"""
响应断言类
"""
import re


class Assert(object):
    """
    响应断言
    """

    def equals(self, exp, result):
        """
        响应断言相等判断
        :param exp: 期望响应结果
        :param result: 实际响应结果
        :return: 响应断言相等
        """
        return exp == result

    def contains(self, result, target):
        """
        响应断言包含判断
        :param result: 实际响应结果
        :param target: 期望响应结果（需要断言的部分），举例：参考下方
        :return: 响应断言包含
        """
        return target in result

    def re_matches(self, result, pattern):
        """
        响应断言正则判断
        :param result: 实际响应结果
        :param pattern: 期望响应结果（需要断言的部分需正则表达式显示），举例：参考下方
        :return: 响应断言正则判断
        """

        # match(pattern, result) : 其中pattern为要校验的规则; result为要进行校验的字符串;
        match = re.match(pattern, result)  # 从左到右进行正则匹配（常用匹配规则：.*实际内容.*）

        if match is None:
            return False
        else:
            return True
