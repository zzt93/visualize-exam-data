from peewee import *
# 解决了log.db的模型
database = SqliteDatabase('log.db', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Breakpoint(BaseModel):
    condition = TextField(null=True)
    condition_type = TextField(null=True)
    current_hits = IntegerField(null=True)
    enabled = TextField()
    file = TextField()
    file_column = IntegerField()
    file_line = IntegerField()
    function_name = TextField(null=True)
    location_type = TextField()
    tag = TextField(null=True)

    class Meta:
        db_table = 'breakpoint'

class BreakpointEvent(BaseModel):
    breakpoint = IntegerField(db_column='breakpoint_id', null=True)
    modification = TextField()

    class Meta:
        db_table = 'breakpoint_event'

class BuildInfo(BaseModel):
    buildendtime = TextField(null=True)
    buildstarttime = TextField(null=True)
    content = TextField(null=True)
    solutionname = TextField(null=True)
    time = UnknownField(null=True)  # char[22]

    class Meta:
        db_table = 'build_info'

class BuildProjectInfo(BaseModel):
    buildendtime = TextField(null=True)
    buildid = TextField(null=True)
    buildlogcontent = TextField(null=True)
    buildlogfile = TextField(null=True)
    buildstarttime = TextField(null=True)
    commandarguments = TextField(null=True)
    compilercommand = TextField(null=True)
    configurationname = TextField(null=True)
    configurationtype = TextField(null=True)
    linkcommand = TextField(null=True)
    projectname = TextField(null=True)
    runcommand = TextField(null=True)
    solutionname = TextField(null=True)
    time = UnknownField(null=True)  # char[22]

    class Meta:
        db_table = 'build_project_info'

class CommandFile(BaseModel):
    action = UnknownField(null=True)  # char[5]
    filepath = TextField(null=True)
    pastefilepath = TextField(null=True)
    pasteto = TextField(null=True)
    project = TextField(null=True)
    time = UnknownField(null=True)  # char[22]

    class Meta:
        db_table = 'command_file'

class CommandText(BaseModel):
    action = UnknownField(null=True)  # char[10]
    content = TextField(null=True)
    happentime = UnknownField(null=True)  # int8
    name = TextField(null=True)
    path = TextField(null=True)
    project = TextField(null=True)
    time = UnknownField(null=True)  # char[22]

    class Meta:
        db_table = 'command_text'

class ContentInfo(BaseModel):
    fullpath = TextField(null=True)
    happentime = UnknownField(null=True)  # int8
    line = IntegerField(null=True)
    lineoffset = IntegerField(null=True)
    operation = UnknownField(null=True)  # char[7]
    project = TextField(null=True)
    textfrom = BlobField(null=True)
    textto = BlobField(null=True)
    time = UnknownField(null=True)  # char[22]

    class Meta:
        db_table = 'content_info'

class DebugBreak(BaseModel):
    break_reason = TextField()
    breakpoint_last_hit = IntegerField(null=True)

    class Meta:
        db_table = 'debug_break'

class DebugExceptionNotHandled(BaseModel):
    exception = IntegerField(db_column='exception_id')

    class Meta:
        db_table = 'debug_exception_not_handled'

class DebugExceptionThrown(BaseModel):
    exception = IntegerField(db_column='exception_id')

    class Meta:
        db_table = 'debug_exception_thrown'

class DebugInfo(BaseModel):
    config_name = TextField(null=True)
    debug_target = TextField(null=True)
    timestamp = DateTimeField()
    type = TextField()

    class Meta:
        db_table = 'debug_info'

class DebugRun(BaseModel):
    breakpoint_last_hit = IntegerField(null=True)
    run_type = TextField()

    class Meta:
        db_table = 'debug_run'

class Exception(BaseModel):
    action = TextField()
    code = IntegerField(null=True)
    description = TextField(null=True)
    name = TextField(null=True)
    type = TextField(null=True)

    class Meta:
        db_table = 'exception'

class FileEvent(BaseModel):
    filename = TextField(null=True)
    projectname = TextField(null=True)
    targetfile = TextField(db_column='targetFile', null=True)
    time = UnknownField(null=True)  # char[22]
    type = UnknownField(null=True)  # tinyint

    class Meta:
        db_table = 'file_event'

class LocalVariable(BaseModel):
    debug = IntegerField(db_column='debug_id')
    name = TextField()
    value = TextField()

    class Meta:
        db_table = 'local_variable'

class SolutionOpenEvent(BaseModel):
    info = TextField(null=True)
    solutionname = TextField(null=True)
    targetfolder = TextField(null=True)
    time = UnknownField(null=True)  # char[22]
    type = UnknownField(null=True)  # tinyint

    class Meta:
        db_table = 'solution_open_event'

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        db_table = 'sqlite_sequence'
        primary_key = False

