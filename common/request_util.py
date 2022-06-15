# _*_ coding: utf-8 _*_

"""
请求基础处理类
"""
import requests
from common.data_util import DataProcess


class Request(object):
    """
    接口请求封装方法
    """

    def __init__(self):
        """
        初始化
        """
        # 创建session会话对象（保存之前的会话信息cookies数据）
        self.res = requests.session()
        self.dataUtil = DataProcess()

    def do_get(self, url, params=None, headers=None):
        """
        get请求处理
        :param url: 请求url
        :param params: 请求体
        :param headers: 请求头
        :param cookies: 请求cookies
        :return: 响应数据
        """
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        # 先定义响应数据为空
        response = None

        response = self.res.get(url=url, params=params, verify=False, headers=headers)

        return response

    def do_post(self, url, param_type=None, request_param=None, headers=None):
        """
        json数据类型-post请求处理
        :param request_param:
        :param param_type:
        :param data:
        :param files:
        :param url: 请求url
        :param json: 请求体json格式
        :param headers: 请求头
        :return: 响应数据
        """

        if headers is None:
            headers = {}
        if request_param is None:
            request_param = {}

        # 先定义响应数据为空
        response = None

        # json类型（application/json数据格式）
        if param_type == 'json':
            response = self.res.post(url=url, json=request_param, verify=False, headers=headers)

        # 列表类型（application/x-www-form-urlencoded数据格式）和3、xml类型（text/xml数据格式）
        elif param_type == 'form_data':
            response = self.res.post(url=url, data=request_param, verify=False, headers=headers)

        # files文件类型（multipart/form-data数据格式）
        elif param_type == 'files':
            response = self.res.post(url=url, files=request_param, verify=False, headers=headers)

        return response

