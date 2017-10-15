import plotly.plotly
import plotly.graph_objs as go


def show_score(score_data):
    """
    统计学生得分的分布情况
    横轴为得分，纵轴为人数（个）
    :param score_data: [{'userid':str, 'score':float}]
    :return:figure
    """

    score_distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for student in score_data:
        if 0 <= student['score'] <= 10:
            score_distribution[0] = score_distribution[0]+1
        elif 11 <= student['score'] <= 20:
            score_distribution[1] = score_distribution[1]+1
        elif 21 <= student['score'] <= 30:
            score_distribution[2] = score_distribution[2]+1
        elif 31 <= student['score'] <= 40:
            score_distribution[3] = score_distribution[3]+1
        elif 41 <= student['score'] <= 50:
            score_distribution[4] = score_distribution[4]+1
        elif 51 <= student['score'] <= 60:
            score_distribution[5] = score_distribution[5]+1
        elif 61 <= student['score'] <= 70:
            score_distribution[6] = score_distribution[6]+1
        elif 71 <= student['score'] <= 80:
            score_distribution[7] = score_distribution[7]+1
        elif 81 <= student['score'] <= 90:
            score_distribution[8] = score_distribution[8]+1
        elif 91 <= student['score'] <= 100:
            score_distribution[9] = score_distribution[9]+1

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
    :param score_data: [{'userid':str, 'problemid':str, 'score':float}]
    :param problemid: 题号
    :return:figure
    """
    score_distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for student in score_data:
        if problemid == student['problemid']:
            if 0 <= student['score'] <= 10:
                score_distribution[0] = score_distribution[0] + 1
            elif 11 <= student['score'] <= 20:
                score_distribution[1] = score_distribution[1] + 1
            elif 21 <= student['score'] <= 30:
                score_distribution[2] = score_distribution[2] + 1
            elif 31 <= student['score'] <= 40:
                score_distribution[3] = score_distribution[3] + 1
            elif 41 <= student['score'] <= 50:
                score_distribution[4] = score_distribution[4] + 1
            elif 51 <= student['score'] <= 60:
                score_distribution[5] = score_distribution[5] + 1
            elif 61 <= student['score'] <= 70:
                score_distribution[6] = score_distribution[6] + 1
            elif 71 <= student['score'] <= 80:
                score_distribution[7] = score_distribution[7] + 1
            elif 81 <= student['score'] <= 90:
                score_distribution[8] = score_distribution[8] + 1
            elif 91 <= student['score'] <= 100:
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
        title='学生题目得分得分分布柱状图 -- '+problemid
    )

    figure = go.Figure(data=data, layout=layout)
    # print(score_distribution)
    # plotly.offline.plot(fig)  # WEB中显示图片
    return figure
