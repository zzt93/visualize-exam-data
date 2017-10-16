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
