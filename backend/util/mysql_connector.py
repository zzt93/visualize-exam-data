import MySQLdb


class MysqlConnector:
    # TODO charset
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="",  # your password
                         db="cpp_test_server")  # name of the data base
    cur = db.cursor()

    def get_student_file(self, student_id, from_date, to_date):
        self.cur.execute(
            "SELECT e.log, e.monitor FROM auth_user a JOIN exams_examprojects e WHERE a.id = e.user_id AND a.username = '{}' AND e.create_time > '{}' AND e.create_time < '{}'".format(
                student_id, from_date, to_date))
        res = {}
        for row in self.cur.fetchall():
            res[row[0]] = student_id
            res[row[1]] = student_id
        return res

    def close(self):
        self.db.close()

    def get_all_student(self, eid):
        self.cur.execute("select distinct(a.username) from exams_examprojects e join auth_user a where a.id = e.user_id and exam_id = {}".format(eid))
        res = []
        for row in self.cur.fetchall():
            res.append(row[0])
        return res

    def get_question_set(self, eid):
        self.cur.execute("select question_id from exams_examquestion where exam_id = {}".format(eid))
        return set([row[0] for row in self.cur.fetchall()])
