import plotly.plotly
import plotly.graph_objs as go
import pandas as pd


def show_build_error_count(build_error_data: list, problemid: str=None, top: int=10):
    """
    统计所有编译错误的次数的分布。可以比较不同编译错误出现的频率。
    横轴为具体编译错误，纵轴为个数
    :param build_error_data: [{'question_id':str, 'error_code':str, 'count':int}]
    :param problemid: 题号
    :param top: 前N个
    :return:
    """
    '''
    build_error_list = []
    build_error_dict = {}

    for temp in build_error_data:
        if temp['error_code'] not in build_error_list:
            build_error_list.append(temp['error_code'])
    for key in build_error_list:
        build_error_dict[key] = 0
    for temp in build_error_data:
        for key in build_error_dict:
            if key == temp['error_code']:
                build_error_dict[key] = build_error_dict[key]+temp['count']
    
    df = pd.DataFrame.from_dict(build_error_dict, orient='index')
    # df = df.reset_index()
    df = df.sort_values(by=[0], ascending=False)
    df = df.head(top)
    print(df)
    '''
    df = pd.DataFrame(build_error_data)
    df = df.set_index('question_id')
    df.index = df.index.map(lambda x: str(x))
    if problemid not in df.index and problemid != None:
        return None
    if problemid:
        df = df.loc[[problemid], :]
    df = df.groupby(['error_code'])['count'].sum()
    df = df.sort_index()
    df = df.sort_values(ascending=False)
    df = df.head(top)

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
        title='所有编译错误次数分布'
    )

    figure = go.Figure(data=data, layout=layout)
    # print(score_distribution)
    # plotly.offline.plot(fig)    # WEB中显示图片
    return figure


def show_build_failed_count(build_data: list):
    """
    统计所有编译失败次数的分布。可以比较编译失败。
    横轴为编译失败次数，纵轴为人数
    :param build_data: [{'problemid':str, 'student_id':str, 'failed_count':int, 'success_count':int}]
    :return:
    """
    df = pd.DataFrame(build_data)
    # df = df.set_index(['student_id'])
    df = df.groupby(['student_id'])['failed_count', 'success_count'].sum()
    df = df.sort_index()
    max_failed_count = df['failed_count'].max()

    trace = go.Histogram(
        x=df['failed_count'],
        histnorm='count',
        name='failed build times',
        xbins=dict(start=0, end=max_failed_count+1, size=10)
    )
    data = [trace]
    layout = go.Layout(
        title='学生整体编译次数失败分布柱状图',
        barmode='Stack',
        bargap=0.2,
        bargroupgap=0.1
    )

    figure = go.Figure(data=data, layout=layout)
    return figure


