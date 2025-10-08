import sqlite3

# Функция для получения данных из таблицы Анализы
def get_analysis_data(db_path='analyze.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute('SELECT analysis_id, analysis_name, min_value, max_value, low_value_reasons, high_value_reasons FROM analysis')
    analyses = cur.fetchall()

    cur.execute('SELECT id, description FROM reasons')
    reasons = {row[0]: row[1] for row in cur.fetchall()}

    cur.execute('SELECT analysis_name FROM metrics')
    analysis_name = cur.fetchall()

    return analyses, reasons, analysis_name

# Функция для приведения причин в список
def parse_reasons(reasons_string):
    if not reasons_string:
        return []
    return[int(id_str) for id_str in reasons_string.split()]