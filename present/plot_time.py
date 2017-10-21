from backend.util.constant import OperatorType
from .plot_util import deal_result

import datetime
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
import plotly.offline as py
from collections import defaultdict

def show_process_personal(data: list, userid: str, dayid: int):
    """
    统计每人每天的插入、删除字符，编译调试情况。可以得到单个学生某天编码的整体情况。
    横轴是时间00:00-23:59，纵轴是插入字符数（个数），删除字符数（个数），编译点，调试点
    :param data: 包含去重之后的 某人 某天 的全部操作记录
    :param userid: 学号
    :param dayid: 天数id
    :return: fig对象
    """
    leg = ['text', 'build', 'debug']
    period = 1
    first = data[0]
    last = data[len(data) - 1]
    rng = pd.date_range(first['time'] - datetime.timedelta(seconds=period - 1), last['time'], freq='s')
    dict_from = {}
    dict_to = {}
    dict_build_success = {}
    dict_build_failed = {}
    dict_debug_run = {}
    dict_debug_end = {}
    for item in data:
        if item[OperatorType.NAME] == OperatorType.CONTENT_INSERT \
                or item[OperatorType.NAME] == OperatorType.CONTENT_DELETE:
            for i in range(period):
                delta = datetime.timedelta(seconds=i)
                time = item['time'] - delta
                # print(time)
                if time not in dict_from:
                    dict_from[time] = 0
                dict_from[time] += ((len(item['textfrom'])) / period)
                if time not in dict_to:
                    dict_to[time] = 0
                dict_to[time] += ((len(item['textto'])) / period)
            if item['time'] not in dict_from:
                dict_from[item['time']] = 0
            # dict_from[item['time']] += len(item['textfrom'])
            if item['time'] not in dict_to:
                dict_to[item['time']] = 0
                # dict_to[item['time']] += len(item['textto'])
        if item[OperatorType.NAME] == '9':
            if deal_result(item['buildlogcontent']):
                dict_build_success[item['time']] = -5
            else:
                dict_build_failed[item['time']] = -5
        if item[OperatorType.NAME] == '10':
            dict_debug_run[item['time']] = -5
        if item[OperatorType.NAME] == '11':
            dict_debug_end[item['time']] = -5
    pic_data = {}
    if 'text' in leg:
        pic_data['add'] = dict_to
        pic_data['delete'] = dict_from
    if 'build' in leg:
        pic_data['build_success'] = dict_build_success
        pic_data['build_failed'] = dict_build_failed
    if 'debug' in leg:
        pic_data['debug_run'] = dict_debug_run
        pic_data['debug_end'] = dict_debug_end
    pic = pd.DataFrame(pic_data, index=rng)
    pic = pic.fillna(value=0)

    fig = tools.make_subplots(rows=4, cols=1, shared_xaxes=True)

    fig.append_trace(go.Scatter(x=pic.index, y=pic['add'], name='add'), 1, 1)
    fig.append_trace(go.Scatter(x=pic.index, y=pic['delete'], name='delete'), 2, 1)

    debug_list = []
    pre_run = None
    for t in pic.index:
        if pic.loc[t, 'debug_run'] != 0:
            pre_run = t
        if pic.loc[t, 'debug_end'] != 0:
            if pre_run is None:
                continue
            debug_list.append([pre_run, t])
            pre_run = None

    if len(debug_list) != 0:
        y_begin = int(-len(debug_list) / 2)
        x = [debug_list[0][0], debug_list[0][1]]
        y = [y_begin, y_begin]
        pre_end = debug_list[0][1]
        for tx, ty in zip(debug_list[1:], range(y_begin + 1, y_begin + len(debug_list))):
            x.append(pre_end + (tx[0] - pre_end) / 2)
            y.append(None)
            x.extend(tx)
            y.extend([ty, ty])
            pre_end = tx[1]
        fig.append_trace(go.Scatter(x=x, y=y, name='debug', line={'width': 10}), 3, 1)

    build_success_x = []
    build_failed_x = []
    for t in pic.index:
        if pic.loc[t, 'build_success'] != 0:
            build_success_x.append(t)
        if pic.loc[t, 'build_failed'] != 0:
            build_failed_x.append(t)
    fig.append_trace(go.Scatter(x=build_success_x, y=['success'] * len(build_success_x),
                                name='build_success', mode='markers'), 4, 1)
    fig.append_trace(
        go.Scatter(x=build_failed_x, y=['failed'] * len(build_failed_x), name='build_failed', mode='markers')
        , 4, 1)

    return fig


