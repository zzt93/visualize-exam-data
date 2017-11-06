from backend.interface.controller import get_all_problem_id, get_all_day_id,get_all_user_id,get_build_error_count, get_build_failed_count, get_coding_speed, get_debug_personal, get_debug_total, get_paste_content_classification, get_paste_length_personal, get_problem_avgscore, get_problem_score, get_process_personal, get_score, get_testcase_error, get_time_div_total, get_time_less, get_time_personal, get_time_total, get_work_time, get_work_time_personal
from present.plot_time import show_process_personal, show_time_detached, show_time_div_preproblem, show_time_perproblem, show_time_total, show_work_time, show_work_time_personal
from present.plot_copy import show_paste_length_personal, show_paste_content_classification
from present.plot_insert import show_coding_speed
from present.plot_debug import show_debug_personal, show_debug_total
from present.plot_score import show_score, show_problem_avgscore, show_problem_score, show_testcase_error
from present.plot_build import show_build_error_count, show_build_failed_count
from present.plot_check import show_time_less, show_time_less_logic
from present.plot_util import save_as_png, save_as_html, save_as_txt
import plotly.offline as py
import os
from common.plot_constants import ROOT_PATH, TIME_PATH, COPY_PATH, INSERT_PATH, DEBUG_PATH, SCORE_PATH, BUILD_PATH, OTHER_PATH



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

    result = get_time_total()


    # show_time_detached
    print('start show time detached')
    method_path = os.path.join(TIME_PATH, 'user_time')
    method_path = os.path.join(method_path, 'time_detached')
    fig = show_time_detached(result, None)
    save_as_html(fig, method_path, 'total.html')
    for pro in problems:
        fig = show_time_detached(result, pro)
        save_as_html(fig, method_path, 'Q'+str(pro)+'.html')

    # show_time_total
    print('start show time total')
    method_path = os.path.join(TIME_PATH, 'user_time')
    method_path = os.path.join(method_path, 'time_total')
    fig = show_time_total(result, None)
    save_as_html(fig, method_path, 'total.html')
    for pro in problems:
        fig = show_time_total(result, pro)
        save_as_html(fig, method_path, 'Q' + str(pro) + '.html')

    # show_time_perproblem
    print('start show time preproblem')
    method_path = os.path.join(TIME_PATH, 'problem_time')
    method_path = os.path.join(method_path, 'total_time')
    fig = show_time_perproblem(result, None, problems)
    if fig != None:
        save_as_html(fig, method_path, 'total.html')
    for u in users:
        fig = show_time_perproblem(result, u, problems)
        if fig != None:
            save_as_html(fig, method_path, u+'.html')

    # show_time_div_preproblem
    print('start show time div preproblem')
    method_path = os.path.join(TIME_PATH, 'problem_time')
    method_path = os.path.join(method_path, 'div_time')
    fig = show_time_div_preproblem(result, problems)
    if fig != None:
        save_as_html(fig, method_path, 'total.html')


    work_time_data = get_work_time()

    # show_work_time
    print('start show work time')
    method_path = os.path.join(TIME_PATH, 'work_time')
    method_path = os.path.join(method_path, 'per_hour')

    fig = show_work_time(work_time_data)
    if fig != None:
        save_as_html(fig, method_path, 'total.html')


    # show_work_time_personal
    print('start show work time personal')
    method_path = os.path.join(TIME_PATH, 'work_time')
    method_path = os.path.join(method_path, 'per_day')

    for u in users:
        fig = show_work_time_personal(result, userid=u)
        if fig != None:
            save_as_html(fig, method_path, str(u)+'.html')



    print('start paste length personal')
    paste_data = get_paste_length_personal()
    paste_length_data = [t['pasta_data'] for t in paste_data]

    # show_paste_length_personal
    method_path = os.path.join(COPY_PATH, 'paste_length')
    for u in users:
        fig = show_paste_length_personal(paste_length_data, u)
        if fig != None:
            save_as_html(fig, method_path, str(u)+'.html')


    print('start paste content classification')
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




    print('start code speed')
    code_speed_data = get_coding_speed()
    # show_coding_speed
    method_path = os.path.join(INSERT_PATH, 'code_speed')
    fig = show_coding_speed(code_speed_data)
    save_as_html(fig, method_path, 'total.html')


    print('start debug personal')
    debug_per_data = get_debug_personal()
    debug_person_data = [t['debug_data'] for t in debug_per_data]
    # show_debug_personal
    method_path = os.path.join(DEBUG_PATH, 'per_problem')
    fig = show_debug_personal(debug_person_data, None)
    if fig:
        save_as_html(fig, method_path, 'total.html')
    for u in users:
        fig = show_debug_personal(debug_person_data, u)
        if fig:
            save_as_html(fig, method_path, str(u)+'.html')


    print('start debug total')
    debug_total_data = get_debug_total()
    # show_debug_total
    method_path = os.path.join(DEBUG_PATH, 'debug_count')
    fig = show_debug_total(debug_total_data)
    if fig:
        save_as_html(fig, method_path, 'total.html')


    print('start score')
    score_data = get_score()
    for s in score_data:
        s['score'] = s['score']/15
    # show_score
    fig = show_score(score_data)
    if fig:
        save_as_html(fig, SCORE_PATH, 'total.html')


    print('start score preproblem')
    score_problem_data = get_problem_score()
    # show_problem_score
    method_path = os.path.join(SCORE_PATH, 'pre_problem')
    for p in problems:
        fig = show_problem_score(score_problem_data, str(p))
        if fig:
            save_as_html(fig, method_path, 'Q'+str(p)+'.html')


    print('start testcase error')
    test_data = get_testcase_error()
    testcase_data = []
    for te in test_data:
        testcase_data.extend(te['test_data'])
    # show_testcase_error
    method_path = os.path.join(SCORE_PATH, 'testcase')
    for p in problems:
        fig = show_testcase_error(testcase_data, str(p))
        if fig:
            save_as_html(fig, method_path, 'Q'+str(p)+'.html')


    print('start problem avg score')
    ave_score_data = get_problem_avgscore()
    # show_problem_avgscore
    fig = show_problem_avgscore(ave_score_data)
    save_as_html(fig, SCORE_PATH, 'ave_total.html')

    print('start build error count')
    build_error_data = get_build_error_count()
    # show_build_error_count
    method_path = os.path.join(BUILD_PATH, 'error_code')
    fig = show_build_error_count(build_error_data, None)
    if fig:
        save_as_html(fig, method_path, 'total.html')
    for p in problems:
        fig = show_build_error_count(build_error_data, str(p))
        if fig:
            save_as_html(fig, method_path, 'Q'+str(p)+'.html')

    print('start build failed count')
    build_failed_data = get_build_failed_count()
    # show_build_failed_count
    fig = show_build_failed_count(build_failed_data)
    if fig:
        save_as_html(fig, BUILD_PATH, 'build_failed_total.html')


    print('start time less')
    less = get_time_less()
    res = show_time_less(less)
    # show_time_less
    method_path = os.path.join(ROOT_PATH, )
    res_data, res_count = show_time_less_logic(result)
    save_as_txt(res_data, method_path, 'less_time_user.txt')
    save_as_txt(res_count, method_path, 'less_time_count.txt')




























