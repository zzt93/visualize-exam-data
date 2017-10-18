from peewee import *

db = MySQLDatabase('visualize_exam', user='root', charset='utf8mb4')



class BaseModel(Model):
    class Meta:
        database = db


class Student(BaseModel):
    student_id = CharField(unique=True)

class Exam(BaseModel):
    exam_id = IntegerField(unique=True)

class StudentInExam(BaseModel):
    student_id = ForeignKeyField(Student)
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'exam_id')

# 13.学生题目得分分布柱状图
# 16.每题编码时间过少的人
class StudentQuestionResult(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    used_time = IntegerField()
    score = FloatField(default=0)
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('question_id', 'student_id', 'exam_id')



# 1.个人整体情况图
# 5.整体编码时间分布
# 10.题目调试次数统计
class Operation(BaseModel):
    op_type = IntegerField()
    op_happen_time = TimestampField()
    op_last_time = IntegerField()
    student_id = ForeignKeyField(Student)
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('op_happen_time', 'student_id', 'exam_id')

# 2.编码、调试时间总体情况统计柱状图
# 3.编码、调试时间个人情况统计柱状图
# 4.学生每题编码、调试的平均时间比例统计、分布
# 6.个人每天编码时间统计
class CodeAndDebugTime(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    code_time = IntegerField()
    debug_time = IntegerField()
    date = DateField()
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'question_id', 'exam_id')


# 7.个人外来粘贴字符数统计柱状图
class Paste(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    paste_content = CharField()
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'question_id', 'exam_id')


# 8.粘贴内容分类统计柱状图
# TODO 可能要换个名字是不是。。。也可能需要直接去掉上面那个Paste
class Paste2(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    paste_content = CharField()
    count = IntegerField()
    paste_type = IntegerField()
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'question_id', 'exam_id')


# 9.平均编码速度分布图
class Speed(BaseModel):
    student_id = ForeignKeyField(Student)
    speed = FloatField(help_text='speed 的单位是字符/分钟')
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'exam_id')

# 11.学生整体调试次数分布统计
class Debug(BaseModel):
    student_id = ForeignKeyField(Student)
    debug_count = IntegerField(default=1)
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'exam_id')


# 14.编译错误出现的次数分布
class BuildError(BaseModel):
    question_id = IntegerField()
    error_code = CharField()
    count = IntegerField()
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('question_id', 'error_code', 'exam_id')


# 15.编译失败的次数分布
class BuildFailure(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    failed_count = IntegerField()
    success_count = IntegerField()
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'question_id', 'exam_id')
