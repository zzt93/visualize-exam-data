BUILD_INFO = 'build_info'
SQLITE_SEQUENCE = 'sqlite_sequence'
BUILD_PROJECT_INFO = 'build_project_info'
COMMAND_TEXT = 'command_text'
COMMAND_FILE = 'command_file'
CONTENT_INFO = 'content_info'
DEBUG_INFO = 'debug_info'
DEBUG_BREAK = 'debug_break'
BREAK_POINT = 'breakpoint'
DEBUG_RUN = 'debug_run'
EXCEPTION = 'exception'
DEBUG_EXCEPTION_THROWN = 'debug_exception_thrown'
DEBUG_EXCEPTION_NOT_HANDLES = 'debug_exception_not_handled'
LOCAL_VARIABLE = 'local_variable'
BREAKPOINT_EVENT = 'breakpoint_event'
SOLUTION_OPEN_EVENT = 'solution_open_eventfile_event'
ITEMTABLE = 'ItemTable'


class OperatorType:
    NAME = 'operator'
    TEXT_SAVE = '1'
    TEXT_CUT = '2'
    TEXT_PASTE = '3'
    TEXT_COPY = '4'
    CONTENT_INSERT = '5'
    CONTENT_REPLACE = '6'
    CONTENT_DELETE = '7'
    CONTENT_SAVE = '8'
    BUILD = '9'
    DEBUG_TUN = '10'
    DEBUG_BREAK = '11'
    DEBUG_EXCEPTION_NOT_HANDLED = '12'
    BROWSER_URL = '13'
    BROWSER_URL_CLOSE = '14'
    BROWSER_COPY = '15'
    BROWSER_PASTE = '16'
    BROWSER_CUT = '17'
    TEST = '18'
    TEXT_STARTUNDO = '19'
    TEXT_UNDOEND = '20'
    TEXT_STARTREDO = '21'
    TEXT_REDOEND = '22'

    @staticmethod
    def id_to_name(id):
        res = {
            '1': 'text_save',
            '2': 'text_cut',
            '3': 'text_paste',
            '4': 'text_copy',
            '5': 'content_insert',
            '6': 'content_replace',
            '7': 'content_delete',
            '8': 'content_save',
            '9': 'build',
            '10': 'debug_run',
            '11': 'debug_break',
            '12': 'debug_exception_not_handled',
            '13': 'browser_url',
            '14': 'browser_url_close',
            '15': 'browser_copy',
            '16': 'browser_paste',
            '17': 'browser_cut',
            '18': 'test',
            '19': 'text_StartUndo',
            '20': 'text_UndoEnd',
            '21': 'text_StartRedo',
            '22': 'text_RedoEnd'
        }
        return res[id]

    @staticmethod
    def id_to_category(id):
        id = int(id)
        if 1 <= id <= 4:
            return 'text'
        elif 5 <= id <= 8:
            return 'content'
        elif id == 9:
            return 'build'
        elif 10 <= id <= 12:
            return 'debug'
        elif 13 <= id <= 17:
            return 'browser'
        elif id == 18:
            return 'test'
        elif 19 <= id <= 22:
            return 'text'
