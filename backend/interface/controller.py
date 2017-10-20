import os
from backend.database.model import *
from backend.preprocess.pre_process import merge_log_score
from backend.util.config import EID
from backend.util.mysql_connector import MysqlConnector
from backend.util.constant import OperatorType


### *1. 个人整体情况图：
def get_process_personal():
    result = []
    for stu in Student.select():
        day_op = {}
        for op in Operation.select().where(Operation.student_id == stu.student_id):
            day = op.op_happen_time.date()
            entry = {'op_type': op.op_type, 'op_happen_time': op.op_happen_time, 'op_last_time': op.op_last_time}
            if day in day_op:
                day_op[day].append(entry)
            else:
                day_op[day] = [entry]
            for key in day_op:
                record = {'data': day_op[key], 'student_id': stu.student_id, 'dayid': key}
                result.append(record)
    return result


### *2. 编码、调试时间总体情况统计柱状图:
def get_time_total():
    total = []
    for cdt in CodeAndDebugTime.select():
        entry = {'student_id': cdt.student_id.student_id, 'question_id': cdt.question_id,
                 'dayid': cdt.date, 'code_time': cdt.code_time, 'debug_time': cdt.debug_time}
        total.append(entry)
    return total


### 3. 编码、调试时间个人情况统计柱状图:
def get_time_personal():
    total = []
    for stu in Student.select():
        user_data = []
        for cdt in CodeAndDebugTime.select().where(stu.student_id == CodeAndDebugTime.student_id):
            entry = {'student_id': cdt.student_id.student_id, 'question_id': cdt.question_id,
                     'dayid': cdt.date, 'code_time': cdt.code_time, 'debug_time': cdt.debug_time}
            user_data.append(entry)
        total.append({'user_data': user_data, 'student_id': stu.student_id})
    return total


### *4. 学生每题编码、调试的平均时间比例统计、分布:
def get_time_div_total():
    data = []
    for qid in QuestionInExam.select():
        cnt = 0
        total_debug_time = 0
        total_code_time = 0
        for cdt in CodeAndDebugTime.select().where(CodeAndDebugTime.question_id == qid):
            cnt += 1
            total_code_time += cdt.code_time
            total_debug_time += cdt.debug_time
        if cnt == 0:
            cnt = 1
        data.append(
            {'question_id': qid.question_id, 'debug_time': total_debug_time / cnt, 'code_time': total_code_time / cnt})
    return data


###  6. 个人每天编码时间统计:
def get_work_time_personal():
    result = []
    for stu in Student.select():
        day_op = {}
        for op in Operation.select().where(Operation.student_id == stu.student_id):
            day = op.op_happen_time.date()
            entry = {'op_type': op.op_type, 'op_happen_time': op.op_happen_time, 'op_last_time': op.op_last_time}
            if day in day_op:
                day_op[day].append(entry)
            else:
                day_op[day] = [entry]
            for key in day_op:
                record = {'data': day_op[key], 'student_id': stu.student_id, 'dayid': key}
                result.append(record)
    return result

### 5. 整体编码时间分布:
def get_work_time():
    result = []
    for stu in Student.select():
        day_op = {}
        for op in Operation.select().where(Operation.student_id == stu.student_id):
            day = op.op_happen_time.date()
            entry = {'op_type': op.op_type, 'op_happen_time': op.op_happen_time, 'op_last_time': op.op_last_time}
            if day in day_op:
                day_op[day].append(entry)
            else:
                day_op[day] = [entry]
            for key in day_op:
                record = {'data': day_op[key], 'student_id': stu.student_id, 'dayid': key}
                result.append(record)
    return result


## 拷贝：

### 7. 个人外来粘贴字符数统计柱状图:

def get_paste_length_personal():
    pasta_data = []
    for p in Paste.select():
        entry = {'student_id': p.student_id.student_id, 'question_id': p.question_id,
                 'paste_content': p.paste_content, 'happen_time': p.happen_time}
        pasta_data.append({'pasta_data': entry, 'student_id': p.student_id.student_id})
    return pasta_data

    ### *8. 粘贴内容分类统计柱状图:


def get_paste_content_classification():
    # paste_data: List
    # paste_data = [entry1, entry2,……]
    # student_id: string
    # question_id: string
    # paste_class: string
    # count: int
    # entry = {'student_id': student_id_value, 'question_id': question_id_value, 'paste_class': paste_class_value, 'count': count_value}
    # student_id: string
    # return [{'paste_data': paste_data, 'student_id': student_id_value}]
    pasta_data = []
    source = Paste.raw(
        'select student_id_id, question_id, paste_type, count(*) as cnt from paste GROUP BY student_id_id, question_id, paste_type')
    for i in source:
        paste_data = {'student_id': i.student_id.student_id, 'question_id': i.question_id,
                      'paste_class': i.paste_type, 'count': i.cnt}
        pasta_data.append({'paste_data': paste_data, 'student_id': i.student_id.student_id})
    return pasta_data

