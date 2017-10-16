from peewee import *

db = MySQLDatabase('test', user='root', charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = db


class File(BaseModel):
    sid = ForeignKeyField(Student)
    filename = CharField()


class Student(BaseModel):
    studentId = CharField(unique=True)


class StudentQuestionResult(BaseModel):
    sid = ForeignKeyField(Student)
    qid = IntegerField()
    time_span = IntegerField()
    score = FloatField(default=0)

    class Meta:
        primary_key = CompositeKey('qid', 'sid')


# 1.个人整体情况图 TODO
# 5.整体编码时间分布
# 6.个人每天编码时间统计
# 10.题目调试次数统计
class Operation(BaseModel):
    pass

# 2.编码、调试时间总体情况统计柱状图
# 3.编码、调试时间个人情况统计柱状图
# 4.学生每题编码、调试的平均时间比例统计、分布
class CodeAndDebugTime(BaseModel):
    userid = CharField()
    problemid = CharField()
    code_time = IntegerField()
    debug_time = IntegerField()
    class Meta:
        primary_key = CompositeKey('userid', 'problemid')


# 7.个人外来粘贴字符数统计柱状图
class Paste(BaseModel):
    userid = CharField()
    problemid = CharField()
    paste_content = CharField()
    class Meta:
        primary_key = CompositeKey('userid', 'problemid')

# 8.粘贴内容分类统计柱状图
# TODO 可能要换个名字是不是。。。也可能需要直接去掉上面那个Paste
class Paste2(BaseModel):
    userid = CharField()
    problemid = CharField()
    paste_content = CharField()
    count = IntegerField()
    class Meta:
        primary_key = CompositeKey('userid', 'problemid')

# 9.平均编码速度分布图
class Speed(BaseModel):
    userid = CharField(unique=True)
    # speed 的单位是字符/分钟
    speed = FloatField()

# 11.学生整体调试次数分布统计
class Debug(BaseModel):
    userid = CharField(unique=True)
    debug_count = IntegerField()

# 12.学生得分分布柱状图
class ScoreInTotal(BaseModel):
    userid = CharField(unique=True)
    score = FloatField()

# 13.学生题目得分分布柱状图
class ScoreInProblem(BaseModel):
    userid = CharField()
    problemid = CharField()
    score = FloatField()
    class Meta:
        primary_key = CompositeKey('userid', 'problemid')

# 14.编译错误出现的次数分布
class BuildError(BaseModel):
    problemid = CharField()
    error_code = CharField()
    count = IntegerField()
    class Meta:
        primary_key = CompositeKey('problem', 'error_code')

# 15.编译失败的次数分布
class BuildFailure(BaseModel):
    userid = CharField()
    problemid = CharField()
    failed_count = IntegerField()
    success_count = IntegerField()
    class Meta:
        primary_key = CompositeKey('userid', 'problemid')

# 16.每题编码时间过少的人
class TimeTooLittle(BaseModel):
    userid = CharField()
    problemid = CharField()
    user_time = FloatField()
    class Meta:
        primary_key = CompositeKey('userid', 'problemid')

# 16.每题编码时间过少的人
class TimePerProblem(BaseModel):
    problemid = CharField(unique=True)
    mean_time = FloatField()






