import MySQLdb


class MysqlConnector:
    # TODO charset

    def __init__(self) -> None:
        self.db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                             user="root",  # your username
                             passwd="root",  # your password
                             db="cpp_test_server")  # name of the data base

    def get_student_file(self, student_id, eid):
        cur = self.db.cursor()
        cur.execute(
            "SELECT ep.log, ep.monitor FROM auth_user a JOIN exams_examprojects ep, exams_exam e WHERE e.id = {} AND a.id = ep.user_id AND a.username = '{}' AND ep.create_time > e.begin_time".format(
               eid, student_id))
        res = {}
        for row in cur.fetchall():
            res[row[0]] = student_id
            res[row[1]] = student_id
        cur.close()
        return res

    def get_student_monitor_file(self, student_id, eid):
        cur = self.db.cursor()
        cur.execute(
            "SELECT ep.monitor FROM auth_user a JOIN exams_examprojects ep, exams_exam e WHERE e.id = {} AND a.id = ep.user_id AND a.username = '{}' AND ep.create_time > e.begin_time ".format(
                eid, student_id))
        res = []
        for row in cur.fetchall():
            res.append(row[0])
        cur.close()
        return res

    def close(self):
        self.db.close()

    def get_all_student(self, eid):
        cur = self.db.cursor()
        cur.execute("select distinct(a.username) from exams_examprojects e join auth_user a where a.id = e.user_id and exam_id = {}".format(eid))
        res = []
        for row in cur.fetchall():
            res.append(row[0])
        cur.close()
        return res

    def get_question_set(self, eid):
        cur = self.db.cursor()
        cur.execute("select question_id from exams_examquestion where exam_id = {}".format(eid))
        res = set([row[0] for row in cur.fetchall()])
        cur.close()
        return res
