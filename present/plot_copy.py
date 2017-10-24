import plotly.graph_objs as go
from plotly import tools
import pandas as pd
from backend.interface.controller import get_all_paste_type


def show_paste_length_personal(paste_data: list, userid: str=None, title: str=None):
    """
    统计个人从外部粘贴的字符数分布。可以查看个人的粘贴字符情况，筛选经常进行大段粘贴的情况。
    横轴为字符数（个），纵轴为次数（个）
    :param paste_data: [{'student_id': str, 'question_id':str, 'paste_content':str}], 注意需要去除非外来的粘贴字符
    :param userid:
    :return:
    """
    df = pd.DataFrame(paste_data)
    df = df.set_index('student_id')
    if userid not in df.index and userid != None:
        return None
    if userid:
        df = df.loc[[userid], :]
    df['paste_len'] = df['paste_content'].map(len)
    max_time = df['paste_len'].max()

    if not title:
        title = userid + ' paste length'

    total_trace = go.Histogram(x=df['paste_len'], histnorm='count', name='code time', xbins=dict(start=0, end=max_time, size=20))
    layout = go.Layout(title=title, xaxis=dict(title='paste length'), yaxis=dict(title='count'), bargap=0.2, bargroupgap=0.1)
    fig = go.Figure(data=[total_trace], layout=layout)
    return fig


def show_paste_content_classification(paste_class: list, userid: str=None, classes: list=[], title:str = None):
    """
    对粘贴内容进行分类，统计不同类粘贴的次数。可以识别学生经常进行的粘贴内容。
    横轴为类别，纵轴为次数（个）
    分为整体情况统计与个人情况统计
    :param paste_class: [{'student_id':str, 'question_id':str, 'paste_class':str, 'count':int}]
    :param userid: 学号，为None代表全部学生
    :return:
    """
    df = pd.DataFrame(paste_class)
    df = df.set_index('student_id')
    if userid not in df.index and userid != None:
        return None
    if userid:
        df = df.loc[[userid], :]
    df = df.groupby(['paste_class'])['count'].sum()
    for cla in classes:
        if cla not in df.index:
            df.loc[cla] = 0

    type_dict = get_all_paste_type()
    df.index = df.index.map(lambda x:type_dict[x])

    if not title:
        if not userid:
            userid = 'all'
        title = userid + ' average time ratio'

    trace = go.Pie(labels=df.index, values=df, name='average time ratio')
    layout = go.Layout(title=title, barmode='stack')
    fig = go.Figure(data=[trace], layout=layout)
    return fig

