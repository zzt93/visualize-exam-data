

def show_debug_personal(data: list, userid: str, problemid: str):
    """
    统计每个人在不同题目的调试次数。可以发现不同题目的调试次数，评估不同题目的难度。
    横轴为题目，纵轴为调试次数（个）
    :param data: data包含去重之后的 某人 的全部操作记录
    :param userid: 学号
    :param problemid: 题号
    :return:
    """
    pass


def show_debug_total(debug_count_data: list):
    """
    统计学生整体上调试次数的分布，可以发现学生整体是否善用了调试工具。
    横轴为调试次数段（个），纵轴为学生人数（个）
    :param debug_count_data: [{'userid':str, 'debug_count':int}]
    :return:
    """
    pass

