import os
from zipfile import ZipFile

from backend.util.config import LOG_DIR
from backend.util.log_data_transform import transform_test_log
from backend.util.mysql_connector import MysqlConnector
from backend.util.path_util import scan_dir


def extract_score(log_file_zip, times):
    test_log_handler = []
    if os.path.isfile(log_file_zip):
        try:
            with ZipFile(log_file_zip) as myzip:
                for f in myzip.infolist():
                    (filepath, tempfilename) = os.path.split(f.filename)
                    (shortname, extension) = os.path.splitext(tempfilename)
                    if shortname == 'app':
                        test_log_handler.append(myzip.open(f.filename))
        except OSError as e:
            print(log_file_zip)
            print(e)

    test_cases = {}
    log = {}
    for handler in test_log_handler:
        log_list = transform_test_log(handler)
        for line in log_list:
            if line['time'] in times:
                continue
            else:
                times.add(line['time'])

            ac_list = line['message']['AC']
            ac = len(ac_list)
            wa_list = line['message']['WA']
            wa = len(wa_list)
            tie_list = line['message']['TIE']
            tie = len(tie_list)
            rte = 0
            rte_list = []
            if 'RTE' in line['message']:
                rte_list = line['message']['RTE']
                rte = len(rte_list)
            s = ac / (ac + wa + tie + rte)
            qid_ = line['qid']

            wa_list.extend(tie_list)
            wa_list.extend(rte_list)
            test_dict = {'ac': ac_list, 'wrong': wa_list}
            score_dict = {'score': s}
            score_dict.update(test_dict)
            if qid_ in log:
                if log[qid_] is not None and log[qid_]['score'] < s:
                    log[qid_] = score_dict
            else:
                log[qid_] = score_dict


            if qid_ in test_cases:
                test_cases[qid_].append(test_dict)
            else:
                test_cases[qid_] = [test_dict]
    return log, test_cases


def merge_log_score(eid, file_to_id=None, student_list=None):
    if file_to_id is None or student_list is None:
        file_to_id, student_list = file_to_sid(eid)
    score = {}
    test_cases = {}
    times = {}
    for sid in student_list:
        score[sid] = {}
        test_cases[sid] = {}
        times[sid] = set()

    for file_name in scan_dir(LOG_DIR):
        if file_name not in file_to_id:
            continue
        student_id = file_to_id[file_name]
        score_log, test_cases_log = extract_score(file_name, times[student_id])
        # assert student_id in score
        for question_id, score_dict in score_log.items():
            if question_id in score[student_id]:
                if score[student_id][question_id] is not None and score[student_id][question_id]['score'] > score_dict['score']:
                    score[student_id][question_id] = score_dict
            else:
                score[student_id][question_id] = score_dict

        for question_id, dict_list in test_cases_log.items():
            if question_id in test_cases[student_id]:
                test_cases[student_id][question_id].extend(dict_list)
            else:
                test_cases[student_id][question_id] = dict_list

    return score, test_cases


def file_to_sid(eid):
    connector = MysqlConnector()
    student_list = connector.get_all_student(eid)
    file_to_id = {}
    for sid in student_list:
        file_to_id.update(connector.get_student_file(sid, eid))

    connector.close()
    return file_to_id, student_list