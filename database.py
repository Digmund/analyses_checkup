import sqlite3

# Функция для получения данных из таблицы Анализы
def get_analysis_data(db_path='analyze.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Запрос для получения всех данных
    cur.execute('SELECT analysis_id, analysis_name, min_value, max_value, low_value_reasons, high_value_reasons FROM analysis')
    analyses = cur.fetchall()
    # Запрос для получения всех причин
    cur.execute('SELECT id, description FROM reasons')
    reasons = {row[0]: row[1] for row in cur.fetchall()}

    return analyses, reasons

# Функция для приведения причин в список
def parse_reasons(reasons_string):
    if not reasons_string:
        return []
    return[int(id_str) for id_str in reasons_string.split()]

# Функция для добавления анализа
def add_analysis(name, min_val, max_val, low_reasons_str, high_reasons_str, db_path='analyze.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Запрос для добавления анализа
    cur.execute('''INSERT OR IGNORE INTO analysis (analysis_name, min_value, max_value, low_value_reasons, high_value_reasons)
                VALUES (?, ?, ?, ?, ?)''', (name, min_val, max_val, low_reasons_str, high_reasons_str))

    conn.commit()
    conn.close()

# Функция для добавления причины
def add_reason(description, db_path='analyze.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Запрос для добавления причины
    cur.execute('''
                INSERT OR IGNORE INTO reasons (description)
                VALUES (?)''', (description,))

    conn.commit()
    conn.close()