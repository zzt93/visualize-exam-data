import datetime
import json
import re

from backend.util.constant import OperatorType


def transform_test_log(f):
    op_dict_list = []

    line_list = f.readlines()
    pattern = re.compile('(.*)\[(.*)\]')
    for line in line_list:
        line = line.decode('utf-8')
        ops = [t.strip() for t in line.strip().split('::')]
        if len(ops) < 3 or ops[2] != 'test':
            continue
        res = dict()
        res['time'] = datetime.datetime.strptime(ops[0][:-1], '%Y-%m-%d %H:%M:%S')
        for k, v in zip(ops[1::2], ops[2::2]):
            if k == 'message':
                json_obj = json.loads(v)
                v = {a: [pattern.match(t).group(1) for t in b] for a, b in json_obj.items()}
                for tk in ['AC', 'TIE', 'WA']:
                    if tk not in v:
                        v[tk] = []
            res[k] = v
        res[OperatorType.NAME] = OperatorType.TEST
        op_dict_list.append(res)
    return op_dict_list