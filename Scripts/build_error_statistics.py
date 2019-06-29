import MySQLdb
import numpy as np


BUILD_ERROR = 'builderror'


def connect(db_name, host='localhost', user='root', passwd='root', port=3306):
    con = MySQLdb.connect(host=host, user=user, passwd=passwd, database=db_name, port=port)
    return con


def disconnect(con):
    con.close()


def cal_build_error(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM {}'.format(BUILD_ERROR))
    res = cur.fetchall()
    return res


def sum_dicts(*dict_args):
    keys = set()
    for dictionary in dict_args:
        keys |= set(dictionary.keys())
    res = {k: np.sum(list(map(lambda di: di.get(k, 0), dict_args))) for k in keys}
    return res


def add_dict(one_dict: dict, key, value):
    if one_dict == None:
        return
    if key in one_dict.keys():
        one_dict[key] += value
    else:
        one_dict[key] = value


def deal_with_data(res, dicts):
    for id, error_code, num in res:
        if error_code[0] == 'C':
            for di in dicts:
                add_dict(di, error_code, num)
    return dicts


def statistics_data_dict(db_names:list, db_dicts:list):
    for db_name in db_names:
        con = connect(db_name)
        res = cal_build_error(con)
        disconnect(con)
        deal_with_data(res, db_dicts)
    return db_dicts


def sort_dict_value(one_dict:dict, key_fn=lambda x: x[1], reverse=True):
    sort_list = sorted(one_dict.items(), key=key_fn, reverse=True)
    return sort_list


def cal_percentage(sorted_value):
    total_list = [i[1] for i in sorted_value]
    total = np.sum(total_list)
    sorted_value = [list(i) + [i[1]/total] for i in sorted_value]
    return sorted_value


def get_top_percent(percented_value, max_percent=0.9):
    i = 0
    while np.sum(percented_value[0:i]) <= max_percent and i < len(percented_value):
        i += 1
    return i


if __name__ == '__main__':
    structured_db = ['visualize_exam_first_exam', 'visualize_exam_second_exam']
    object_oriented_db = ['visualize_exam_third_exam']
    structured_dict = {}
    object_oriented_dict = {}

    statistics_data_dict(structured_db, [structured_dict])
    statistics_data_dict(object_oriented_db, [object_oriented_dict])

    all_dict = sum_dicts(structured_dict, object_oriented_dict)

    structured_sorted_list = sort_dict_value(structured_dict)
    object_oriented_sorted_list = sort_dict_value(object_oriented_dict)
    all_sorted_list = sort_dict_value(all_dict)

    structured_sorted_list = cal_percentage(structured_sorted_list)
    object_oriented_sorted_list = cal_percentage(object_oriented_sorted_list)
    all_sorted_list = cal_percentage(all_sorted_list)

    # print(len(all_sorted_list))
    # print(all_sorted_list)
    n = get_top_percent(list(zip(*all_sorted_list))[-1], 0.9)
    n = 20
    for res in all_sorted_list[:n+1]:
        # pass
        print(res)
    res_sum = np.sum(list(zip(*all_sorted_list[:n]))[-1])
    print(n, res_sum)


