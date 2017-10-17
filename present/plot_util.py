import plotly.plotly as py
import plotly.offline as offline
import re
import os


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


def save_as_txt(content, filename):
    with open(filename, 'w') as f:
        for student in content:
            for key in student:
                f.write(key+':'+str(student[key])+'\t')
            f.write('\n')


def deal_result(content):
    lines = content.split("\n")
    for temp in lines:
        temp = temp.strip()
        temps = temp.split(">")
        if len(temps) > 1:
            line = temp[2:]
        else:
            line = temp
        pattern = re.compile(r"^(Build succeeded|生成成功).*")
        match = pattern.search(line)
        if match:
            return 1
        pattern = re.compile(r"^(Build FAILED|生成失败).*")
        match = pattern.search(line)
        if match:
            return 0
    return 0
