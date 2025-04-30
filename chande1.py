import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('sdsyxyq/db.sqlite3')
cursor = conn.cursor()

# 执行删除操作，删除 2025-04-27 注册的用户
cursor.execute("DELETE FROM users_customuser WHERE date_joined LIKE '2025-04-29%'")

# 提交更改并关闭连接
conn.commit()
conn.close()