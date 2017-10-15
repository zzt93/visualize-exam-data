def string_to_datetime(s):
    import datetime
    return datetime.datetime.strptime(s, '%Y/%m/%d %H:%M:%S')


def timedelta_milliseconds(td):
    return td.days*86400000 + td.seconds*1000 + td.microseconds/1000
