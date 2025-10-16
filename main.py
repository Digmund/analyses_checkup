from collections import Counter
from database import get_analysis_data, parse_reasons

# Получаем данные из базы данных
analyses, reasons = get_analysis_data()

# Функция для сравнения анализов с минимумом и максимумом
def analyze_single_value(user_inputs, analyses):
    results = []
    for analysis in analyses:
        id, name, min_value, max_value, low_value_reasons, high_value_reasons = analysis
        # Если имя есть в инпутах, то значение меняем на float
        if name in user_inputs:
            user_value = float(user_inputs[name])
        else:
            continue
        # Распределение
        if user_value < min_value:
            results.extend(parse_reasons(low_value_reasons))
        elif user_value > max_value:
            results.extend(parse_reasons(high_value_reasons))
        else:
            continue
    # Подсчитываем результаты
    result_count = Counter(results)
    sorted_result = result_count.most_common()
    return sorted_result