import os
from collections import OrderedDict
from zipfile import ZipFile

from backend.database.model import *
from backend.util.collection_util import sort_dict, minus_dict
from backend.util.config import *
from backend.util.constant import OperatorType, INVALID
from backend.util.error_util import error_extraction
from backend.util.log_data_transform import transform_test_log
from backend.util.monitor_data_transform import read_data
from backend.util.mysql_connector import MysqlConnector
from backend.util.path_util import scan_dir

PASTE_TYPE = 123

FIVE_MIN = 5 * 60


def extract_score(log_file_zip, times):
    test_log_handler = []
    if os.path.isfile(log_file_zip):
        with ZipFile(log_file_zip) as myzip:
            for f in myzip.infolist():
                (filepath, tempfilename) = os.path.split(f.filename)
                (shortname, extension) = os.path.splitext(tempfilename)
                if shortname == 'app':
                    test_log_handler.append(myzip.open(f.filename))

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
            if qid_ in log:
                if log[qid_] < s:
                    log[qid_] = s
            else:
                log[qid_] = s

            wa_list.extend(tie_list)
            wa_list.extend(rte_list)
            res_dict = {'ac': ac_list, 'wrong': wa_list}
            if qid_ in test_cases:
                test_cases[qid_].append(res_dict)
            else:
                test_cases[qid_] = [res_dict]
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
        assert student_id in score
        for question_id, score_value in score_log.items():
            if question_id in score[student_id]:
                if score[student_id][question_id] > score_value:
                    score[student_id][question_id] = score_value
            else:
                score[student_id][question_id] = score_value

        for question_id, dict_list in test_cases_log.items():
            if question_id in test_cases[student_id]:
                test_cases[student_id][question_id].extend(dict_list)
            else:
                test_cases[student_id][question_id] = dict_list

    return score, test_cases


def extract_monitor(monitor_file_zip):
    if os.path.isfile(monitor_file_zip):
        with ZipFile(monitor_file_zip) as myzip:
            for f in myzip.infolist():
                (filepath, tempfilename) = os.path.split(f.filename)
                if tempfilename == r'Dao\log.db':
                    return read_data(myzip.extract(f, path='/tmp'))


def merge_monitor(new, original):
    minus_dict(original, new)
    original.extend(new)


def merge_monitor_info(eid, file_to_id=None):
    if file_to_id is None:
        file_to_id, not_used = file_to_sid(eid)

    res = {}
    for file_name in scan_dir(MONITOR_DIR):
        if file_name not in file_to_id:
            continue
        sid = file_to_id[file_name]
        monitor_list = extract_monitor(file_name)
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


def extract_question_id(s):
    try:
        tmp = int(s[1:])
    except ValueError:
        return INVALID
    from backend.interface.controller import get_all_problem_id
    ids = get_all_problem_id()
    if tmp not in ids:
        return INVALID
    return tmp


def get_question_set(eid):
    mysql = MysqlConnector()
    question_id_set = mysql.get_question_set(EID)
    mysql.close()
    return question_id_set


