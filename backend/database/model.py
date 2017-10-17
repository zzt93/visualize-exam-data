from peewee import *

db = MySQLDatabase('visualize_exam', user='root', charset='utf8mb4')


# todo naming: use question_id (not problem_id), student_id (user_id)
# todo support multiple exams
# todo question_id type: int

class BaseModel(Model):
    class Meta:
        database = db


class Student(BaseModel):
    student_id = CharField(unique=True)

class StudentInExam(BaseModel):
    student_id = ForeignKeyField(Student)
    exam_id = IntegerField()

# 16.每题编码时间过少的人
class StudentQuestionResult(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    used_time = FloatField()
    score = FloatField(default=0)

    class Meta:
        primary_key = CompositeKey('question_id', 'student_id')



# 1.个人整体情况图
# 5.整体编码时间分布
# 10.题目调试次数统计
# TODO there may be some problems, the model may be modified
class Operation(BaseModel):
    op_type = CharField()
    op_happen_time = TimestampField()
    op_last_time = IntegerField()
    student = ForeignKeyField(Student)


# 2.编码、调试时间总体情况统计柱状图
# 3.编码、调试时间个人情况统计柱状图
# 4.学生每题编码、调试的平均时间比例统计、分布
# 6.个人每天编码时间统计
class CodeAndDebugTime(BaseModel):
    userid = ForeignKeyField(Student)
    problemid = CharField()
    code_time = IntegerField()
    debug_time = IntegerField()
    date = DateField()

    class Meta:
        primary_key = CompositeKey('userid', 'problemid')


# 7.个人外来粘贴字符数统计柱状图
class Paste(BaseModel):
    userid = ForeignKeyField(Student)
    problemid = CharField()
    paste_content = CharField()

    class Meta:
        primary_key = CompositeKey('userid', 'problemid')


# 8.粘贴内容分类统计柱状图
# TODO 可能要换个名字是不是。。。也可能需要直接去掉上面那个Paste
class Paste2(BaseModel):
    userid = ForeignKeyField(Student)
    problemid = CharField()
    paste_content = CharField()
    count = IntegerField()

    class Meta:
        primary_key = CompositeKey('userid', 'problemid')


# 9.平均编码速度分布图
class Speed(BaseModel):
    userid = ForeignKeyField(Student)
    speed = FloatField(help_text='speed 的单位是字符/分钟')


# 11.学生整体调试次数分布统计
class Debug(BaseModel):
    userid = ForeignKeyField(Student)
    debug_count = IntegerField()


# 12.学生得分分布柱状图
class ScoreInTotal(BaseModel):
    userid = ForeignKeyField(Student)
    score = FloatField()


# 13.学生题目得分分布柱状图
class ScoreInProblem(BaseModel):
    userid = ForeignKeyField(Student)
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
    userid = ForeignKeyField(Student)
    problemid = CharField()
    failed_count = IntegerField()
    success_count = IntegerField()

    class Meta:
        primary_key = CompositeKey('userid', 'problemid')
