# author = weizhang
# time: 2022/6/2 22:52
import json
from common.log_util import logger
import jsonpath


class RelationExtract(object):
    """
    关联提取做全局变量
    从响应结果当中，提取值，并设置为全局变量(Data类作为本框架的全局变量类)
    1、提取表达式：放在excel当中
       (可能提取1个，可能提取多个。。以表达式个数为准)
    2、提取出来之后，设置为Data类属性
    """

    def __init__(self, response_json, response, data_obj, key, value):
        """
        初始化数据
        :param extract_epr: 提取表达式（字典形式的字符串'{"key":"value"}'，其中key为全局变量名，value为jsonpath表达式）
        :param response_json: json格式响应数据
        :param data_obj: 设置全局变量类（默认为Data类）
        :param response: 【全】响应数据（包含响应头数据）
        :param key:
        """

        self.response_json = response_json
        self.response = response
        self.data_obj = data_obj
        self.key = key
        self.value = value

    def extract_responseheaders_token(self):
        """
        提取响应头中token
        :return:
        """
        response_headers_token = self.response.headers["token"]
        logger.info("提取响应头中token为：{}".format(response_headers_token))

        # 存储data_obj对象中key属性为response_headers_token
        setattr(self.data_obj, self.key, str(response_headers_token))

    def extract_responseheaders_contenttype(self):
        """
        提取响应头中content-type
        :return:
        """
        response_headers_contenttype = self.response.headers["Content-Type"]
        logger.info("提取响应头中token为：{}".format(response_headers_contenttype))

        # 存储data_obj对象中key属性为response_headers_contenttype
        setattr(self.data_obj, self.key, str(response_headers_contenttype))

    def extract_response(self):
        """
        提取响应结果中数据
        :return:
        """
        # 提取响应结果中值做接口关联入参（jsonpath提取：提取成功返回列表，提取失败返回False）
        extract_result = jsonpath.jsonpath(self.response_json, self.value)

        # 提取成功设置为Data类的属性（key是全局变量名，result[0]就是提取后的值）
        if extract_result:
            if isinstance(extract_result[0], dict):
                # 如果提取的结果是字典，则转换为json字符串
                extract_result = json.dumps(extract_result[0])
                logger.info("响应数据提取值为:{}".format(extract_result))
                setattr(self.data_obj, self.key, str(extract_result))
            else:
                logger.info("响应数据提取值为:{}".format(extract_result[0]))
                setattr(self.data_obj, self.key, str(extract_result[0]))
        else:
            logger.info('******报错：响应数据提取值为空！******')
