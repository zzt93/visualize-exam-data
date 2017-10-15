import MySQLdb


class MysqlConnector:
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="cpp_test",  # your username
                         passwd="cpp_test",  # your password
                         db="cpp_test_server")  # name of the data base
    cur = db.cursor()

    def get_student_file(self, student_id, from_date, to_date):
        self.cur.execute(
            "select e.log, e.monitor from auth_user a JOIN exams_examprojects e where a.user_id = e.user_id and username = '%ld' and e.create_time > '%s' and e.create_time < '%s'" % (student_id, from_date, to_date))

        for row in self.cur.fetchall():
            print(row[0])

    def close(self):
        self.db.close()