def store_to_db(eid):
    # store exam
    Exam.get_or_create(exam_id=eid)

    # store question
    question_set = get_question_set(eid)
    for question_id in question_set:
        QuestionInExam.get_or_create(exam_id=eid, question_id=question_id)

    file_to_id, student_list = file_to_sid(eid)
    #
    # store student
    for sid in student_list:
        Student.get_or_create(student_id=sid)
        StudentInExam.get_or_create(student_id=sid, exam_id=eid)
    #
    # store score
    score, test_cases = merge_log_score(eid, file_to_id)
    # for student_id, value in score.items():
    #     for question_id, s in value.items():
    #         StudentQuestionResult.create(student_id=student_id, question_id=question_id, score=score)
    #
    # # store test cases
    # for student_id, question_dict in test_cases:
    #     for question_id, dict_list in question_dict:
    #         for ac_dict in dict_list:
    #             TestCase.create(student_id=student_id, question_id=question_id, ac_list=ac_dict['ac'], wrong_list=ac_dict['wrong'])
    #
    # store other monitor inof
    monitor = merge_monitor_info(eid, file_to_id)
    for sid, info_list in monitor.items():
        debug_time = {}
        code_time = {}
        code_len = 0
        info_list = sorted(info_list, key=lambda d: d['time'])
        for monitor_dict in info_list:
            op_type = int(monitor_dict['operator'])
            Operation.create(op_type=op_type, op_happen_time=monitor_dict['time'], student_id=sid)
            category = OperatorType.id_to_category(op_type)
            if category == 'text' or category == 'content':
                question_id = INVALID
                if category == 'text':
                    # {'id': 1, 'time': datetime.datetime(2017, 9, 22, 11, 27, 36), 'operator': '4', 'name': '用例文档.md', 'path': 'E:\\大二软工二\\', 'content': '<table>', 'happentime': 636416764559624377, 'project': 'Miscellaneous Files'}
                    # {'id': 114, 'time': datetime.datetime(2017, 9, 28, 14, 53, 14), 'operator': '2', 'name': 'Main.cpp', 'path': 'c:\\Users\\43796\\documents\\visual studio 2013\\Projects\\Exam36\\Q65\\', 'content': 'int n, a[100000],sum=0;', 'happentime': 636422071943562630, 'project': 'Q65'}
                    # {'id': 41, 'time': datetime.datetime(2017, 9, 28, 10, 27, 54), 'operator': '3', 'name': 'Main.cpp', 'path': 'c:\\Users\\43796\\documents\\visual studio 2013\\Projects\\Exam36\\Q63\\', 'content': 'cin >> x;\r\n\t\t\tfor (int i = 0; i < n; i++)\r\n\t\t\t\ta[i] += x;\r\n\t\t\tbreak;', 'happentime': 636421912749274277, 'project': 'Q63'}
                    # {'id': 42, 'time': datetime.datetime(2017, 9, 28, 10, 28, 1), 'operator': '4', 'name': 'Main.cpp', 'path': 'c:\\Users\\43796\\documents\\visual studio 2013\\Projects\\Exam36\\Q63\\', 'content': "case 's':\r\n\t\t\tcin >> x;\r\n\t\t\tfor (int i = 0; i < n; i++)\r\n\t\t\t\ta[i] -= x;\r\n\t\t\tbreak;", 'happentime': 636421912814745993, 'project': 'Q63'}
                    question_id = extract_question_id_from_path(monitor_dict['path'])
                    if op_type == 3:  # paste
                        paste, created = Paste.get_or_create(student_id=sid, question_id=question_id,
                                                             happen_time=monitor_dict['time'])
                        paste.paste_content = monitor_dict['content']
                        paste.paste_type = PASTE_TYPE
                        paste.save()
                elif category == 'content':
                    # {'id': 5, 'time': datetime.datetime(2017, 9, 27, 17, 16, 44), 'operator': '5', 'fullpath': 'C:\\Users\\89749\\Desktop\\C++_Homeworks\\Q2\\Q2\\Q2\\main.cpp', 'textfrom': '', 'textto': '<>', 'line': 1, 'lineoffset': 9, 'happentime': 636421294046897697, 'project': 'Q2'}
                    # {'id': 1759, 'time': datetime.datetime(2017, 9, 28, 16, 35, 48), 'operator': '6', 'fullpath': 'c:\\Users\\43796\\documents\\visual studio 2013\\Projects\\Exam36\\Q69\\Main.cpp', 'textfrom': 'isp\r\n', 'textto': 'isPalindrome', 'line': 18, 'lineoffset': 7, 'happentime': 636422133483868599, 'project': 'Q69'}
                    # {'id': 1717, 'time': datetime.datetime(2017, 9, 28, 16, 33, 20), 'operator': '7', 'fullpath': 'c:\\Users\\43796\\documents\\visual studio 2013\\Projects\\Exam36\\Q69\\Main.cpp', 'textfrom': 'break', 'textto': '', 'line': 8, 'lineoffset': 3, 'happentime': 636422132007669805, 'project': 'Q69'}
                    # {'id': 1612, 'time': datetime.datetime(2017, 9, 28, 16, 4, 45), 'operator': '8', 'fullpath': 'c:\\Users\\43796\\documents\\visual studio 2013\\Projects\\Exam36\\Q68\\Main.cpp', 'textfrom': '', 'textto': '', 'line': 22, 'lineoffset': 21, 'happentime': 636422114855703774, 'project': 'Q68'}
                    question_id = extract_question_id_from_path(monitor_dict['fullpath'])
                    if op_type >= 5 and op_type <= 7:
                        code_len += abs(len(monitor_dict['textfrom']) - len(monitor_dict['textto']))


                # store code time
                if question_id == INVALID:
                    continue
                code_date = monitor_dict['time']
                if question_id in code_time:
                    if code_date in code_time[question_id][code_date]:
                        assert 'last' in code_time[question_id][code_date]
                        code_time[question_id][code_date]['last'] = monitor_dict['time']
                        gap = (monitor_dict['time'] - code_time[question_id][code_date]['last']).total_seconds()
                        if gap < FIVE_MIN:
                            code_time[question_id][code_date]['count'] = code_time[question_id][code_date][
                                                                             'count'] + gap
                    else:
                        code_time[question_id][code_date] = {'last': monitor_dict['time'], 'count': 0}
                else:
                    code_time[question_id] = {}

            elif category == 'debug':
                # {'id': 1052, 'operator': '10', 'time': datetime.datetime(2017, 9, 27, 20, 52, 40), 'debug_target': 'C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe', 'debug_action': 'continue'}
                # {'id': 1053, 'operator': '11', 'time': datetime.datetime(2017, 9, 27, 20, 52, 40), 'debug_target': 'C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe', 'debug_action': 'dbgEventReasonEndProgram'}
                # {'id': 33, 'operator': '12', 'time': datetime.datetime(2017, 9, 27, 18, 35, 3), 'debug_target': 'C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q10.exe'}

                # store debug overview
                d, created = Debug.get_or_create(student_id=sid, exam_id=eid)
                d.debug_count = d.debug_count + 1
                d.save()
                # store debug time
                filename = monitor_dict['debug_target']
                question_id = extract_question_id_from_path(filename)
                if question_id == INVALID:
                    continue
                if 'debug_action' not in monitor_dict or monitor_dict['debug_action'] == 'dbgEventReasonEndProgram':
                    assert question_id in debug_time
                    gap = monitor_dict['time'] - debug_time[question_id]
                    debug_time_model, created = CodeAndDebugTime.get_or_create(student_id=sid, question_id=question_id,
                                                                               date=monitor_dict['time'].date())
                    debug_time_model.debug_time = debug_time_model.debug_time + gap
                elif monitor_dict['debug_action'] == 'start':
                    debug_time[question_id] = monitor_dict['time']

            elif category == 'test':
                print()
            elif category == 'build':
                # {'id_build_info': 94, 'time': datetime.datetime(2017, 9, 27, 20, 52, 6), 'buildstarttime_build_info': '2017/9/27 20:52:03', 'buildendtime_build_info': '2017/9/27 20:52:06', 'solutionname_build_info': 'Homework1', 'content': '1>------ 已启动全部重新生成:  项目: Q9, 配置: Debug Win32 ------\r\n1>  用于 x86 的 Microsoft (R) C/C++ 优化编译器 18.00.40629 版版权所有(C) Microsoft Corporation。  保留所有权利。\r\n1>  \r\n1>  cl /c /ZI /W3 /WX- /sdl /Od /Oy- /D _MBCS /Gm /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Fo"Debug\\\\" /Fd"Debug\\vc120.pdb" /Gd /TP /analyze- /errorReport:prompt "源.cpp"\r\n1>  \r\n1>  源.cpp\r\n1>  Microsoft (R) Incremental Linker Version 12.00.40629.0\r\n1>  Copyright (C) Microsoft Corporation.  All rights reserved.\r\n1>  \r\n1>  "/OUT:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe" /INCREMENTAL kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST "/MANIFESTUAC:level=\'asInvoker\' uiAccess=\'false\'" /manifest:embed /DEBUG "/PDB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.pdb" /TLBID:1 /DYNAMICBASE /NXCOMPAT "/IMPLIB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.lib" /MACHINE:X86 "Debug\\源.obj" \r\n1>  Q9.vcxproj -> C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe\r\n========== 全部重新生成:  成功 1 个，失败 0 个，跳过 0 个 ==========\r\n', 'id_build_project_info': 95, 'time_build_project_info': '2017/9/27 20:52:06', 'buildid': '2017/9/27 20:52:03', 'buildstarttime_build_project_info': '2017/9/27 20:52:03', 'buildendtime_build_project_info': '2017/9/27 20:52:04', 'solutionname_build_project_info': 'Homework1', 'projectname': 'Q9', 'configurationname': 'Debug|Win32', 'configurationtype': 'typeApplication', 'runcommand': 'C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe', 'commandarguments': '', 'buildlogfile': 'C:\\Users\\89749\\Desktop\\Homework1\\Q9\\Debug\\Q9.log', 'buildlogcontent': '生成启动时间为 2017/9/27 20:52:03。\r\n     1>项目“C:\\Users\\89749\\Desktop\\Homework1\\Q9\\Q9.vcxproj”在节点 2 上(Rebuild 个目标)。\r\n     1>ClCompile:\r\n         C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\VC\\bin\\CL.exe /c /ZI /W3 /WX- /sdl /Od /Oy- /D _MBCS /Gm /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Fo"Debug\\\\" /Fd"Debug\\vc120.pdb" /Gd /TP /analyze- /errorReport:prompt "源.cpp"\r\n         用于 x86 的 Microsoft (R) C/C++ 优化编译器 18.00.40629 版版权所有(C) Microsoft Corporation。  保留所有权利。\r\n         \r\n         cl /c /ZI /W3 /WX- /sdl /Od /Oy- /D _MBCS /Gm /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Fo"Debug\\\\" /Fd"Debug\\vc120.pdb" /Gd /TP /analyze- /errorReport:prompt "源.cpp"\r\n         \r\n         源.cpp\r\n       Link:\r\n         C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\VC\\bin\\link.exe /ERRORREPORT:PROMPT /OUT:"C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe" /INCREMENTAL kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST /MANIFESTUAC:"level=\'asInvoker\' uiAccess=\'false\'" /manifest:embed /DEBUG /PDB:"C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.pdb" /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB:"C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.lib" /MACHINE:X86 "Debug\\源.obj"\r\n         Microsoft (R) Incremental Linker Version 12.00.40629.0\r\n         Copyright (C) Microsoft Corporation.  All rights reserved.\r\n         \r\n         "/OUT:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe" /INCREMENTAL kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST "/MANIFESTUAC:level=\'asInvoker\' uiAccess=\'false\'" /manifest:embed /DEBUG "/PDB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.pdb" /TLBID:1 /DYNAMICBASE /NXCOMPAT "/IMPLIB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.lib" /MACHINE:X86 "Debug\\源.obj" \r\n         Q9.vcxproj -> C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe\r\n     1>已完成生成项目“C:\\Users\\89749\\Desktop\\Homework1\\Q9\\Q9.vcxproj”(Rebuild 个目标)的操作。\r\n\r\n生成成功。\r\n\r\n已用时间 00:00:00.92\r\n', 'compilercommand': 'cl /c /ZI /W3 /WX- /sdl /Od /Oy- /D _MBCS /Gm /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Fo"Debug\\\\" /Fd"Debug\\vc120.pdb" /Gd /TP /analyze- /errorReport:prompt "源.cpp"', 'linkcommand': '"/OUT:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe" /INCREMENTAL kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST "/MANIFESTUAC:level=\'asInvoker\' uiAccess=\'false\'" /manifest:embed /DEBUG "/PDB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.pdb" /TLBID:1 /DYNAMICBASE /NXCOMPAT "/IMPLIB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.lib" /MACHINE:X86 "Debug\\源.obj"', 'operator': '9'}
                errors = error_extraction(monitor_dict['content'])
                question_id = extract_question_id(monitor_dict['projectname'])
                if question_id == INVALID:
                    continue
                build, created = BuildResult.get_or_create(question_id=question_id, student_id=sid)
                if len(errors) == 0:
                    build.success_count = build.success_count + 1
                else:
                    build.failed_count = build.failed_count + 1
                    for e in errors:
                        build, created = BuildError.get_or_create(question_id=question_id, error_code=e['code'])
                        build.failed_count = build.failed_count + 1

        code_time_sum = 0
        for question_id, d in code_time.items():
            for day, info in d.items():
                code_time_model, created = CodeAndDebugTime.get_or_create(student_id=sid, question_id=question_id,
                                                                          date=day)
                code_time_model.code_time = info['count']
                code_time_sum += info['count']

        Speed(student_id=sid, exam_id=eid, speed=code_len/code_time_sum).create()


def extract_question_id_from_path(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shortname, extension) = os.path.splitext(tempfilename)
    question_id = extract_question_id(shortname)
    return question_id


if __name__ == '__main__':
    os.chdir('../../')

    # test monitor info extraction
    # merge_monitor_info(EID)

    # test score, test_case
    # merge_log_score(EID)

    # final step
    store_to_db(EID)
