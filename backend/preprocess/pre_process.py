import os
from zipfile import ZipFile

from backend.util.config import *
from backend.util.log_data_transform import transform_test_log
from backend.util.mysql_connector import MysqlConnector
from backend.util.scan_database import scan_dir


def extract_score(log_file_zip):
    test_log_handler = []
    if os.path.isfile(log_file_zip):
        with ZipFile(log_file_zip) as myzip:
            for f in myzip.infolist():
                (filepath, tempfilename) = os.path.split(f.filename)
                (shortname, extension) = os.path.splitext(tempfilename)
                if shortname == 'app':
                    test_log_handler.append(myzip.open(f.filename))

    log = {}
    for handler in test_log_handler:
        log_list = transform_test_log(handler)
        for line in log_list:
            ac = len(line['message']['AC'])
            wa = len(line['message']['WA'])
            tie = len(line['message']['TIE'])
            rte = 0
            if 'RTE' in line['message']:
                rte = len(line['message']['RTE'])
            s = ac / (ac + wa + tie + rte)
            if line['qid'] in log:
                if log[line['qid']] < s:
                    log[line['qid']] = s
            else:
                log[line['qid']] = s
    return log


def extract_log_score():
    file_to_id = file_to_sid()
    score = {}
    for sid in range(STUDENT_ID_START, STUDENT_ID_END):
        score[sid] = {}

    for file_name in scan_dir(LOG_DIR):
        if file_name not in file_to_id:
            continue
        tmp = extract_score(file_name)
        student_id = file_to_id[file_name]
        assert student_id in score
        for problem_id, value in tmp.items():
            if problem_id in score[student_id]:
                if score[student_id][problem_id] > value:
                    score[student_id][problem_id] = value
            else:
                score[student_id][problem_id] = value

    return score


def extract_monitor(monitor_file_zip):
    monitor_handler = []
    if os.path.isfile(monitor_file_zip):
        with ZipFile(monitor_file_zip) as myzip:
            for f in myzip.infolist():
                (filepath, tempfilename) = os.path.split(f.filename)
                (shortname, extension) = os.path.splitext(tempfilename)
                if shortname == 'app':
                    monitor_handler.append(myzip.open(f.filename))



def extract_monitor_info():
    file_to_id = file_to_sid()
    for file_name in scan_dir(MONITOR_DIR):
        if file_name not in file_to_id:
            continue
        extract_monitor(file_name)
        sid = file_to_id[file_name]


def file_to_sid():
    connector = MysqlConnector()
    file_to_id = {}
    for sid in range(STUDENT_ID_START, STUDENT_ID_END):
        file_to_id.update(connector.get_student_file(sid, FROM_DATE, TO_DATE))

    connector.close()
    return file_to_id


def sort_by_time():
    return


if __name__ == '__main__':
    os.chdir('../../')
    extract_monitor_info()
