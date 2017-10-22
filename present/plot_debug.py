import plotly.plotly
import plotly.graph_objs as go
import pandas as pd


def show_debug_personal(debug_data: list, userid: str=None, problemid: str=None) :
    """
    统计每个人在不同题目的调试次数。可以发现不同题目的调试次数，评估不同题目的难度。
    横轴为题目，纵轴为调试次数（个）
    :param debug_data:[{'student_id':string,'problem_id':string,'debug_count':int}]
    :param userid: 学号
    :param problemid: 题号
    :return:figure
    """
    df = pd.DataFrame(debug_data)
    df = df.set_index('student_id')
    if userid not in df.index and userid != None:
        return None

    if userid:
        df = df.loc[[userid], :]
    df = df.groupby(['problem_id'])['debug_count'].sum()
    df.index = df.index.map(lambda x: 'Q'+str(x))
    df = df.sort_index()


    trace = go.Bar(
        x=df.index,
        y=df,
        text=df,
        textposition='auto'
    )

    data = [trace]
    layout = go.Layout(
        title='不同题目调试次数柱状图'
    )

    figure = go.Figure(data=data,layout=layout)
    return figure


def show_debug_total(debug_count_data):
    """
    统计学生整体上调试次数的分布，可以发现学生整体是否善用了调试工具。
    横轴为调试次数段（个），纵轴为学生人数（个）
    :param debug_count_data: [{'student_id':str, 'debug_count':int}]
    :return:figure
    """
    debug_count_personal = []
    debug_distribution = []
    x_axis = []
    for student in debug_count_data:
        debug_count_personal.append(student['debug_count'])

    for i in range(max(debug_count_personal)+1):
        debug_distribution.append(0)
        x_axis.append(i)

    for i in x_axis:
        for student in debug_count_data:
            if student['debug_count'] == i:
                debug_distribution[i] = debug_distribution[i]+1
    # print (x_axis)
    trace = go.Bar(
        x=x_axis,
        y=debug_distribution,
        text=debug_distribution,
        textposition='auto',
        marker=dict(
            color='rgb(0,162,232)',
        )
    )
    data = [trace]
    layout = go.Layout(
        title='学生整体调试次数分布柱状图',
        barmode='Stack'
    )

    figure = go.Figure(data=data, layout=layout)
    return figure