def show_time_detached(user_data: list, problemid: str=None, title: str= 'coding time'):
    """
    统计不同编码、调试时间的人数。可以得到整体与每题的编码时间人数分布。
    横轴为时间段（min），纵轴为人数（个）
    分为总体情况与每题目情况
    :param user_data: [{'userid':str, 'problemid':str, 'dayid':int, 'code_time':int, 'debug_time':int}]
    :param title: figure title
    :return:
    """
    df = pd.DataFrame(user_data)
    df = df.set_index(['problemid'])
    if problemid:
        df = df.loc[problemid]
    df = df.groupby(['userid'])['code_time', 'debug_time'].sum()
    df = df.sort_index()
    max_time = df['code_time'].max()
    max_time2 = df['debug_time'].max()
    if max_time < max_time2:
        max_time = max_time2

    coding_trace = go.Histogram(x=df['code_time'], histnorm='count', name='code time', xbins=dict(start=0, end=max_time, size=10))
    debug_trace = go.Histogram(x=df['debug_time'], histnorm='count', name='debug time', xbins=dict(start=0, end=max_time, size=10))
    layout = go.Layout(title=title, xaxis=dict(title='time/min'), yaxis=dict(title='count'), bargap=0.2, bargroupgap=0.1)
    fig = go.Figure(data=[coding_trace, debug_trace], layout=layout)
    return fig


def show_time_total(user_data: list, problemid: str=None, title: str= 'total coding time'):
    """
    统计不同编码、调试时间的人数。可以得到整体与每题的编码时间人数分布。
    横轴为时间段（min），纵轴为人数（个）
    分为总体情况与每题目情况
    :param user_data: [{'userid':str, 'problemid':str, 'dayid':int, 'code_time':int, 'debug_time':int}]
    :param title: figure title
    :return:
    """
    df = pd.DataFrame(user_data)
    df = df.set_index(['problemid'])
    if problemid:
        df = df.loc[problemid]
    df = df.groupby(['userid'])['code_time', 'debug_time'].sum()
    df = df.sort_index()
    df['work_time'] = df['code_time'] + df['debug_time']
    max_time = df['work_time'].max()

    total_trace = go.Histogram(x=df['work_time'], histnorm='count', name='code time', xbins=dict(start=0, end=max_time, size=20))
    layout = go.Layout(title=title, xaxis=dict(title='time/min'), yaxis=dict(title='count'), bargap=0.2, bargroupgap=0.1)
    fig = go.Figure(data=[total_trace], layout=layout)
    return fig


def show_time_perproblem(user_data: list, userid: str=None, problem_list: list=[], title: str=None):
    """
    统计个人每道题的编码，调试时间。可以得到每个人的每题编码时间。
    横轴为题目编号，纵轴为所花时间（min）
    :param user_data: [{'userid':str, 'problemid':str, 'dayid':int, 'code_time':int, 'debug_time':int}]
    :param userid: 学号
    :return:
    """
    df = pd.DataFrame(user_data)
    df = df.set_index('userid')
    if userid:
        df = df.loc[userid]
    df = df.groupby(['problemid'])['code_time', 'debug_time'].sum()
    for problem in problem_list:
        if problem not in df.index:
            df.loc[problem] = {'code_time': 0, 'debug_time': 0}
    df = df.sort_index()

    if not title:
        if not userid:
            userid = 'all'
        title = userid + ' working time'

    coding_trace = go.Bar(x=df.index, y=df['code_time'], name='code time')
    debug_trace = go.Bar(x=df.index, y=df['debug_time'], name='debug time')
    layout = go.Layout(title=title, barmode='stack')
    fig = go.Figure(data=[coding_trace, debug_trace], layout=layout)
    return fig


