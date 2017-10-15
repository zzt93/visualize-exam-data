import util.monitor_data_transform as mon_transform
from util.log_data_transform import transform_test_log

def combine_database(con_mon=None, con_bro=None, test_log=None):
    '''
    :param con_mon: a db connect object of codding
    :param con_bro: a db connect object of browser
    :param test_log_handler: a dir path
    :return: a list object
    '''

    from util.scan_database import scan_dir
    import os

    res = []
    if con_mon:
        res.extend(mon_transform.combine_database(con_mon))
    for file in scan_dir(test_log):
        test_log_handler = None
        if os.path.isfile(file):
            (filepath, tempfilename) = os.path.split(file)
            (shotname, extension) = os.path.splitext(tempfilename)
            if shotname == 'app':
                test_log_handler = open(file)
        if test_log_handler:
            res.extend(transform_test_log(test_log_handler))

    res = sorted(res, key=lambda x: x['time'])
    return res