# _*_ coding: utf-8 _*_


"""
请求基础处理类（数据依赖处理、执行请求、结果解析）
"""
import unittest
from common.time_util import GetTime
from common.global_data import Data
from common.configparam_util import ConfigEngine
from common.relation_extract_util import RelationExtract
from common.request_util import Request
from common.excel_util import Excel
from common.data_util import DataProcess
from common.assert_util import Assert
from common.log_util import logger
from common.dataBase_util import MysqlDb
from common.parametric_util import Parametric
import re
from common.thinktime_util import ThinkTime


class RunCase(unittest.TestCase):
    """
    执行测试用例类（数据依赖处理、执行请求、结果解析）
    1、执行测试用例case请求
    2、测试结果断言
    """

    """定义常量，指定表格每一列"""
    CASE_ID = 1  # 用例编号
    MODULE_NAME = 2  # 项目名称
    CASE_NAME = 3  # 用例名称
    RUN_FLAG = 4  # 用例是否运行
    WAIT_TIME = 5  # 前置思考时间
    PRECONDITION_SQL = 6  # 前置条件
    URL = 7  # 接口url
    REQUEST_METHOD = 8  # 请求方法post/get
    HEADERS = 9  # 请求头
    PARAM_TYPE = 10  # 请求数据类型json/form_data/files
    REQUEST_PARAM = 11  # 请求体
    EXTRACT = 12  # 关联提取
    EXP_RESULT = 13  # 期望响应结果
    ASSET_TYPE = 14  # 断言类型
    ASSET_PATTERN = 15  # 断言规则

    def __init__(self, file_name, sheet_name=None, sheet_index=0):
        """
        初始化方法
        :param file_name:  excel的地址
        :param sheet_name:  Excel表sheet页的名称
        :param sheet_index:  Excel表sheet页的标识

        """
        super().__init__()
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.requestUtil = Request()
        self.excelUtil = Excel(file_name, sheet_name, sheet_index)
        self.dataUtil = DataProcess()
        self.assetUtil = Assert()
        self.get_nowTime = GetTime().get_nowtime()
        self.parametric = Parametric()

    def run_case_by_data(self, data):
        """
        执行测试用例case：格式：{"1":[test_001,订单,下单,www.baidu.com,xx,xx,]}
        :param data: 数据内容（当前使用：Excel表每条用例---每个用例数据按{"行号":[用例数据]}存储）
        :return: 断言判断结果并在Excel中记录最终结果
        """
        # 启动表的行位为第2行
        row_no = 2
        # 赋值key给行号
        for key in data:
            row_no = key
            break
        # 获取所有用例的行号
        row_data = data.get(row_no)

        # 获取所有的测试用例数据
        case_id = row_data[self.CASE_ID - 1]  # 获取用例编号
        module_name = row_data[self.MODULE_NAME - 1]  # 获取项目名称
        case_name = row_data[self.CASE_NAME - 1]  # 获取用例名称
        run_flag = row_data[self.RUN_FLAG - 1]  # 获取用例是否执行
        wait_time = row_data[self.WAIT_TIME - 1]  # 获取前置思考时间
        pre_sql = row_data[self.PRECONDITION_SQL - 1]  # 获取前置条件
        url = row_data[self.URL - 1]  # 获取执行用例的url
        request_method = row_data[self.REQUEST_METHOD - 1]  # 获取执行用例的请求类型
        headers = row_data[self.HEADERS - 1]  # 获取执行用例的请求头
        param_type = row_data[self.PARAM_TYPE - 1]  # 获取请求数据类型
        request_param = row_data[self.REQUEST_PARAM - 1]  # 获取执行用例的请求体
        exp_result = row_data[self.EXP_RESULT - 1]  # 获取期望响应结果
        asset_type = row_data[self.ASSET_TYPE - 1]  # 获取断言类型
        asset_pattern = row_data[self.ASSET_PATTERN - 1]  # 获取断言规则
        extract = row_data[self.EXTRACT - 1]  # 获取关联数据extract表达式（全局变量）

        logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logger.info("执行用例：%s-%s-%s" % (case_id, module_name, case_name))

        # 判断测试用例是否执行
        if run_flag == '否':
            # 用例不执行
            logger.info("******跳过：run_flag为否，该条测试用例不执行！******")
            self.skipTest("******跳过：run_flag为否，该条测试用例不执行！******")

        elif run_flag == '是':
            # 判断执行测试用例前是否有“思考时间（既等待时间）”
            self.think_time(wait_time, self.get_nowTime)

            # 判断执行测试用例前是否有“前置条件”
            self.precondition(pre_sql)
            # 获取处理后url
            url = self.url_handle(url)

            logger.info('请求类型：%s' % request_method)

            # 获取处理后请求头
            headers = self.headers_handle(headers, Data)

            logger.info("请求参数类型：%s" % param_type)

            # 获取处理后请求体
            request_param = self.requestparam_handle(request_param, param_type, Data)

            # 进行get请求
            if request_method == 'get':
                response = self.requestUtil.do_get(url, request_param, headers)

            # 进行post请求
            elif request_method == 'post':
                response = self.requestUtil.do_post(url, param_type, request_param, headers)

            else:
                logger.info('******报错：请求类型输入不正确！******')

            # 移出响应结果头尾空格
            response_text = response.text.strip()
            logger.info("断言类型：%s" % asset_type)
            logger.info("断言规则：%s" % asset_pattern)
            logger.info("期望响应结果：%s" % exp_result)
            logger.info("实际响应结果：%s" % response_text)

            # 响应数据提取为全局变量，供参数化使用
            self.relation_extract(extract, response.json(), response, Data)

            # 断言判断，记录最终结果
            result = self.asset_handle(exp_result, response_text, asset_type, asset_pattern, response)

            return result

        else:
            logger.info('******报错：执行状态输入不正确！******')

    def think_time(self, wait_time, func):
        """
        思考时间
        :param wait_time: 等待时间（单位：秒）
        :param func: 思考时间后执行的函数方法
        :return:
        """
        # 获取等待时间长度
        if wait_time:
            if int(wait_time):
                logger.info('前置思考时间为：%s秒' % int(wait_time))
                ThinkTime(func).seconds(wait_time)
            else:
                logger.info('******报错：前置思考时间输入不正确！******')
        else:
            logger.info('前置思考时间为空')

    def precondition(self, pre_sql):
        """
        前置条件（判断测试用例执行前是否有SQL前置条件）
        :return:
        """
        # 判断前置sql是否存在，存在则执行前置sql语句
        if pre_sql:
            # 新增数据库数据
            MysqlDb().insert(pre_sql)
            logger.info("前置条件：%s" % pre_sql)
        else:
            logger.info('前置条件为空')

    def url_handle(self, url):
        """
        url处理：用于切换不同测试环境
        1、url全称：host+path
        2、只有path
        :param url: url
        :return: url全称（host+path）
        """
        # 判断url是否全称（协议protocal + 域名host + 地址path）
        if url.startswith("https://") or url.startswith("http://"):
            url = url
            logger.info("请求URL：%s" % url)
        elif url is None:
            logger.info('******报错：URL输入为空！******')
        else:
            url = ConfigEngine.get_config('caseFileSetting', 'base_url_test') + url
            logger.info("请求URL：%s" % url)

        return url

    def headers_handle(self, headers, data_obj):
        """
        请求头处理
        :param headers: 请求头
        :param data_obj: 全局变量Data类
        :return: 处理后的请求头
        """
        if headers:
            # 第一步，把excel当中的一整个测试用例(excel当中的一行)转换成字符串
            headers_str = str(headers)

            # 第二步，利用正则表达式提取mark标识符（既全局变量Data类中属性名称，需保证提取变量名称和参数化引用名称一致）
            replaced_marks_list = re.findall("\${(.+?)}", headers_str)

            if replaced_marks_list:
                # 从全局变量Data类当中取值来替换标识符
                headers_str = self.parametric.headers_parametric(headers_str, replaced_marks_list, data_obj)

                # 切换字典格式
                headers = eval(headers_str)
                logger.info("请求头：%s" % headers)

            else:
                # 切换字典格式
                headers = eval(headers_str)
                logger.info("请求头：%s" % headers)
        else:
            logger.info("请求头为空")

        return headers

    def requestparam_handle(self, request_param, param_type, data_obj):
        """
        请求体参数处理
        :param param_type: 请求体类型（json/formdata/files）
        :param request_param: 请求体
        :param data_obj: 全局变量Data类
        :return: 处理后的请求体参数
        """
        # 第一步，把excel当中的一整个测试用例(excel当中的一行)转换成字符串
        headers_str = str(request_param)

        # 第二步，利用正则表达式提取mark标识符（既全局变量Data类中属性名称，需保证提取变量名称和参数化引用名称一致）
        replaced_marks_list = re.findall("\${(.+?)}", headers_str)

        if request_param:
            if param_type == "json":
                # 请求体参数化处理
                request_param = self.parametric.requestparam_parametric(request_param, replaced_marks_list, data_obj)
                # 将请求体数据序列化为JSON字符串（json.dumps()）
                request_param = self.dataUtil.json_to_str(request_param)
                logger.info("请求参数：%s" % request_param)

            elif param_type == 'form_data':
                # 请求体参数化处理
                request_param = self.parametric.requestparam_parametric(request_param, replaced_marks_list, data_obj)
                # data通过eval方法转换为字典格式
                request_param = eval(request_param)
                logger.info("请求参数：%s" % request_param)

            elif param_type == 'files':
                # 请求体参数化处理
                request_param = self.parametric.requestparam_parametric(request_param, replaced_marks_list, data_obj)
                # files通过eval方法转换为字典格式
                try:
                    request_param = eval(request_param)
                    logger.info("请求参数：%s" % request_param)
                except FileNotFoundError:
                    logger.info('******报错：上传文件不存在！******')

            # 考虑get请求-请求参数场景
            elif param_type is None:
                # 请求体参数化处理
                request_param = self.parametric.requestparam_parametric(request_param, replaced_marks_list, data_obj)
                # data通过eval方法转换为字典格式
                request_param = eval(request_param)
                logger.info("请求参数：%s" % request_param)

            else:
                logger.info('******报错：请求参数类型输入不正确！******')

        else:
            logger.info("请求参数为空")

        return request_param

    def relation_extract(self, extract_pre, response_json, response, data_obj):
        """
        创建关联全局变量，从响应数据中提取
        :param extract_epr: 提取表达式（字典形式的字符串'{"key":"value"}'，其中key为全局变量名，value为jsonpath表达式）
        :param response_json: json格式响应数据
        :param data_obj: 设置全局变量类（默认为Data类）
        :param response: 【全】响应数据（包含响应头数据）
        :return:
        """

        if extract_pre:
            # 1、从excel中读取的提取表达式，转成字典对象
            extract_dict = eval(extract_pre)

            # 2、遍历字典的key,value（key是全局变量名，value是jsonpath表达式）
            for key, value in extract_dict.items():
                # 提取响应头token，并存入Data全局变量中
                if "response_headers_token" in key:
                    RelationExtract(response_json, response, data_obj, key, value).extract_responseheaders_token()

                # 提取响应头content-type，并存入Data全局变量中
                elif "response_headers_contenttype" in key:
                    RelationExtract(response_json, response, data_obj, key, value).extract_responseheaders_contenttype()

                # 提取响应结果的数据
                else:
                    RelationExtract(response_json, response, data_obj, key, value).extract_response()

        else:
            logger.info('关联数据提取为空')

    def asset_handle(self, exp_result, response_text, asset_type, asset_pattern, res=None):
        """
        根据断言方式进行断言判断
        :param res: 响应数据
        :param exp_result: 期望响应结果
        :param response_text: 实际响应结果
        :param asset_type: 断言类型
        :param asset_pattern: 断言规则（举例：响应结果的data[0].issue或data.issue）
        :return: 断言结果（既期望响应结果和实际响应结果是否一致）
        """
        # 默认asset_flag（断言结果）为空
        asset_flag = None
        if asset_type == '相等':  # 如果断言类型为 相等
            if asset_pattern is None or asset_pattern == '':  # 如果 断言模式为空
                # 断言结果输出为相等
                asset_flag = self.assetUtil.equals(response_text, exp_result)
            else:
                # 获取期望响应结果对应的字段值（根据断言规则提取）
                exp_value = self.dataUtil.json_data_analysis(asset_pattern, exp_result)

                # 获取实际响应结果对应的字段值（根据断言规则提取）
                response_value = self.dataUtil.json_data_analysis(asset_pattern, response_text)

                # 断言结果输出为相等
                asset_flag = self.assetUtil.equals(exp_value, response_value)

        elif asset_type == '包含':  # 如果断言类型为 包含
            # asset_flag = self.assetUtil.contains(response_text, asset_pattern)
            # 断言结果输出为包含
            asset_flag = self.assetUtil.contains(response_text, exp_result)

        elif asset_type == '正则':  # 如果断言类型为 正则
            # asset_flag = self.assetUtil.re_matches(response_text, asset_pattern)
            # 断言结果输出为正则
            asset_flag = self.assetUtil.re_matches(response_text, exp_result)
        elif asset_type == '响应头':  # 如果断言类型为 请求头
            asset_flag = self.assetUtil.contains(res.headers["Content-Type"], exp_result)
        return asset_flag, response_text, asset_type, exp_result
