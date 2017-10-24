import plotly.plotly
import plotly.graph_objs as go
import pandas as pd


def show_score(score_data):
    """
    统计学生得分的分布情况
    横轴为得分，纵轴为人数（个）
    :param score_data:  [{'student_id':str, 'score':float}]
    :return:figure
    """

    for data in score_data:
        data['new_score'] = data['score'] * 100

    userids = []
    new_score_data = []
    for data in score_data:
        if data['student_id'] not in userids:
            userids.append(data['student_id'])
            new_score_data.append(data)
        else:
            for new_data in new_score_data:
                if data['student_id'] == new_data['student_id']:
                    if data['new_score'] > new_data['new_score']:
                        new_data['new_score'] = data['new_score']
    score_data = new_score_data

    score_distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for student in score_data:
        if 0 <= student['new_score'] <= 10:
            score_distribution[0] = score_distribution[0] + 1
        elif 11 <= student['new_score'] <= 20:
            score_distribution[1] = score_distribution[1] + 1
        elif 21 <= student['new_score'] <= 30:
            score_distribution[2] = score_distribution[2] + 1
        elif 31 <= student['new_score'] <= 40:
            score_distribution[3] = score_distribution[3] + 1
        elif 41 <= student['new_score'] <= 50:
            score_distribution[4] = score_distribution[4] + 1
        elif 51 <= student['new_score'] <= 60:
            score_distribution[5] = score_distribution[5] + 1
        elif 61 <= student['new_score'] <= 70:
            score_distribution[6] = score_distribution[6] + 1
        elif 71 <= student['new_score'] <= 80:
            score_distribution[7] = score_distribution[7] + 1
        elif 81 <= student['new_score'] <= 90:
            score_distribution[8] = score_distribution[8] + 1
        elif 91 <= student['new_score'] <= 100:
            score_distribution[9] = score_distribution[9] + 1

    trace = go.Bar(
        x=['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80',
           '81-90', '91-100'],
        y=score_distribution,
        # text=score_distribution,
        textposition='auto',
        marker=dict(
            color='rgb(0,162,232)',
        )
    )
    data = [trace]
    layout = go.Layout(
        title='学生得分分布柱状图'
    )

    figure = go.Figure(data=data, layout=layout)
    # print(score_distribution)
    # plotly.offline.plot(fig)    # WEB中显示图片
    return figure


def show_problem_score(score_data: list, problemid: str):
    """
    统计每题得分的分布情况
    横轴为得分，纵轴为人数（个）
    :param score_data: [{'student_id':str, 'question_id':str, 'score':float}]
    :param problemid: 题号
    :return:figure
    """

    for data in score_data:
        data['new_score'] = data['score'] * 100

    new_score_data = []
    for data in score_data:
        for new_data in new_score_data:
            if new_data['student_id'] == data['student_id'] and new_data['question_id'] == data['question_id']:
                if data['new_score'] > new_data['new_score']:
                    new_data['new_score'] = data['new_score']
                continue
        new_score_data.append(data)
    score_data = new_score_data

    score_distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for student in score_data:
        if problemid == str(student['question_id']):
            if 0 <= student['new_score'] <= 10:
                score_distribution[0] = score_distribution[0] + 1
            elif 11 <= student['new_score'] <= 20:
                score_distribution[1] = score_distribution[1] + 1
            elif 21 <= student['new_score'] <= 30:
                score_distribution[2] = score_distribution[2] + 1
            elif 31 <= student['new_score'] <= 40:
                score_distribution[3] = score_distribution[3] + 1
            elif 41 <= student['new_score'] <= 50:
                score_distribution[4] = score_distribution[4] + 1
            elif 51 <= student['new_score'] <= 60:
                score_distribution[5] = score_distribution[5] + 1
            elif 61 <= student['new_score'] <= 70:
                score_distribution[6] = score_distribution[6] + 1
            elif 71 <= student['new_score'] <= 80:
                score_distribution[7] = score_distribution[7] + 1
            elif 81 <= student['new_score'] <= 90:
                score_distribution[8] = score_distribution[8] + 1
            elif 91 <= student['new_score'] <= 100:
                score_distribution[9] = score_distribution[9] + 1

    trace = go.Bar(
        x=['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80',
           '81-90', '91-100'],
        y=score_distribution,
        text=score_distribution,
        textposition='auto',
        marker=dict(
            color='rgb(0,162,232)',
        )
    )
    data = [trace]
    layout = go.Layout(
        title='学生题目得分得分分布柱状图 -- ' + str(problemid)
    )

    figure = go.Figure(data=data, layout=layout)
    # print(score_distribution)
    # plotly.offline.plot(fig)  # WEB中显示图片
    return figure


def show_testcase_error(testcase_data: list, problemid: str):
    """
    统计每道题每个测试用例错误的人数
    :param testcase_data:[{'question_id':string , 'testcase_id':string , 'error_count':int}]
    :param problemid:string
    :return:figure
    """
    for data in testcase_data:
        if data['testcase_id'] == '':
            data['testcase_id'] = 'AC'
    df = pd.DataFrame(testcase_data)
    df = df.set_index('question_id')
    df.index = df.index.map(lambda x: str(x))
    if problemid not in df.index:
        return None

    df = df.loc[[problemid], :]

    # df = df.reset_index()
    df = df.groupby(['testcase_id'])['error_count'].sum()
    df = df.sort_index()
    df = df.sort_values(ascending=False)

    trace = go.Pie(
        labels=df.index,
        values=df,
    )

    data = [trace]
    layout = go.Layout(
        title='题目测试用例错误情况柱状图 -- ' + problemid
    )

    figure = go.Figure(data=data, layout=layout)
    # print(score_distribution)
    # plotly.offline.plot(fig)    # WEB中显示图片
    return figure


def show_problem_avgscore(score_data: list):
    """
    统计每题的平均分
    :param score_data:[{'userid':str, 'problemid':str, 'score':float}]
    :return:figure
    """

    for data in score_data:
        data['new_score'] = data['score'] * 100
    new_score_data = []
    for data in score_data:
        for new_data in new_score_data:
            if new_data['student_id'] == data['student_id'] and new_data['question_id'] == data['question_id']:
                if data['new_score'] > new_data['new_score']:
                    new_data['new_score'] = data['new_score']
                continue
        new_score_data.append(data)
    score_data = new_score_data

    df = pd.DataFrame(score_data)
    # df = df.set_index('student_id')
    df = df.groupby(['question_id'])['new_score'].mean()
    df = df.sort_index()
    df.index = df.index.map(lambda x: 'Q' + str(x))
    df = df.sort_values(ascending=False)
    df = df.round(1)

    trace = go.Bar(
        x=df.index,
        y=df,
        text=df,
        textposition='auto',
        marker=dict(
            color='rgb(0,162,232)',
        )
    )

    data = [trace]
    layout = go.Layout(
        title='每题平均分分布柱状图'
    )

    figure = go.Figure(data=data, layout=layout)
    # print(score_distribution)
    # plotly.offline.plot(fig)    # WEB中显示图片
    return figure
