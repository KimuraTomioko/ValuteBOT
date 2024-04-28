import sqlite3

# Подключаемся к базе данных (если она существует) или создаем новую
conn = sqlite3.connect('database.db')

# Создаем курсор для выполнения операций с базой данных
cursor = conn.cursor()

# Создаем таблицу с тремя колонками: chat_id (целые числа), sum_to_buy (целые числа), paid (строки)
cursor.execute('''CREATE TABLE IF NOT EXISTS purchases
                  (chat_id INTEGER, sum_to_buy INTEGER, user_id_game INT, paid TEXT)''')

# Сохраняем изменения
conn.commit()

# Закрываем соединение с базой данных
conn.close()
