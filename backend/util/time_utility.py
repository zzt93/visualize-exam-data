import locale
import datetime


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
                ss = s.split(' ')
                new_date = ss[0][:-3] + ' ' + ss[1]
                try:
                    return datetime.datetime.strptime(new_date, '%Y/%m/%d/%a %H:%M:%S')
                except ValueError:
                    # 2017/10/2 星期一 下午 20:04:08
                    ss = s.split(' ')
                    new_date = ss[0] + ' ' + ss[3]
                    return datetime.datetime.strptime(new_date, '%Y/%m/%d %H:%M:%S')


def timedelta_milliseconds(td):
    return td.days * 86400000 + td.seconds * 1000 + td.microseconds / 1000


def timestamp_datetime(ts):
    if isinstance(ts, (int, float, str)):
        try:
            ts = int(ts)
        except ValueError:
            raise

        if len(str(ts)) == 13:
            ts = int(ts / 1000)
        if len(str(ts)) != 10:
            raise ValueError
    else:
        raise ValueError()
    return datetime.fromtimestamp(ts)
