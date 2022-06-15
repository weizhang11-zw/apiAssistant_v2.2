import os
import unittest
from common.time_util import GetTime
from testcase import run_main
from common.HTMLTestRunnerNew_util import HTMLTestRunner

"""执行测试套件"""
# 创建测试套件
suite = unittest.TestSuite()

# 创建一个loader对象，用来加载测试用例
loader = unittest.TestLoader()

# 通过模块加载(.py文件) 头
suite.addTest(loader.loadTestsFromModule(run_main))

# 执行测试套件（集合），并生成HTML测试报告
file_name = 'report_{}.html'.format(GetTime().get_nowtime())
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(basedir, "reports")
report_name = os.path.join(log_dir, file_name)
# report_name = '../reports/' + file_name

# 通过open()方法以二进制写模式('wb')打开当前目录下的report.html，如果没有，则自动创建
fp = open(report_name, 'wb')
runner = HTMLTestRunner(
    stream=fp,  # 指定测试报告文件
    title='接口自动化测试报告',  # 定义测试报告的标题
    description='接口自动化测试报告详细信息',  # 定义测试报告的副标题
    verbosity=2,
)

# 执行测试套件
runner.run(suite)
fp.close()
