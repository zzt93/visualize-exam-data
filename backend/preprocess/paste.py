import re

PASTE_TYPE_OTHER = 0
PASTE_TYPE_LONG = 1
PASTE_TYPE_IF = 2
PASTE_TYPE_LOOP = 3
PASTE_TYPE_FUNC = 4
PASTE_TYPE_TOKEN = 5

token_pattern = re.compile(r"[\w_]+")
func_pattern = re.compile(r"[\w_]+\([\w,_]*\)")
if_pattern = re.compile(r"if\s*\(([^()]|\s)*\)\s*\{(.|\s)*?\}")
loop_pattern = re.compile(r"(while|for)\s*\(([^()]|\s)*\)\s*\{(.|\s)*?\}")


def get_paste_type(content):
    if len(content) > 200:
        return PASTE_TYPE_LONG
    if 'if' in content:
        return PASTE_TYPE_IF
    if 'while' in content or 'for' in content:
        return PASTE_TYPE_LOOP
    if func_pattern.search(content):
        return PASTE_TYPE_FUNC
    # if token_pattern.search(content):
    return PASTE_TYPE_TOKEN
    # return PASTE_TYPE_OTHER
