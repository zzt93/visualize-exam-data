from backend.util.mysql_connector import MysqlConnector

from backend.util.config import *

# TODO file format: sqllite or defined class format
def to_single_file(file_name, data_source):
    with open(file=file_name, mode='w') as f:
        f.write(data_source)
    return


def student_file_name(user_id, from_date, to_date):
    return user_id + "_" + from_date + "~" + to_date


def remove_dup():
    connector = MysqlConnector()
    for i in range(STUDENT_ID_START, STUDENT_ID_END):
        connector.get_student_file(id, FROM_DATE, TO_DATE)

    # log use time and user_id
    # monitor
    return


def sort_by_time():
    return
