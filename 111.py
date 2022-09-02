import sqlite3
conn=sqlite3.connect("studentList.db")
cursor=conn.cursor()
sql = f"SELECT pad FROM web_db WHERE No='001'"
print(cursor.execute(sql).fetchall()[0][0])