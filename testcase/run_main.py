import os

from common.configparam_util import ConfigEngine
from common.excel_util import Excel
from testcase.run_case import RunCase
from common import ddt_util
import unittest

# 获取全部测试用例
file_name = ConfigEngine.get_config("caseFileSetting", "caseFile")
sheet_name = ConfigEngine.get_config("caseFileSetting", "sheetName")
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(basedir, "data")
file_path = os.path.join(config_path, file_name)
excelUtil = Excel(file_path, sheet_name)
excelUtil.load_excel()
datas = excelUtil.get_case_list()


@ddt_util.ddt
class RunMain(unittest.TestCase):
    """
    测试用例执行
    """

    @ddt_util.data(*datas)
    def test_run_case(self, data):
        """
        执行测试用例
        :param data: 数据内容
        :return: 响应结果断言
        """
        result = RunCase(file_path, sheet_name).run_case_by_data(data)  # 执行单个测试用例
        self.assertTrue(result[0], msg=f"{result[1]} {result[2]} {result[3]} 条件不成立")  # 断言响应结果存在
