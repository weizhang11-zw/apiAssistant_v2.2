import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.time_util import GetTime


class Email(object):
    """
    发送邮件
    """

    def __init__(self, email_info):
        """
        初始化获取邮件基本信息
        :param email_info: 邮件发送的信息内容
        """
        # self.now_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.now_date = GetTime().get_nowtime()  # 初始化获取当前时间

        self.email_info = email_info  # 初始化邮件内容信息

        # 使用SMTP_SSL连接服务，端口默认为465
        self.Email_SMTP = smtplib.SMTP_SSL(self.email_info['server'], self.email_info['port'])

        # 创建变量
        self.user_from = ''

    def login_Email(self):
        """
        通过邮箱名和smtp授权码登录到邮箱
        :return: 邮箱加载
        """
        self.user_from = self.email_info['user']
        login_email = self.Email_SMTP.login(self.email_info['user'], self.email_info['password'])
        return login_email

    def send_Email(self):
        """
        发送邮件，可以实现群发
        :return:
        """

        # 创建MIMEMultipart()对象
        msg = MIMEMultipart()

        # 定义邮件附件内容
        filePath = self.get_report()  # 获取测试报告文件
        report_file = open(filePath, 'rb').read()  # 打开测试报告文件
        att = MIMEText(report_file, 'base64', 'utf-8')  # 构造附件
        att["Content-Type"] = 'application/octet-stream'  # 这里的filename可以任意写，写什么名字，邮件中附件显示什么名字
        att["Content-Disposition"] = 'attachment; filename="API_report.html"'

        msg.attach(att)  # 获取邮件附件内容

        # 定义文件标题栏
        msg['From'] = self.email_info['user']  # 邮件发送者
        msg['To'] = self.email_info['to']  # 邮件接收者
        msg['Subject'] = self.email_info['subject']  # 邮件标题名称 html 设置文本格式，第三个 utf-8 设置编码

        # 定义邮件正文内容
        # contents = MIMEText(self.email_info['content'], 'html', 'utf-8')  # 三个参数：第一个为文本内容，第二个
        contents = MIMEText(report_file, 'html', 'utf-8')  # 三个参数：第一个为文本内容，第二个

        msg.attach(contents)  # 获取邮件正文内容

        try:
            self.login_Email()  # 邮箱加载
            self.Email_SMTP.sendmail(self.user_from, self.email_info['to'].split(','), msg.as_string())
            print('邮件发送成功，请注意查收！'.center(30, '#'))
        except Exception as e:
            print('邮件发送失败：', e)

    @staticmethod
    def get_report(reports_path=r"../reports/"):
        """
        查找测试报告目录，找到最新生成的测试报告文件
        :param self:
        :param reports_path: 测试报告所在目录
        :return: 返回最新的测试报告文件
        """
        lists = os.listdir(reports_path)  # 列出目录的下所有文件和文件夹保存到lists
        lists.sort(key=lambda fn: os.path.getmtime(reports_path + "/" + fn))  # 按时间排序
        file_new = os.path.join(reports_path, lists[-1])  # 获取最新的文件保存到file_new
        return file_new

    def close(self):
        """
        退出smtp服务
        :return:
        """
        self.Email_SMTP.quit()
        print('logout'.center(30, '#'))
