from backend.interface.controller import get_all_problem_id, get_all_day_id,get_all_user_id,get_build_error_count, get_build_failed_count, get_coding_speed, get_debug_personal, get_debug_total, get_paste_content_classification, get_paste_length_personal, get_problem_avgscore, get_problem_score, get_process_personal, get_score, get_testcase_error, get_time_div_total, get_time_less, get_time_personal, get_time_total, get_work_time, get_work_time_personal
from present.plot_time import show_process_personal, show_time_detached, show_time_div_preproblem, show_time_perproblem, show_time_total, show_work_time, show_work_time_personal
from present.plot_copy import show_paste_length_personal, show_paste_content_classification
from present.plot_util import save_as_png, save_as_html, save_as_txt
import plotly.offline as py
import os
from common.plot_constants import ROOT_PATH, TIME_PATH, COPY_PATH



def init():
    os.chdir("..")


# time
def run_process_personal():
    result = get_process_personal()
    print(result[0])
    print(result[1])
    print(result[2])


def run_time_perproblem():
    pass


def run_time_div_preproblem():
    pass


def run_work_time():
    pass


def run_work_time_personal():
    pass


# copy
def run_paste_length_personal():
    pass


def run_paste_content_classification():
    pass


# insert
def run_coding_speed():
    pass


# debug
def run_debug_personal():
    pass


def run_debug_total():
    pass


# score
def run_score():
    pass


def run_problem_score():
    pass


# build
def run_build_error_count():
    pass


# check
def run_build_failed_count():
    pass


def run_time_less():
    pass


if __name__ == '__main__':
    init()
    problems = get_all_problem_id()
    users = get_all_user_id()

    # show_process_personal

    # result = get_time_total()


    # # show_time_detached
    # method_path = os.path.join(TIME_PATH, 'user_time')
    # method_path = os.path.join(method_path, 'time_detached')
    # fig = show_time_detached(result, None)
    # save_as_html(fig, method_path, 'total.html')
    # for pro in problems:
    #     fig = show_time_detached(result, pro)
    #     save_as_html(fig, method_path, 'Q'+str(pro)+'.html')
    #
    # # show_time_total
    # method_path = os.path.join(TIME_PATH, 'user_time')
    # method_path = os.path.join(method_path, 'time_total')
    # fig = show_time_total(result, None)
    # save_as_html(fig, method_path, 'total.html')
    # for pro in problems:
    #     fig = show_time_total(result, pro)
    #     save_as_html(fig, method_path, 'Q' + str(pro) + '.html')
    #
    # show_time_perproblem
    # method_path = os.path.join(TIME_PATH, 'problem_time')
    # method_path = os.path.join(method_path, 'total_time')
    # fig = show_time_perproblem(result, None, problems)
    # if fig != None:
    #     save_as_html(fig, method_path, 'total.html')
    # for u in users:
    #     fig = show_time_perproblem(result, u, problems)
    #     if fig != None:
    #         save_as_html(fig, method_path, u+'.html')

    # show_time_div_preproblem
    # method_path = os.path.join(TIME_PATH, 'problem_time')
    # method_path = os.path.join(method_path, 'div_time')
    # fig = show_time_div_preproblem(result, problems)
    # if fig != None:
    #     save_as_html(fig, method_path, 'total.html')


    # work_time_data = get_work_time()

    # show_work_time
    # method_path = os.path.join(TIME_PATH, 'work_time')
    # method_path = os.path.join(method_path, 'per_hour')
    #
    # fig = show_work_time(work_time_data)
    # if fig != None:
    #     save_as_html(fig, method_path, 'total.html')


    # show_work_time_personal
    # method_path = os.path.join(TIME_PATH, 'work_time')
    # method_path = os.path.join(method_path, 'per_day')
    #
    # for u in users:
    #     fig = show_work_time_personal(result, userid=u)
    #     if fig != None:
    #         save_as_html(fig, method_path, str(u)+'.html')



    paste_data = get_paste_length_personal()
    paste_length_data = [ t['pasta_data'] for t in paste_data]

    # show_paste_length_personal
    method_path = os.path.join(COPY_PATH, 'paste_length')
    for u in users:
        fig = show_paste_length_personal(paste_length_data, u)
        if fig != None:
            save_as_html(fig, method_path, str(u)+'.html')


    clas = get_paste_content_classification()
    paste_cla_data = [t['paste_data'] for t in clas]
    # show_paste_content_classification
    method_path = os.path.join(COPY_PATH, 'paste_classification')
    fig = show_paste_content_classification(paste_cla_data, None)
    save_as_html(fig, method_path, 'total.html')
    for u in users:
        fig = show_paste_content_classification(paste_cla_data, u)
        if fig != None:
            save_as_html(fig, method_path, str(u)+'.html')





