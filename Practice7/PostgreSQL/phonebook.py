import psycopg2
import csv
from config import load_config

def execute_query(sql, params=None):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                # conn.commit() выполнится автоматически при выходе из with
    except Exception as e:
        print(f'DB error: {e}')

def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook
    (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL
    )
    """
    execute_query(sql)
    print("Таблица успешно создана")

def insert_data_by_consol():
    print("Введите имя:")
    name = input()
    print("Введите номер:")
    num = input()
    sql = "INSERT INTO phonebook(name, phone_number) VALUES(%s, %s)"
    execute_query(sql, (name, num))

def insert_data_from_csv(file_path):
    sql = "INSERT INTO phonebook(name, phone_number) VALUES(%s, %s)"
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row: # проверка, что строка не пустая
                            cur.execute(sql, row)
        print(f"Данные успешно загружены из {file_path}")        
    except Exception as e:
        print(f"Error: {e}")

def update_data():
    print("Введите имя для поиска:")
    old_name = input()
    print("Введите новый номер:")
    new_num = input()
    # ИСПРАВЛЕНО: убрано слово TABLE
    sql = "UPDATE phonebook SET phone_number = %s WHERE name = %s"
    execute_query(sql, (new_num, old_name))
    print("Данные обновлены")

def search_to_insert():
    sql = "SELECT * FROM phonebook WHERE name LIKE %s"
    print("Введите имя для поиска:")
    search = input()
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (f'%{search}%',))
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Error: {e}")

def delete():
    print("Введите имя для удаления:")
    name = input()
    sql = "DELETE FROM phonebook WHERE name=%s"
    # ИСПРАВЛЕНО: добавлена запятая для создания кортежа
    execute_query(sql, (name,))
    print("Успешно удалено")

if __name__ == "__main__":
    # create_table() — это можно закомментировать, таблица уже есть
    insert_data_from_csv('phonebook.csv')
    
    # Чтобы протестировать загрузку из CSV:
    # 1. Создай файл phonebook.csv
    # 2. Напиши в нем: Имя,Номер
    # 3. Раскомментируй строку ниже:
    # insert_data_from_csv('phonebook.csv')