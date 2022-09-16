import random
import sqlite3

Num = ["0003", "0004", "0005", "0006", "0007", "0008"]
conn = sqlite3.connect("studentList.db")
cur = conn.cursor()
for i in Num:
    for j in range(1, 6):
        try:
            sql = f"INSERT INTO grade VALUES('{i}','{j}','{random.randint(30, 100)}')"
            cur.execute(sql)
            conn.commit()
        except:
            continue
