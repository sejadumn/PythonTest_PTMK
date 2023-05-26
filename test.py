import sys
import sqlite3
import random
import string
from datetime import datetime

# Получение параметра командной строки
command = sys.argv[1] if len(sys.argv) > 1 else ''

# Подключение к базе данных SQLite
conn = sqlite3.connect('mydatabase.db')

# Установка кодировки UTF-8 для базы данных
conn.execute('PRAGMA encoding = "UTF-8"')

# Создание таблицы
def create_table():
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                gender TEXT NOT NULL
            )
        ''')
        print("Таблица 'users' успешно создана.")
    except sqlite3.Error as e:
        print("Ошибка при создании таблицы:", e)

# Добавление записи
def add_user(full_name, date_of_birth, gender):
    try:
        conn.execute('INSERT INTO users (full_name, date_of_birth, gender) VALUES (?, ?, ?)',
                     (full_name, date_of_birth, gender))
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при добавлении записи:", e)

# Генерация случайного пола
def generate_gender():
    genders = ['Male', 'Female']
    return random.choice(genders)

# Генерация случайной даты рождения
def generate_date_of_birth():
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2005, 12, 31)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")

# Генерация случайного ФИО
def generate_full_name():
    first_letter = random.choice(string.ascii_uppercase)
    remaining_letters = ''.join(random.choices(string.ascii_lowercase, k=4))
    return first_letter + remaining_letters

# Заполнение автоматически 1 000 000 строк
def generate_data():
    for _ in range(1000000):
        full_name = generate_full_name()
        date_of_birth = generate_date_of_birth()
        gender = generate_gender()
        add_user(full_name, date_of_birth, gender)
    print("Данные успешно сгенерированы.")

# Заполнение автоматически 100 строк с мужским полом и начальной буквой "F"
def generate_additional_data():
    for _ in range(100):
        full_name = "F" + ''.join(random.choices(string.ascii_lowercase, k=4))
        date_of_birth = generate_date_of_birth()
        gender = "Male"
        add_user(full_name, date_of_birth, gender)
    print("Дополнительные данные успешно сгенерированы.")

# Выборка данных по критерию пола и начальной буквы ФИО
def select_data():
    try:
        start_time = datetime.now()
        query = '''
            SELECT full_name, date_of_birth, gender,
                (strftime('%Y', 'now') - strftime('%Y', date_of_birth)) - (strftime('%m-%d', 'now') < strftime('%m-%d', date_of_birth)) AS age
            FROM users
            WHERE gender = 'Male' AND full_name LIKE 'F%'
            ORDER BY full_name
        '''
        result = conn.execute(query)
        for row in result:
            print(f"ФИО: {row[0]}, Дата рождения: {row[1]}, Пол: {row[2]}, Количество полных лет: {row[3]}")
        end_time = datetime.now()
        execution_time = end_time - start_time
        print("Время выполнения: ", execution_time)
    except sqlite3.Error as e:
        print("Ошибка при выполнении запроса:", e)

# Обработка параметра командной строки
if command == '1':
    create_table()
elif command == '2':
    if len(sys.argv) == 5:
        full_name = sys.argv[2]
        date_of_birth = sys.argv[3]
        gender = sys.argv[4]
        add_user(full_name, date_of_birth, gender)
    else:
        print("Неверное количество аргументов. Используйте формат: myApp 2 ФИО ДатаРождения Пол")
elif command == '3':
    select_data()
elif command == '4':
    generate_data()
    generate_additional_data()
elif command == '5':
    select_data()

# Закрытие соединения с базой данных
conn.close()
