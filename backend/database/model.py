from peewee import *
import random
import time
import datetime
import string

db = MySQLDatabase('visualize_exam', user='root', charset='utf8mb4')

def before_request_handler():
    db.connect()



def after_request_handler():
    db.close()


class BaseModel(Model):
    class Meta:
        database = db


class Student(BaseModel):
    student_id = CharField(primary_key=True, unique=True)


class Exam(BaseModel):
    exam_id = IntegerField(unique=True, primary_key=True)

class StudentInExam(BaseModel):
    student_id = ForeignKeyField(Student)
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'exam_id')

class QuestionInExam(BaseModel):
    exam_id = ForeignKeyField(Exam)
    question_id = IntegerField(unique=True, primary_key=True)

# 13.学生题目得分分布柱状图
# 16.每题编码时间过少的人
class StudentQuestionResult(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    used_time = IntegerField()
    score = FloatField(default=0)
    class Meta:
        primary_key = CompositeKey('question_id', 'student_id')



# 1.个人整体情况图
# 5.整体编码时间分布
# 10.题目调试次数统计
class Operation(BaseModel):
    op_type = IntegerField()
    op_happen_time = TimestampField()
    op_last_time = IntegerField(default=0)
    student_id = ForeignKeyField(Student)
    class Meta:
        primary_key = CompositeKey('op_happen_time', 'student_id')

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
    class Meta:
        primary_key = CompositeKey('student_id', 'question_id')


# 7.个人外来粘贴字符数统计柱状图
# 8.粘贴内容分类统计柱状图
class Paste(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    paste_content = CharField()
    paste_type = IntegerField()
    happen_time = DateTimeField()
    class Meta:
        primary_key = CompositeKey('student_id', 'question_id', 'paste_type')


# 9.平均编码速度分布图
class Speed(BaseModel):
    student_id = ForeignKeyField(Student)
    speed = FloatField(help_text='speed 的单位是字符/分钟')
    exam_id = ForeignKeyField(Exam)
    class Meta:
        primary_key = CompositeKey('student_id', 'exam_id')

# 11.学生整体调试次数分布统计
class Debug(BaseModel):
    student_id = ForeignKeyField(Student, primary_key=True)
    debug_count = IntegerField(default=1)



# 14.编译错误出现的次数分布
class BuildError(BaseModel):
    question_id = ForeignKeyField(QuestionInExam)
    error_code = CharField()
    count = IntegerField()
    class Meta:
        primary_key = CompositeKey('question_id', 'error_code')


# 15.编译失败的次数分布
class BuildFailure(BaseModel):
    student_id = ForeignKeyField(Student)
    question_id = IntegerField()
    failed_count = IntegerField()
    success_count = IntegerField()
    class Meta:
        primary_key = CompositeKey('student_id', 'question_id')

def insert_test():
    # #######Student
    # for sid in range(1, 300):
    #     Student.create(student_id = str(sid))
    #
    # #######Exam
    # for eid in range(1, 5):
    #     Exam.create(exam_id = eid)
    #
    # #######StudentInExam
    # for eid in range(1, 3):
    #     for sid in range(1, 200):
    #         StudentInExam.create(student_id=sid, exam_id = eid)
    #
    # ########QuestionInExam
    # eid = 1
    # for qid in range(1, 16):
    #     QuestionInExam.create(question_id = qid, exam_id = eid)
    # eid = 2
    # for qid in range(16, 27):
    #     QuestionInExam.create(question_id = qid, exam_id = eid)

    #######StudentQuestionResult
    # for qid in range(1, 16):
    #     for sid in range(1, 220):
    #         ut = random.randint(0, 300)
    #         sc = random.random() * 100
    #         StudentQuestionResult.create(student_id = sid, question_id = qid, used_time = ut, score = sc)

    # #######Operation
    # for t in range(1, 5):
    #     for sid in range(1, 200):
    #         ot = random.randint(1, 8)
    #         oht = time.time()
    #         olt = random.randint(10, 200)
    #         Operation.create(op_type = ot, op_happen_time = oht, op_last_time = olt, student_id=str(sid))
    #######CodeAndDebugTime
    # for sid in range(1, 100):
    #     for qid in range(1, 15):
    #         ct = random.randint(50, 500)
    #         dt = random.randint(0, 200)
    #         d = datetime.datetime.now().strftime('%Y-%m-%d')
    #         CodeAndDebugTime.create(student_id = sid, question_id = qid, code_time = ct, debug_time = dt, date = d)

    ######Paste
    # for pt in range(1, 5):
    #     for sid in range(1, 50):
    #         for qid in range(1, 11):
    #             len = random.randint(1, 20)
    #             salt = ''.join(random.sample(string.ascii_letters + string.digits, len))
    #             ht = datetime.datetime.now()
    #             Paste.create(student_id = str(sid), question_id = qid, paste_content = salt, paste_type = pt, happen_time = ht)
    #######Speed
    # for sid in range(1, 100):
    #     for eid in range(1, 3):
    #         s = random.random() * 100
    #         Speed.create(student_id = sid, speed = s, exam_id = eid)

    #######Debug
    # for sid in range(1, 200):
    #     dc = random.randint(0, 100)
    #     Debug.create(student_id = sid, debug_count = dc)

    ######BuildError
    for qid in range(1, 15):
        for ec in range(1, 6):
            c = random.randint(0, 100)
            BuildError.create(question_id = qid, error_code = ec, count = c)

    #######BuildFailure
    # for sid in range(1, 100):
    #     for qid in range(1, 18):
    #         fc = random.randint(0, 30)
    #         sc = random.randint(0, 60)
    #         BuildFailure.create(student_id = sid, question_id = qid, failed_count = fc, success_count = sc)
    pass


#
#
# # 15.编译失败的次数分布
# class BuildFailure(BaseModel):
#     student_id = ForeignKeyField(Student)
#     question_id = IntegerField()
#     failed_count = IntegerField()
#     success_count = IntegerField()
#     class Meta:
#         primary_key = CompositeKey('student_id', 'question_id')

def create_tables():
    db.connect()
    db.create_tables([Student, Exam, StudentInExam, QuestionInExam, StudentQuestionResult, Operation, CodeAndDebugTime,
                      Paste, Speed, Debug, BuildError, BuildFailure])


# create_tables()
db.create_table(BuildError)
insert_test()