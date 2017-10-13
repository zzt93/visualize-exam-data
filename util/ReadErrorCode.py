import sqlite3
import re


def clearErrorDB():
    con2=sqlite3.connect(r"C:\Users\Lf\Desktop\test.db")
    con2.execute("DELETE FROM error")
    con2.commit()
    con2.execute("update sqlite_sequence SET seq = 0 where name ='error';")
    con2.commit()
    con2.close()


def checkErrorDB():
    con2=sqlite3.connect(r"C:\Users\Lf\Desktop\test.db")
    con2.execute("CREATE TABLE IF NOT EXISTS error (id INTEGER PRIMARY KEY autoincrement, buildprojid INTEGER, buildid TEXT, projectname TEXT, errorcontent TEXT, errorposition TEXT, errorcode TEXT, errormessage TEXT) ")
    con2.commit()
    con2.close()


def saveError(err):
    con2=sqlite3.connect(r"C:\Users\Lf\Desktop\test.db")
    con2.execute(r"INSERT INTO error (buildprojid, buildid, projectname, errorcontent, errorposition, errorcode, errormessage) VALUES (?, ?, ?, ?, ?, ?, ?)", [err[0], err[1], err[4], err[6], err[7], err[8], err[9]])
    con2.commit()
    con2.close()


def dealError(pro):
    content=pro[5]
    lines=content.split("\n")
    for temp in lines:
        temp=temp.strip()
        temps=temp.split(">")
        if len(temps)>1:
            line=temp[2:]
        else:
            line=temp
        pattern=re.compile(r"^(.*): (fatal |)error (\w*): (.*)$")
        match=pattern.search(line)
        if match:
            position=match.group(1)
            code=match.group(3)
            message=match.group(4)
            err=pro+(line, position, code, message)
            saveError(err)
            print(code+"\t"+message)


def readBuildInf():
    con1=sqlite3.connect(r"C:\Users\Lf\Desktop\test\sh\CppMonitor\Dao\log.db")
    pros=con1.execute(r"SELECT time, buildid, buildstarttime, buildendtime, projectname, buildlogcontent FROM build_project_info")
    for pro in pros:
        dealError(pro)
    con1.close()


if __name__ == '__main__':
    print("")
    print("Code\tMessage")
    clearErrorDB()
    checkErrorDB()
    readBuildInf()
