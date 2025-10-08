from collections import Counter
from database import get_analysis_data, parse_reasons

analyses, reasons, analysis_name = get_analysis_data()

# Функция для сравнения анализов с минимумом и максимумом
def analyze_single_value(analysis_name, analyses):
    results = []
    for analysis in analyses:
        id, name, min_value, max_value, low_value_reasons, high_value_reasons = analysis
        user_input = input(f"Вставьте значение для {name} (ср.зн. {min_value}-{max_value}): ")
        if user_input == '':
            continue
        user_value = float(user_input)
        if user_value < min_value:
            results.extend(parse_reasons(low_value_reasons))
        elif user_value > max_value:
            results.extend(parse_reasons(high_value_reasons))
        else:
            continue

    result_count = Counter(results)
    sorted_result = result_count.most_common()
    return sorted_result

sorted_result = analyze_single_value(analysis_name, analyses)
print("=== === === === ===")
print("Причины (от большего к меньшему):")
print("=== === === === ===")
for result, count in sorted_result:
    print(f"{reasons[result]} встречается {count} раз")
    print("--- --- ---")
