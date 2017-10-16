import plotly.graph_objs as go
from plotly import tools


def show_paste_length_personal(paste_data: list, userid: str, title: str=None):
    """
    统计个人从外部粘贴的字符数分布。可以查看个人的粘贴字符情况，筛选经常进行大段粘贴的情况。
    横轴为字符数（个），纵轴为次数（个）
    :param paste_data: [{'userid': str, 'problemid':str, 'paste_content':str}], 注意需要去除非外来的粘贴字符
    :param userid:
    :return:
    """
    x = []
    max_time = 0
    for paste in paste_data:
        if userid != paste['userid']:
            continue
        t = len(paste['paste_content'])
        x.append(t)
        if t > max_time:
            max_time = t

    if not title:
        title = userid + ' paste length'

    total_trace = go.Histogram(x=x, histnorm='count', name='code time', xbins=dict(start=0, end=max_time, size=20))
    layout = go.Layout(title=title, xaxis=dict(title='paste length'), yaxis=dict(title='count'), bargap=0.2, bargroupgap=0.1)
    fig = go.Figure(data=[total_trace], layout=layout)
    return fig


def show_paste_content_classification(paste_class: list, userid: str=None, classes:list=[], title:str = None):
    """
    对粘贴内容进行分类，统计不同类粘贴的次数。可以识别学生经常进行的粘贴内容。
    横轴为类别，纵轴为次数（个）
    分为整体情况统计与个人情况统计
    :param paste_class: [{'userid':str, 'problemid':str, 'paste_class':str, 'count':int}]
    :param userid: 学号，为None代表全部学生
    :return:
    """
    data = {}
    for paste in paste_class:
        if paste['userid'] != userid and userid:
            continue
        if paste['paste_class'] not in data.keys():
            data[paste['paste_class']] = paste['count']
        else:
            data[paste['paste_class']] += paste['count']

    for cla in classes:
        if cla not in data.keys():
            data[cla] = 0

    data = sorted(data.items(), key=lambda d: d[0])

    x = []
    y = []
    for da in data:
        x.append(da[0])
        y.append(da[1])

    if not title:
        if not userid:
            userid = 'all'
        title = userid + ' average time ratio'

    trace = go.Bar(x=x, y=y, name='average time ratio')
    layout = go.Layout(title=title, barmode='stack')
    fig = go.Figure(data=[trace], layout=layout)
    return fig

