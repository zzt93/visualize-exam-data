import plotly.plotly as py
import plotly.offline as offline


def save_as_png(figure, filename):
    """
    将图表保存为.png格式
    :param figure:list
    :param filename:string
    :return:
    """

    py.sign_in('Panjks-', 't59Jl2ktBmwycqKAX8uQ')
    py.image.save_as(figure, filename=filename)


def save_as_html(figure, filename):
    """
    将图表保存为.html格式
    :param figure: list
    :param filename: string
    :return:
    """
    offline.plot(figure, auto_open=False, filename=filename)