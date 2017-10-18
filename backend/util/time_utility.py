import locale


def string_to_datetime(s):
    import datetime
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.datetime.strptime(s, '%Y/%m/%d %H:%M:%S')
        except ValueError:
            # 2017/9/27 星期三 19:50:25
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
            try:
                return datetime.datetime.strptime(s, '%Y/%m/%d %A %H:%M:%S')
            except ValueError:
                # 2017/9/27/周三 22:34:49
                locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
                return datetime.datetime.strptime(s, '%Y/%m/%d/%a %H:%M:%S')

def timedelta_milliseconds(td):
    return td.days * 86400000 + td.seconds * 1000 + td.microseconds / 1000
