import os

from backend.util.constant import INVALID
from backend.util.mysql_connector import MysqlConnector
from backend.util.path_util import path_leaf


def get_question_set(eid):
    mysql = MysqlConnector()
    question_id_set = mysql.get_question_set(eid)
    mysql.close()
    return question_id_set


def extract_question_id(project_name):
    try:
        tmp = int(project_name[1:])
    except ValueError:
        print('project name is invalid: ' + project_name)
        return INVALID
    from backend.interface.controller import get_all_problem_id
    ids = get_all_problem_id()
    if tmp not in ids:
        print('project name is invalid: ' + project_name)
        return INVALID
    return tmp


def extract_question_id_from_path(filename):
    temp = path_leaf(filename)
    (short_name, extension) = os.path.splitext(temp)
    question_id = extract_question_id(short_name)
    return question_id