def show_time_div_preproblem(user_data: list, problem_list:list = [], title: str = 'average time ratio'):
    """
    统计每题学生编码的平均时间的比例。可以发现不同题目的编码调试难度
    横轴为题目，纵轴为学生在该题的编码、调试比例。
    :param user_data: [{'userid':str, 'problemid':str, 'dayid':int, 'code_time':int, 'debug_time':int}]
    :return:
    """
    df = pd.DataFrame(user_data)
    gp = df.groupby(['userid', 'problemid'])
    df = gp['code_time', 'debug_time'].sum()
    df = df.reset_index(level=['userid', 'problemid'])
    df['average'] = df['code_time']/df['debug_time']
    df = df.groupby(['problemid'])['average'].mean()
    for problem in problem_list:
        if problem not in df.index:
            df.loc[problem] = {'average': 0}
    df = df.sort_values(ascending=False)

    trace = go.Bar(x=df.index, y=df, name='average time ratio')
    layout = go.Layout(title=title, barmode='stack')
    fig = go.Figure(data=[trace], layout=layout)
    return fig


def show_work_time(all_data: list):
    """
    统计24h内，每个时间段正在编写作业的用户人数。可以得到学生主要进行编码、完成作业的时间段。
    横轴为时间00:00-23:59，纵轴为人数（个）
    :param all_data: [{'userid':str, 'data':list}], data包含去重之后的某用户的全部操作记录
    :return:
    """
    time_dict = {}
    for i in range(24):
        time_dict[str(i)] = 0

    user_time_dict = {}
    for all_data_item in all_data:
        userid = all_data_item['userid']
        data = all_data_item['data']
        for i in range(24):
            user_time_dict[str(i)] = []
        for da in data:
            da_time = da['time']
            day = da_time.day
            hour = da_time.hour
            if day not in user_time_dict[str(hour)]:
                user_time_dict[str(hour)].append(day)
        for k in user_time_dict.keys():
            time_dict[k] += len(user_time_dict[k])

    time_dict = sorted(time_dict.items(), key=lambda d: int(d[0]))

    x = []
    y = []
    for item in time_dict:
        x.append(item[0])
        y.append(item[1])

    print(x)
    print(y)
    title = 'work hours'
    trace = go.Scatter(x=x, y=y, name='work time per day')
    layout = go.Layout(title=title, barmode='stack', showlegend=True, xaxis=dict(autotick=False))
    print(layout.help('annotations'))
    fig = go.Figure(data=[trace], layout=layout)
    return fig


def show_work_time_personal(word_time_data: list, userid: str, day_list: list=[], title: str=None):
    """
    统计个人在作业期间每天的编码时间。可以得到用户每天编码所花时间的情况。
    横轴为天数，纵轴为时间（min）
    :param word_time_data: [{'userid':str, 'problemid':str, 'dayid':int, 'code_time':int, 'debug_time':int}]
    :param userid: 学号
    :param title 标题
    :return:
    """
    df = pd.DataFrame(word_time_data)
    df = df.set_index('userid')
    if userid:
        df = df.loc[userid]
    df = df.groupby('dayid')['code_time', 'debug_time'].sum()
    df['work_time'] = df['code_time'] + df['debug_time']
    for day in day_list:
        if day not in df.index:
            df.loc[day] = {'code_time': 0, 'debug_time': 0, 'work_time':0}
    df = df.sort_index()


    title = userid + ' work time per day'

    trace = go.Scatter(x=df.index, y=df['work_time'], name='work time per day')
    layout = go.Layout(title=title, barmode='stack')
    fig = go.Figure(data=[trace], layout=layout)
    return fig
