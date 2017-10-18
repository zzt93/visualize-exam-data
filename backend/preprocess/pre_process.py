import os
from zipfile import ZipFile

from backend.database.model import *
from backend.util.collection_util import sort_by_time, minus_dict
from backend.util.config import *
from backend.util.constant import OperatorType, INVALID
from backend.util.error_util import error_extraction
from backend.util.log_data_transform import transform_test_log
from backend.util.monitor_data_transform import read_data
from backend.util.mysql_connector import MysqlConnector
from backend.util.scan_database import scan_dir


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


def store_to_db(eid):
    # store exam
    # Exam(eid).save()
    #
    file_to_id, student_list = file_to_sid(eid)
    #
    # # store student
    # for sid in student_list:
    #     Student(sid).save()
    #     StudentInExam(student_id=sid, eid=eid).save()
    #
    # # store score
    score, test_cases = merge_log_score(file_to_id)
    # for student_id, value in score.items():
    #     for question_id, s in value.items():
    #         StudentQuestionResult(student_id=student_id, question_id=question_id, score=score).save()
    #
    # # store test cases
    # for student_id, question_dict in test_cases:
    #     for question_id, dict_list in question_dict:
    #         for ac_dict in dict_list:
    #             TestCase(student_id, question_id, ac_dict['ac'], ac_dict['wrong']).save()
    #
    # store other monitor inof
    monitor = merge_monitor_info(eid, file_to_id)
    ordered_monitor = sort_by_time(monitor, lambda args: args[1]['time'])
    for sid, l in ordered_monitor.items():
        for m in l:
            op_type = m['operator']
            Operation(op_type, m['time'], sid).save()
            category = OperatorType.id_to_category(op_type)
            if category == 'text':
                # m: {'id': 1, 'time': datetime.datetime(2017, 9, 22, 11, 27, 36), 'operator': '4', 'name': '用例文档.md', 'path': 'E:\\大二软工二\\', 'content': '<table>', 'happentime': 636416764559624377, 'project': 'Miscellaneous Files'}
                print()
            elif category == 'content':
                # {'id': 5, 'time': datetime.datetime(2017, 9, 27, 17, 16, 44), 'operator': '5', 'fullpath': 'C:\\Users\\89749\\Desktop\\C++_Homeworks\\Q2\\Q2\\Q2\\main.cpp', 'textfrom': '', 'textto': '<>', 'line': 1, 'lineoffset': 9, 'happentime': 636421294046897697, 'project': 'Q2'}
                print()
            elif category == 'debug':
                # {'id': 1052, 'operator': '10', 'time': datetime.datetime(2017, 9, 27, 20, 52, 40), 'debug_target': 'C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe', 'debug_action': 'continue'}
                # {'id': 1053, 'operator': '11', 'time': datetime.datetime(2017, 9, 27, 20, 52, 40), 'debug_target': 'C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe', 'debug_action': 'dbgEventReasonEndProgram'}
                # {'id': 33, 'operator': '12', 'time': datetime.datetime(2017, 9, 27, 18, 35, 3), 'debug_target': 'C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q10.exe'}
                d, created = Debug.get_or_create(student_id=sid, exam_id=eid)
                d.debug_count = d.debug_count + 1
                d.save()
            elif category == 'test':
                print()
            elif category == 'build':
                # {'id_build_info': 94, 'time': datetime.datetime(2017, 9, 27, 20, 52, 6), 'buildstarttime_build_info': '2017/9/27 20:52:03', 'buildendtime_build_info': '2017/9/27 20:52:06', 'solutionname_build_info': 'Homework1', 'content': '1>------ 已启动全部重新生成:  项目: Q9, 配置: Debug Win32 ------\r\n1>  用于 x86 的 Microsoft (R) C/C++ 优化编译器 18.00.40629 版版权所有(C) Microsoft Corporation。  保留所有权利。\r\n1>  \r\n1>  cl /c /ZI /W3 /WX- /sdl /Od /Oy- /D _MBCS /Gm /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Fo"Debug\\\\" /Fd"Debug\\vc120.pdb" /Gd /TP /analyze- /errorReport:prompt "源.cpp"\r\n1>  \r\n1>  源.cpp\r\n1>  Microsoft (R) Incremental Linker Version 12.00.40629.0\r\n1>  Copyright (C) Microsoft Corporation.  All rights reserved.\r\n1>  \r\n1>  "/OUT:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe" /INCREMENTAL kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST "/MANIFESTUAC:level=\'asInvoker\' uiAccess=\'false\'" /manifest:embed /DEBUG "/PDB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.pdb" /TLBID:1 /DYNAMICBASE /NXCOMPAT "/IMPLIB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.lib" /MACHINE:X86 "Debug\\源.obj" \r\n1>  Q9.vcxproj -> C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe\r\n========== 全部重新生成:  成功 1 个，失败 0 个，跳过 0 个 ==========\r\n', 'id_build_project_info': 95, 'time_build_project_info': '2017/9/27 20:52:06', 'buildid': '2017/9/27 20:52:03', 'buildstarttime_build_project_info': '2017/9/27 20:52:03', 'buildendtime_build_project_info': '2017/9/27 20:52:04', 'solutionname_build_project_info': 'Homework1', 'projectname': 'Q9', 'configurationname': 'Debug|Win32', 'configurationtype': 'typeApplication', 'runcommand': 'C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe', 'commandarguments': '', 'buildlogfile': 'C:\\Users\\89749\\Desktop\\Homework1\\Q9\\Debug\\Q9.log', 'buildlogcontent': '生成启动时间为 2017/9/27 20:52:03。\r\n     1>项目“C:\\Users\\89749\\Desktop\\Homework1\\Q9\\Q9.vcxproj”在节点 2 上(Rebuild 个目标)。\r\n     1>ClCompile:\r\n         C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\VC\\bin\\CL.exe /c /ZI /W3 /WX- /sdl /Od /Oy- /D _MBCS /Gm /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Fo"Debug\\\\" /Fd"Debug\\vc120.pdb" /Gd /TP /analyze- /errorReport:prompt "源.cpp"\r\n         用于 x86 的 Microsoft (R) C/C++ 优化编译器 18.00.40629 版版权所有(C) Microsoft Corporation。  保留所有权利。\r\n         \r\n         cl /c /ZI /W3 /WX- /sdl /Od /Oy- /D _MBCS /Gm /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Fo"Debug\\\\" /Fd"Debug\\vc120.pdb" /Gd /TP /analyze- /errorReport:prompt "源.cpp"\r\n         \r\n         源.cpp\r\n       Link:\r\n         C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\VC\\bin\\link.exe /ERRORREPORT:PROMPT /OUT:"C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe" /INCREMENTAL kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST /MANIFESTUAC:"level=\'asInvoker\' uiAccess=\'false\'" /manifest:embed /DEBUG /PDB:"C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.pdb" /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB:"C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.lib" /MACHINE:X86 "Debug\\源.obj"\r\n         Microsoft (R) Incremental Linker Version 12.00.40629.0\r\n         Copyright (C) Microsoft Corporation.  All rights reserved.\r\n         \r\n         "/OUT:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe" /INCREMENTAL kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST "/MANIFESTUAC:level=\'asInvoker\' uiAccess=\'false\'" /manifest:embed /DEBUG "/PDB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.pdb" /TLBID:1 /DYNAMICBASE /NXCOMPAT "/IMPLIB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.lib" /MACHINE:X86 "Debug\\源.obj" \r\n         Q9.vcxproj -> C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe\r\n     1>已完成生成项目“C:\\Users\\89749\\Desktop\\Homework1\\Q9\\Q9.vcxproj”(Rebuild 个目标)的操作。\r\n\r\n生成成功。\r\n\r\n已用时间 00:00:00.92\r\n', 'compilercommand': 'cl /c /ZI /W3 /WX- /sdl /Od /Oy- /D _MBCS /Gm /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Fo"Debug\\\\" /Fd"Debug\\vc120.pdb" /Gd /TP /analyze- /errorReport:prompt "源.cpp"', 'linkcommand': '"/OUT:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.exe" /INCREMENTAL kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST "/MANIFESTUAC:level=\'asInvoker\' uiAccess=\'false\'" /manifest:embed /DEBUG "/PDB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.pdb" /TLBID:1 /DYNAMICBASE /NXCOMPAT "/IMPLIB:C:\\Users\\89749\\Desktop\\Homework1\\Debug\\Q9.lib" /MACHINE:X86 "Debug\\源.obj"', 'operator': '9'}
                errors = error_extraction(m['content'])
                question_id = extract_question_id(m['projectname'])
                if question_id == INVALID:
                    continue
                if len(errors) == 0:
                    build, created = BuildResult.get_or_create(question_id=question_id, error_code=e['code'])
                    build.success_count = build.success_count + 1
                for e in errors:
                    build, created = BuildResult.get_or_create(question_id=question_id, error_code=e['code'])
                    build.failed_count = build.failed_count + 1


if __name__ == '__main__':
    os.chdir('../../')
    # merge_monitor_info(EID)
    # store_to_db(EID)
    merge_log_score(EID)
