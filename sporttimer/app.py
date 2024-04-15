from flask import Flask
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="sporttime",
                                  # пароль, который указали при установке PostgreSQL
                                  password="SportRus12!",
                                  host="127.0.0.1",
                                  port="5432",
				database="sporttime_db")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    sql_create_database = 'create database sporttime_db'
    cursor.execute(sql_create_database)
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")

app = Flask(__name__)
@app.route('/')
def home():
    return '<h1>Hello!!!, World!</h1>'
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
