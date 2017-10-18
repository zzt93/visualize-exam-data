import os
from zipfile import ZipFile

from backend.database.model import *
from backend.util.collection_util import unique_dict
from backend.util.config import *
from backend.util.constant import OperatorType
from backend.util.log_data_transform import transform_test_log
from backend.util.monitor_data_transform import read_data
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


def merge_log_score(eid, file_to_id=None, student_list=None):
    if file_to_id is None or student_list is None:
        file_to_id, student_list = file_to_sid(eid)
    score = {}
    for sid in student_list:
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
    if os.path.isfile(monitor_file_zip):
        with ZipFile(monitor_file_zip) as myzip:
            for f in myzip.infolist():
                (filepath, tempfilename) = os.path.split(f.filename)
                if tempfilename == r'Dao\log.db':
                    return read_data(myzip.extract(f, path='/tmp'))


def merge_monitor(new, original):
    original.extend(new)
    return unique_dict(original)


def merge_monitor_info(eid, file_to_id=None):
    if file_to_id is None:
        file_to_id, not_used = file_to_sid(eid)

    res = {}
    for file_name in scan_dir(MONITOR_DIR):
        if file_name not in file_to_id:
            continue
        monitor_list = extract_monitor(file_name)
        sid = file_to_id[file_name]
        if sid not in res:
            res[sid] = monitor_list
        else:
            merge_monitor(monitor_list, res[sid])
    return res


def file_to_sid(eid):
    connector = MysqlConnector()
    student_list = connector.get_all_student(eid)
    file_to_id = {}
    for sid in student_list:
        file_to_id.update(connector.get_student_file(sid, FROM_DATE, TO_DATE))

    connector.close()
    return file_to_id, student_list


def store_to_db(eid):
    # store exam
    Exam(eid).save()

    file_to_id, student_list = file_to_sid(eid)
    # store student
    for sid in student_list:
        Student(sid).save()
        StudentInExam(student_id=sid, eid=eid).save()
    # store score
    score = merge_log_score(file_to_id)
    for student_id, value in score.items():
        for question_id, s in value.items():
            StudentQuestionResult(student_id=student_id, question_id=question_id, score=score).save()
    # store other monitor inof
    monitor = merge_monitor_info(file_to_id)
    for sid, l in monitor.items():
        for m in l:
            operator_ = m['operator']
            # m: {'id': 1, 'time': datetime.datetime(2017, 9, 22, 11, 27, 36), 'operator': '4', 'name': '用例文档.md', 'path': 'E:\\大二软工二\\', 'content': '<table>', 'happentime': 636416764559624377, 'project': 'Miscellaneous Files'}
            Operation(operator_, m['time'], sid).save()
            category = OperatorType.id_to_category(operator_)
            if category == 'text':
                print()
            elif category == 'content':
                print()
            elif category == 'debug':
                d, created = Debug.get_or_create(student_id=sid, exam_id=eid)
                d.debug_count = d.debug_count + 1
                d.save()
                print()
            elif category == 'test':
                print()
            elif category == 'build':
                build, created = BuildError.get_or_create(question_id=m[''], error_code=m[''])
                print()


def sort_by_time():
    return


if __name__ == '__main__':
    os.chdir('../../')
    # unique_dict([{'x': 1, 'y': 2}, {'x': 1, 'y': 2}, {'x': 2, 'y': 2}])
    merge_monitor_info(EID)
