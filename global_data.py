import os

from common.time_util import GetTime
from common.dataBase_util import MysqlDb


class Data(object):
    """
    参数化全局变量存储空间
    """
    t = GetTime()
    tomorrow_time = t.get_tomorrow()
    today_time = t.get_today()
    yesterday_time = t.get_yesterday()
    # xiaokang_token = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJwaG9uZSI6IjE3NjIxNTI1Mzg3IiwiZXhwVGltZSI6MzE1MzYwMDAwMDAsImFjY291bnRObyI6IkdNMjAyMjA1MjAwOTU2MjYwMDAwMDAwMzA1IiwicGxhdFR5cGUiOiI0IiwidXNlck5hbWUiOiJnbV81Mzg3IiwiZXhwIjoxNjg0NTYzOTc3LCJ1c2VySWQiOiIxMzMwMSJ9.AAKPonKC7Y4ZfZ3x6qitTKVqsQCjb921IqfXMI_FgDO9K62I7Vjz_3cHPOJ00_R_8c5YWu_l-ZKtcuSESX1SBg"
    user_name = "17621525387"
    password = "541925"
    # consultId = str(MysqlDb().query_one(
    #     f"SELECT id FROM `wjj-gm-health-consult`.`gm_health_consult_info`  where appoint_start_time > '{today_time} 00:00:00' limit 1")[
    #     0])