## 插入： speed的单位是字符 / 分钟


# ### 9. 平均编码速度分布图:

def get_coding_speed():
    # speed_data: List
    # speed_data = [entry1, entry2, ……]
    # student_id: string
    # speed: float
    # entry = {'student_id': student_id_value, 'speed': speed_value}
    # return speed_data
    speed_data = []
    for sp in Speed.select():
        entry = {'student_id': sp.student_id.student_id, 'speed': sp.speed}
        speed_data.append(entry)
    return speed_data


## 调试：

### 10. 题目调试次数统计:


# TODO 这里少一个属性，Debug里没有question_id
def get_debug_personal():
    # data定义见1
    # student_id: string
    # question_id: string
    # return {'data': data_value, 'student_id': student_id_value, 'question_id': question_id_value}
    result = []
    return result


## *11. 学生整体调试次数分布统计:


def get_debug_total():
    # debug_count_data: List
    # debug_count_data = [entry1, entry2, ……]
    # student_id: string
    # debug_count: int
    # entry = {'student_id': student_id_value, 'debug_count': debug_count_value}
    # return debug_count_data
    debug_count_data = []
    for de in Debug.select():
        entry = {'student_id': de.student_id.student_id, 'debug_count': de.debug_count}
        debug_count_data.append(entry)
    return debug_count_data


## 得分：

### *12. 学生得分分布柱状图:
def get_score():
    # score_data: List
    # score_data = [entry1, entry2, ……]
    # student_id: string
    # score: float
    # entry = {'student_id': student_id_value, 'score': score_value}
    score_data = []
    for stu in Student.select():
        total_score = 0
        for sqr in StudentQuestionResult.select().where(stu.student_id == StudentQuestionResult.student_id):
            total_score += sqr.score
        entry = {'student_id': stu.student_id, 'score': total_score}
        score_data.append(entry)
    return score_data


### *13. 学生题目得分分布柱状图:

def get_problem_score():
    """
    # score_data: List
    # score_data = [entry1, entry2, ……]
    # student_id: string
    # question_id: string
    # score: float
    # entry = {'student_id': student_id_value, 'question_id': question_id_value, 'score': score_value}
    :return: score_data
    """
    score_data = []
    for sqr in StudentQuestionResult.select():
        entry = {'student_id': sqr.student_id.student_id, 'question_id': sqr.question_id, 'score': sqr.score}
        score_data.append(entry)
    return score_data


## 编译：

### *14. 编译错误出现的次数分布:


def get_build_error_count():
    # build_error_data: List
    # build_error_data = [entry1, entry2, ……]
    # question_id: string
    # error_code: string
    # count: int
    # entry = {'question_id': question_id_value, 'error_code': error_code_value, 'count': count_value}
    # return build_error_data
    build_error_data = []
    for be in BuildError.select():
        entry = {'question_id': be.question_id.question_id, 'error_code': be.error_code, 'count': be.count}
        build_error_data.append(entry)
    return build_error_data


### *15. 编译失败的次数分布:
def get_build_failed_count():
    # build_data: List
    # build_data = [entry1, entry2, ……]
    # question_id: string
    # student_id: string
    # failed_count: int
    # success_count: int
    # entry = {'question_id': question_id_value, 'student_id': student_id_value, 'failed_count': failed_count_value, 'success_count': success_count_value}
    # return build_failed_data
    build_data = []
    for br in BuildResult.select():
        entry = {'question_id': br.question_id, 'student_id': br.student_id.student_id, 'failed_count': br.failed_count,
                 'success_count': br.success_count}
        build_data.append(entry)
    return build_data


### *16. 每题编码时间过少的人:
def get_time_less():
    user_list = []
    for ques in QuestionInExam.select():
        cnt = 0
        total_time = 0
        for stu in StudentQuestionResult.select().where(StudentQuestionResult.question_id == ques.question_id):
            total_time += stu.used_time
            cnt += 1
        if cnt == 0:
            cnt = 1
        mean_time = total_time / cnt
        print(mean_time, ques.question_id)
        for stu in StudentQuestionResult.select().where(StudentQuestionResult.question_id == ques.question_id):
            if stu.used_time < 0.2 * mean_time:
                entry = {'student_id': stu.student_id.student_id, 'question_id': ques.question_id,
                         'used_time': stu.used_time,
                         'mean_time': mean_time}
                user_list.append(entry)
    return user_list


def get_all_user_id():
    pass


def get_all_day_id():
    pass


def get_all_problem_id():
    pass


if __name__ == '__main__':
    os.chdir('../../')
    # print(get__problem_score())
    print(get_work_time())
    # print(datetime.datetime.now().date())
