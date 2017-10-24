import plotly.plotly
import plotly.graph_objs as go
import pandas as pd


def show_coding_speed(speed_data):
    """
    统计学生平均编码速度（每分钟插入字符）的人数分布。可以整体评估学生的编码速度。
    横轴为编码速度（个/min），纵轴为人数
    :param speed_data: [{'student_id':str, 'speed':float}]
    :return:figure
    """
    df = pd.DataFrame(speed_data)
    df = df.set_index(['student_id'])
    # df = df.groupby(['student_id'])['speed'].sum()
    max_speed = 100
    trace = go.Histogram(
        x=df['speed'],
        histnorm='count',
        name='coding speed',
        xbins=dict(start=0, end=max_speed, size=2)
    )
    data = [trace]
    layout = go.Layout(
        title='学生平均编码速度分布',
        xaxis=dict(title='个/min'),
        yaxis=dict(title='count'),
        barmode='Stack',
    )
    figure = go.Figure(data=data, layout=layout)
    return figure
