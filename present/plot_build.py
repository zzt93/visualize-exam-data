

def show_build_error_count(build_error_data: list, problemid: str, top: int=10):
    """
    统计所有编译错误的次数的分布。可以比较不同编译错误出现的频率。
    横轴为具体编译错误，纵轴为个数
    :param build_error_data: [{'problemid':str, 'error_code':str, 'count':int}]
    :param problemid: 题号
    :param top: 前N个
    :return:
    """
    pass


def show_build_failed_count(build_data: list):
    """
    统计所有编译失败次数的分布。可以比较编译失败。
    横轴为编译失败次数，纵轴为人数
    :param build_data: [{'problemid':str, 'userid':str, 'failed_count':int, 'success_count':int}]
    :return:
    """
    pass

