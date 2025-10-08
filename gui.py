import customtkinter as ctk
from database import get_analysis_data
from collections import Counter
from main import analyze_single_value

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class AnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Проверка анализов")
        self.geometry("600x800")

        self.analyses, self.reasons, _ = get_analysis_data()

        self.create_widgets()

    def create_widgets(self):
        self.entries = {}  # Словарь для хранения полей ввода

            # Заголовок
        self.label = ctk.CTkLabel(self, text="Введите результаты анализов", font=("Arial", 16))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Создаем поля ввода для каждого анализа
        for i, analysis in enumerate(self.analyses, start=1):
            id, name, min_val, max_val, low_reasons, high_reasons = analysis

            # Название анализа
            label = ctk.CTkLabel(self, text=f"{name} ({min_val}-{max_val})")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            # Поле ввода
            entry = ctk.CTkEntry(self, placeholder_text="Введите значение", width=150)
            entry.grid(row=i, column=1, padx=10, pady=5)

            self.entries[name] = entry  # Сохраняем поле по имени анализа

        # Кнопка проверки
        self.button = ctk.CTkButton(self, text="Проверить", command=self.analyze)
        self.button.grid(row=len(self.analyses)+1, column=0, columnspan=2, pady=20)

        # Поле для результатов
        self.results_text = ctk.CTkTextbox(self, width=600, height=400)
        self.results_text.grid(row=len(self.analyses)+2, column=0, columnspan=2, padx=10, pady=10)

    def analyze(self):
        user_inputs = {}

        for name, entry_widget in self.entries.items():
            value = entry_widget.get().strip()
            if value:
                try:
                    user_inputs[name] = float(value)
                except ValueError:
                    # Можно показать ошибку
                    pass

        sorted_result = analyze_single_value(user_inputs, self.analyses)

        self.results_text.delete("1.0", "end")

        if sorted_result:
            result_text = "Причины отклонений:\n\n"
            result_text += "=== Топ 3 причины ===\n\n"
            for result_id, count in sorted_result[0:3]:
                reason_text = self.reasons.get(result_id, f"Неизвестная причина (ID: {result_id})")
                result_text += f"• {reason_text} (встречается {count} раз)\n"
            result_text += "\n=== === === === ===\n"
            for result_id, count in sorted_result[3:]:
                reason_text = self.reasons.get(result_id, f"Неизвестная причина (ID: {result_id})")
                result_text += f"• {reason_text} (встречается {count} раз)\n"
        else:
            result_text = "Все показатели в норме!"

        self.results_text.insert("1.0", result_text)


if __name__ == "__main__":
    app = AnalyzerApp()
    app.mainloop()