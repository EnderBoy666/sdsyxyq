import sqlite3
import csv


def export_table_to_csv(database_path, table_name, csv_path):
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # 查询表中的所有数据
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # 获取表的列名
        column_names = [description[0] for description in cursor.description]

        # 以utf - 8编码打开CSV文件并写入数据
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            # 写入列名
            csv_writer.writerow(column_names)

            # 写入数据行
            csv_writer.writerows(rows)

        print(f"数据已成功导出到 {csv_path}")

    except sqlite3.Error as e:
        print(f"SQLite错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        if conn:
            conn.close()

# 使用示例
if __name__ == "__main__":
    database_path = 'sdsyxyq\db.sqlite3'
    table_name = 'users_customuser'
    csv_path = 'sdsyxyq\output.csv'
    export_table_to_csv(database_path, table_name, csv_path)