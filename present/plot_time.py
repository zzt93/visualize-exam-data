

def show_process_personal(data: list, userid: str, dayid: int):
    """
    统计每人每天的插入、删除字符，编译调试情况。可以得到单个学生某天编码的整体情况。
    横轴是时间00:00-23:59，纵轴是插入字符数（个数），删除字符数（个数），编译点，调试点
    :param data: 包含去重之后的 某人 某天 的全部操作记录
    :param userid: 学号
    :param dayid: 天数id
    :return: fig对象
    """
    pass


def show_time_total(user_data: list):
    """
    统计不同编码、调试时间的人数。可以得到整体与每题的编码时间人数分布。
    横轴为时间段（min），纵轴为人数（个）
    分为总体情况与每题目情况
    :param user_data: [{'userid':str, 'problemid':str, 'code_time':int, 'debug_time':int}]
    :return:
    """
    pass


def show_time_personal(user_data: list, userid: str):
    """
    统计个人每道题的编码，调试时间。可以得到每个人的每题编码时间。
    横轴为题目编号，纵轴为所花时间（min）
    :param user_data: [{'userid':str, 'problemid':str, 'code_time':int, 'debug_time':int}]
    :param userid: 学号
    :return:
    """
    pass


def show_time_div_total(user_data: list):
    """
    统计每题学生编码的平均时间的比例。可以发现不同题目的编码调试难度
    横轴为题目，纵轴为学生在该题的编码、调试比例。
    :param user_data: [{'userid':str, 'problemid':str, 'code_time':int, 'debug_time':int}]
    :return:
    """
    pass


def show_work_time(all_data: list):
    """
    统计24h内，每个时间段正在编写作业的用户人数。可以得到学生主要进行编码、完成作业的时间段。
    横轴为时间00:00-23:59，纵轴为人数（个）
    :param all_data: [{'userid':str, 'data':list}], data包含去重之后的某用户的全部操作记录
    :return:
    """
    pass


def show_work_time_personal(data: list, userid: str):
    """
    统计个人在作业期间每天的编码时间。可以得到用户每天编码所花时间的情况。
    横轴为天数，纵轴为时间（min）
    :param data: 包含去重之后的 某人 的全部操作记录
    :param userid: 学号
    :return:
    """
    pass
