

def show_paste_length_personal(paste_data: list, userid: str):
    """
    统计个人从外部粘贴的字符数分布。可以查看个人的粘贴字符情况，筛选经常进行大段粘贴的情况。
    横轴为字符数（个），纵轴为次数（个）
    :param paste_data: [{'userid': str, 'problemid':str, 'paste_content':str}], 注意需要去除非外来的粘贴字符
    :param userid:
    :return:
    """
    pass


def show_paste_content_classification(paste_class: list, userid: str):
    """
    对粘贴内容进行分类，统计不同类粘贴的次数。可以识别学生经常进行的粘贴内容。
    横轴为类别，纵轴为次数（个）
    分为整体情况统计与个人情况统计
    :param paste_class: [{'userid':str, 'problemid':str, 'paste_class':str, 'count':int}]
    :param userid: 学号，为None代表全部学生
    :return:
    """
    pass

