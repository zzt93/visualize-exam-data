### \*1. 个人整体情况图：
import os

from backend.preprocess.pre_process import merge_log_score
from backend.util.config import EID


def get_process_personal():
    # 省略部分实现细节
    # data: List, 包含去重之后的 某人 某天 的全部操作记录
    # 例：data_value = [entry1, entry2, entry3]
    # entry: Map, 一条操作记录
    # op_type: Enum, 操作类型
    # op_happen_time: timestamp, 操作发生的时间
    # op_last_time: int, 操作持续时间
    # 例：entry = {'op_type': op_type_value, 'op_happen_time': op_happen_time_value, 'op_last_time': op_last_time_value}
    # userid: string
    # dayid: int, 天数的id
    # return {'data': data_value, 'userid': userid_value, 'dayid': dayid_value}
    pass


### *2. 编码、调试时间总体情况统计柱状图:
### 3. 编码、调试时间个人情况统计柱状图:
### *4. 学生每题编码、调试的平均时间比例统计、分布:
###  6. 个人每天编码时间统计:


def get_time_total():
    # 忽略部分实现细节
    # userid: string
    # problemid: string
    # code_time: int
    # debug_time: int
    # entry1 = {'userid': userid_value, 'problemid': problemid_value, `dayid`: int,'code_time': code_time_value, 'debug_time': debug_time_value}
    # return [entry1, entry2]
    return


### 5. 整体编码时间分布:


def get_work_time():
    # 忽略部分实现细节
    # data 定义格式见1
    # return data
    pass




## 拷贝：

### 7. 个人外来粘贴字符数统计柱状图:


def get_paste_length_personal():
    # paste_data: List
    # paste_data = [entry1, entry2……]
    # userid: string
    # problemid: string
    # paste_content: string
    # entry = {'userid': userid_value, 'problemid': problemid_value, 'paste_content': paste_content_value}
    # userid: string
    # return {'paste_data': paste_data_value, 'userid': userid_value}
    pass

    ### *8. 粘贴内容分类统计柱状图:


def get_paste_content_classification():
    # paste_data: List
    # paste_data = [entry1, entry2,……]
    # userid: string
    # problemid: string
    # paste_class: string
    # count: int
    # entry = {'userid': userid_value, 'problemid': problemid_value, 'paste_class': paste_class_value, 'count': count_value}
    # userid: string
    # return {'paste_data': paste_data, 'user_id': user_id_value}
    pass
    ## 插入： speed的单位是字符 / 分钟


# ### 9. 平均编码速度分布图:



def get_coding_speed():
    # speed_data: List
    # speed_data = [entry1, entry2, ……]
    # userid: string
    # speed: float
    # entry = {'userid': userid_value, 'speed': speed_value}
    # return speed_data
    pass


## 调试：

### 10. 题目调试次数统计:



def get_debug_personal():
    # data定义见1
    # userid: string
    # problemid: string
    # return {'data': data_value, 'userid': userid_value, 'problemid': problemid_value}
    pass


### \*11. 学生整体调试次数分布统计:



def get_debug_total():
    # debug_count_data: List
    # debug_count_data = [entry1, entry2, ……]
    # userid: string
    # debug_count: int
    # entry = {'userid': userid_value, 'debug_count': debug_count_value}
    # return debug_count_data
    pass


## 得分：

### *12. 学生得分分布柱状图:



def get_score():
    # score_data: List
    # score_data = [entry1, entry2, ……]
    # userid: string
    # score: float
    # entry = {'userid': userid_value, 'score': score_value}
    pass
    # return score_data


### *13. 学生题目得分分布柱状图:



def get__problem_score(eid=EID):
    '''
    # score_data: List
    # score_data = [entry1, entry2, ……]
    # userid: string
    # problemid: string
    # score: float
    # entry = {'userid': userid_value, 'problemid': problemid_value, 'score': score_value}
    :return: score_data
    '''
    tmp = merge_log_score(eid)
    res = []
    for sid, value in tmp.items():
        for pid, s in value.items():
            res.append({'userid': sid, 'problemid': pid, 'score': s})

    return res


## 编译：

### *14. 编译错误出现的次数分布:



def get_build_error_count():
    # build_error_data: List
    # build_error_data = [entry1, entry2, ……]
    # problemid: string
    # error_code: string
    # count: int
    # entry = {'problemid': problemid_value, 'error_code': error_code_value, 'count': count_value}
    # return build_error_data
    pass


### *15. 编译失败的次数分布:



def get__build_failed_count():
    # build_data: List
    # build_data = [entry1, entry2, ……]
    # problemid: string
    # userid: string
    # failed_count: int
    # success_count: int
    # entry = {'problemid': problemid_value, 'userid': userid_value, 'failed_count': failed_count_value, 'success_count': success_count_value}
    # return build_failed_data
    pass


### *16. 每题编码时间过少的人:



def get__time_less():
    # user_list: List
    # user_list = [entry1, entry2, ……]
    # userid: string
    # problemid: string
    # user_time: float
    # mean_time: float
    # entry = {'userid': userid_value, 'problemid': problemid_value, 'user_time': user_time_value, 'mean_time': mean_time_value}
    # return user_list
    pass


def get_all_user_id():

    pass


def get_all_day_id():
    pass


def get_all_problem_id():
    pass


if __name__ == '__main__':
    os.chdir('../../')
    print(get__problem_score())
