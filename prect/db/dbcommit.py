import sqlite3

class ErrorImport(ValueError):
    def __init__(self, message):
        super().__init__(message)
        self.msgfmt = message

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('bakery.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS client (
    user_id INT AUTO_INCREMENT NOT NULL,
    name TEXT NOT NULL,
    login TEXT NOT NULL,
    email TEXT NOT NULL,
    PRIMARY KEY(user_id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS goods (
    good_id INT AUTO_INCREMENT NOT NULL,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY(good_id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    client_id INT NOT NULL,
    when_buy TEXT NOT NULL,
    good_id INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(user_id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT,
    FOREIGN KEY (good_id) REFERENCES goods(good_id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
);
''')

connection.commit()

def get_column_names(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]  # Получаем только имена столбцов
    return column_names


def intoBD(val, tablename):
    column_names = get_column_names(tablename)
    result = ', '.join(column_names)
    values = ', '.join(f':{column}' for column in column_names)

    sql = f'INSERT INTO {tablename} ({result}) VALUES ({values})'
    cursor.execute(sql, val)
    return cursor.rowcount

def csvAppend(filename, tablename):
    with open(filename, 'r', encoding='utf-8') as file:
        line_count = sum(1 for _ in file)  # Подсчет строк

    column_names = get_column_names(tablename)

    file = open(filename, 'r', encoding='utf-8')
    m = []
    for i in range(line_count):
        st = file.readline().strip().split(';')
        m.append(dict(zip(column_names, st)))
    file.close()

    suc = 0

    for k in range(len(m)):
        suc = suc + (intoBD(m[k], f'{tablename}'))

    if suc == len(m): return 0
    else: raise ErrorImport(f'Ошибка импорта данных в таблицу, выполнено {suc}/{len(m)}')

def outPrint(TableName):
    data = cursor.execute(f'''SELECT * FROM {TableName}''')
    for row in data:
        print(row)

# data = cursor.execute(f'''SELECT * FROM client ''')
# c = []
# for row in data:
#     c.append(row[3] if row[3][0] == "z" else None)
# for row in c:
#     if row == None: pass
#     else: print(row)
# print(list(cursor.execute('''SELECT * FROM client WHERE user_id > 10''')))
# print(list(cursor.execute('''SELECT * FROM client''')))
# print(list(cursor.execute(''' SELECT * FROM client WHERE ''')))
# outPrint('goods')
connection.commit()