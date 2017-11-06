import pandas as pd

def show_time_less(user_list: list):
    """
    每题编码时间过少的人。以平均时间*20%为阈值，当时间比此时间还少时，认为该学生没有认真完成题目
    :param user_list: [{'userid':str, 'problemid':str, 'user_time':float, 'mean_time':float}]
    :return:list
    """

    time_less_student = []
    for student in user_list:
        if student['used_time'] < student['mean_time']*0.2:
            time_less_student.append(student)

    return time_less_student


def show_time_less_logic(user_data: list):
    df = pd.DataFrame(user_data)
    # df = df.set_index(['question_id'])
    df = df.groupby(['student_id', 'question_id'])['code_time', 'debug_time'].sum()
    df['work_time'] = df['code_time'] + df['debug_time']
    df['work_time'] = df['work_time']/60
    df = df.reset_index(level=['question_id', 'student_id'])
    df_tmp = df.groupby('question_id')['work_time'].mean().to_frame()
    df_tmp = df_tmp.reset_index(['question_id'])
    df_tmp = df_tmp.rename(columns={'work_time': 'mean_time'})

    df = pd.merge(df, df_tmp)

    df = df[df['work_time']<(df['mean_time']*0.2)]
    df_count = df.groupby('student_id')['question_id'].count()
    df_count = df_count.sort_values(ascending=False)
    df_count = df_count.reset_index(['student_id'])
    return df.to_dict(orient='records'), df_count.to_dict(orient='records')
