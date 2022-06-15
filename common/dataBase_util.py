# _*_ coding: utf-8 _*_

from pymysql import Connection

from common.configparam_util import ConfigEngine
from common.log_util import logger

"""
数据库sql处理封装
1、建立连接
2、创建光标
3、创建查询字符串
4、执行查询
5、提交查询
6、关闭游标
7、关闭连接
"""


class MysqlDb(object):

    def __init__(self):
        """
        初始化数据库连接入参
        """
        configEngine = ConfigEngine()
        self.host = configEngine.get_config('dataBase', 'host')
        self.port = configEngine.get_config('dataBase', 'port')
        self.user = configEngine.get_config('dataBase', 'user')
        self.password = configEngine.get_config('dataBase', 'password')
        self.database = configEngine.get_config('dataBase', 'database')
        self.charset = configEngine.get_config('dataBase', 'charset')

        self.conn = Connection(host=self.host,
                               port=int(self.port),
                               user=self.user,
                               password=self.password,
                               database=self.database,
                               charset=self.charset)

        # 创建游标操作数据库
        self.cursor = self.conn.cursor()

        # 初始化日志方法

    def query_one(self, sql, params=None):
        """
        查询第一条结果
        :param sql: SQL语句
        :param params: 查询使用的参数。(可选)
        :return:  查询的第一条结果
        """
        try:
            # 执行SQL语句
            self.cursor.execute(sql, params)
            logger.info("执行SQL语句为:{0}".format(sql))
        except Exception as e:
            logger.info("执行SQL语句异常:{0}".format(e))
            logger.info("异常sql语句为:{0}".format(sql))
        else:
            # 获取查询到的第一条数据
            result = self.cursor.fetchone()
            logger.info(f'sql执行结果为{result}')

            # 调用数据库关闭方法函数
            self.close()

            return result

    def query_all(self, sql, params=None):
        """
        查询所有结果
        :param sql: SQL语句
        :param params: 查询使用的参数。(可选)
        :return: 查询所有结果
        """
        try:
            # 执行SQL语句
            self.cursor.execute(sql, params)
        except Exception as e:
            logger.info("执行SQL语句异常:{0}".format(e))

        else:
            # 获取查询到的第一条数据
            result = self.cursor.fetchall()

            # 调用数据库关闭方法函数
            self.close()

            return result

    def update(self, sql, params=None):
        """
        修改数据
        :param sql: SQL语句
        :param params: 查询使用的参数。(可选)
        :return:
        """
        try:
            # 执行SQL语句
            self.cursor.execute(sql, params)

            # 提交到数据库执行
            self.conn.commit()

            # 打印数据库更新成功
            logger.info("更新成功！")

            # 调用数据库关闭方法函数
            self.close()

        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()

            # 打印数据库更新失败
            logger.info("更新失败,异常{0}".format(e))

    def delete(self, sql, params=None):
        """
        删除数据
        :param sql: SQL语句
        :param params: 查询使用的参数。(可选)
        :return:
        """
        try:
            # 执行SQL语句
            self.cursor.execute(sql, params)

            # 提交到数据库执行
            self.conn.commit()

            # 打印数据库删除成功
            logger.info("删除成功！")

            # 调用数据库关闭方法函数
            self.close()

        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()

            # 打印数据库删除失败
            logger.info("删除失败,异常{0}".format(e))

    def insert(self, sql, params=None):
        """
        新增数据
        :param sql: SQL语句
        :param params: 查询使用的参数。(可选)
        :return:
        """
        try:
            # 执行SQL语句
            self.cursor.execute(sql, params)

            # 提交到数据库执行
            self.conn.commit()

            # 打印数据库新增成功
            logger.info("新增成功！")

            # 调用数据库关闭方法函数
            self.close()

        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()

            # 打印数据库新增失败
            logger.info("新增失败,异常{0}".format(e))

    def close(self):
        """
        数据库关闭
        :return:
        """
        # 关闭游标
        self.cursor.close()

        # 关闭数据库连接
        self.conn.close()


# if __name__ == '__main__':
#     print(MysqlDb().query_one(sql="SELECT * FROM device_account_relation"))
