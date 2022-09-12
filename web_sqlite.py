import sqlite3


class My_sqlite:
    def __init__(self, sqlName):
        self.sqlName = sqlName

    def __enter__(self):
        self.conn = sqlite3.connect(self.sqlName)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_avl, exc_tb):
        self.cursor.close()
        self.conn.close()

    def register(self, user: str, paw: str) -> bool:
        """
        注册信息(学号,密码) 成功返回Ture
        """
        sql = f"insert into web_db(No,pad) values('{user}','{paw}');"
        try:
            self.cursor.execute(sql)
        except:
            return False
        self.conn.commit()
        return True

    def login(self, user: str) -> bool:
        """
        判断某个学号是否可以登录(web表)
        """
        sql = f"select count(*) from web_db where No='{user}' limit 1"
        if self.cursor.execute(sql).fetchall()[0][0] == 1:
            return True
        else:
            return False

    def selPassword(self, user: str, paw: str) -> bool:
        """
        查询输入的密码与数据库的密码是否一致。相同返回Ture
        """
        sql = f"SELECT pad FROM web_db WHERE No='{user}'"
        if self.cursor.execute(sql).fetchall()[0][0] == paw:
            return True
        else:
            return False

    def getStudentInfo(self) -> list:
        """
        返回数据库里的学生信息
        """
        sql = "SELECT id,name,sex,age,address FROM student_info ORDER BY id asc"
        date = self.cursor.execute(sql).fetchall()
        return date

    def chanGePassword(self, user: str, pad: str) -> bool:
        """
        修改登录密码
        """
        sql = f"update web_db set pad = '{pad}' where No= '{user}'"
        try:
            self.cursor.execute(sql)
        except:
            return False
        self.conn.commit()
        return True

    def intoStudentInfo(self, user: str, name: str, sex: str, age: str, address: str) -> bool:
        """
        往数据库中写入学生信息
        """
        sql = f"INSERT INTO student_info (id,name,sex,age,address) VALUES('{user}','{name}','{sex}','{age}','{address}')"
        try:
            self.cursor.execute(sql)
        except:
            return False
        self.conn.commit()
        return True

    def stuinMysql(self, user: str) -> bool:
        """
        判断某个学号是否存在于数据库中(student_info表) 存在return Ture
        """
        sql = f"select count(*) from student_info where id='{user}' limit 1"
        if self.cursor.execute(sql).fetchall()[0][0] == 1:
            return True
        else:
            return False

    def delStudent(self, user: str) -> bool:
        """
        删除学生信息
        """
        if self.stuinMysql(user):
            sql = f"DELETE FROM student_info WHERE id='{user}'"
            try:
                self.cursor.execute(sql)
            except:
                return False
            self.conn.commit()
            return True
        else:
            return False

    def upDataStudent(self, user: str, name: str, sex: str, age: str, address: str) -> None:
        """
        更新学生信息
        """
        sql = f"UPDATE student_info set name='{name}',sex='{sex}',age='{age}',address='{address}' WHERE id='{user}'"
        self.cursor.execute(sql)
        self.conn.commit()

    def getOneStudent(self, user: str) -> list:
        """
        获取某个学生信息
        """
        sql = f"SELECT * FROM student_info WHERE id='{user}'"
        return self.cursor.execute(sql).fetchall()

    def studnetScrore(self) -> list:
        """
        返回全部学生成绩
        """
        sql = "SELECT * FROM grade where id='0001'"
        return self.cursor.execute(sql).fetchall()


# with My_sqlite("student.db") as name:name.getStudentInfo()

def register(database: My_sqlite, user: str, paw: str) -> bool:
    """
    注册信息(学号,密码) 成功返回Ture
    """
    with database:
        return database.register(user, paw)


def loGin(database: My_sqlite, user: str) -> bool:
    """
    判断某个学号是否可以登录(web表)
    """
    with database:
        return database.login(user)


def selPassword(database: My_sqlite, user: str, paw: str) -> bool:
    """
    查询输入的密码与数据库的密码是否一致。相同返回Ture
    """
    with database:
        return database.selPassword(user, paw)


def getStudentInfo(database: My_sqlite) -> tuple:
    """
    返回数据库里的学生信息
    """
    with database:
        return database.getStudentInfo()


def chanGePassword(database: My_sqlite, user: str, pad: str) -> bool:
    """
    修改登录密码
    """
    with database:
        return database.chanGePassword(user, pad)


def intoStudentInfo(database: My_sqlite, user: str, name: str, sex: str, age: str, address: str) -> bool:
    """
    往数据库中写入学生信息
    """
    with database:
        return database.intoStudentInfo(user, name, sex, age, address)


def stuinMysql(database: My_sqlite, user: str) -> bool:
    """
    判断某个学号是否存在于数据库中(student_info表) 存在return Ture
    """
    with database:
        return database.stuinMysql(user)


def delStudent(database: My_sqlite, user: str) -> bool:
    """
    删除学生信息
    """
    with database:
        return database.delStudent(user)


def upDataStudent(database: My_sqlite, user: str, name: str, sex: str, age: str, address: str) -> None:
    """
     更新学生信息
    """
    with database:
        database.upDataStudent(user, name, sex, age, address)


def getOneStudent(database: My_sqlite, user: str) -> list:
    """
    获取某个学生信息
    """
    with database:
        return database.getOneStudent(user)


def studnetScrore(database: My_sqlite) -> list:
    """
    返回全部学生成绩
    """
    with database:
        return database.studnetScrore()



