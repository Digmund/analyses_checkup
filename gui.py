import customtkinter as ctk
from database import get_analysis_data, add_reason
from main import analyze_single_value

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class AnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Проверка анализов")
        self.geometry("600x800")
        self.analyses, self.reasons = get_analysis_data()
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
        self.results_text = ctk.CTkTextbox(self, width=500, height=400)
        self.results_text.grid(row=len(self.analyses)+2, column=0, columnspan=2, padx=10, pady=10)
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=len(self.analyses)+3, column=0, columnspan=2, pady=10)
        self.all_analyses_btn = ctk.CTkButton(
            button_frame,
            text="Все анализы",
            command=self.show_all_analyses,
            width=120
        )
        self.all_analyses_btn.grid(row=0, column=0, padx=10)
        self.all_reasons_btn = ctk.CTkButton(
            button_frame,
            text="Все причины",
            command=self.show_all_reasons,
            width=120
        )
        self.all_reasons_btn.grid(row=0, column=1, padx=10)

    def show_all_analyses(self):
        window = AllAnalyses(self, self.analyses)
        window.attributes('-topmost', True)

    def show_all_reasons(self):
        window = AllReasons(self, self.reasons)
        window.attributes('-topmost', True)

    def analyze(self):
        user_inputs = {}
        for name, entry_widget in self.entries.items():
            value = entry_widget.get().strip()
            if value:
                user_inputs[name] = float(value)
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

# Класс для кнопки "Все анализы"
class AllAnalyses(ctk.CTkToplevel):
        def __init__(self, parent, analyses):
            super().__init__(parent)
            self.analyses = analyses
            self.setup_window()

        def setup_window(self):
            self.title("Все анализы")
            self.geometry("1000x600")
            self.lift()
            self.focus_force()

            headers = ["ID", "Название", "Мин", "Макс", "Причины пониженных значений", "Причины повышенных значений"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(self, text=header, font=("Arial", 14, "bold")).grid(row=0, column=col, padx=10, pady=10)

            for i, analysis in enumerate(self.analyses, start=1):
                id, name, min_val, max_val, low_reasons, high_reasons = analysis
                ctk.CTkLabel(self, text=str(id)).grid(row=i, column=0, padx=10, pady=5)
                ctk.CTkLabel(self, text=name).grid(row=i, column=1, padx=10, pady=5)
                ctk.CTkLabel(self, text=str(min_val)).grid(row=i, column=2, padx=10, pady=5)
                ctk.CTkLabel(self, text=str(max_val)).grid(row=i, column=3, padx=10, pady=5)
                ctk.CTkLabel(self, text=str(low_reasons)).grid(row=i, column=4, padx=10, pady=5)
                ctk.CTkLabel(self, text=str(high_reasons)).grid(row=i, column=5, padx=10, pady=5)

            self.button = ctk.CTkButton(self, text="Добавить анализ", command=self.open_add_analysis)
            self.button.grid(row=len(self.analyses)+1, column=0, columnspan=2, pady=20)

        def open_add_analysis(self):
            window = AddAnalysis(self)
            window.attributes('-topmost', True)

# Класс для кнопки "Добавить анализ"
class AddAnalysis(ctk.CTkToplevel):
        def __init__(self, parent):
            super().__init__(parent)
            self.setup_window()

        def setup_window(self):
            self.title("Добавить анализ")
            self.geometry("1000x100")
            self.lift()
            self.focus_force()
            headers = ["ID", "Название", "Мин", "Макс", "Причины пониженных значений", "Причины повышенных значений"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(self, text=header, font=("Arial", 14, "bold")).grid(row=0, column=col, padx=10, pady=10)

# Класс для кнопки "Все причины"
class AllReasons(ctk.CTkToplevel):
        def __init__(self, parent, reasons):
            super().__init__(parent)
            self.reasons = reasons
            self.setup_window()

        def setup_window(self):
            self.title("Все причины")
            self.geometry("600x800")
            self.lift()
            self.focus_force()
            self.scrollable_frame = ctk.CTkScrollableFrame(self)
            self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            sorted_reasons = sorted(self.reasons.items(), key=lambda x: x[1])
            for i, (reason_id, description) in enumerate(sorted_reasons, start=1):
                label = ctk.CTkLabel(self.scrollable_frame, text=f"{i}. {description}")
                label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.button = ctk.CTkButton(self, text="Добавить причину", command=self.add_reason)
            self.button.grid(row=len(self.reasons)+1, column=0, columnspan=2, pady=20)

        def add_reason(self):
            window = AddReason(self)
            window.attributes('-topmost', True)

class AddReason(ctk.CTkToplevel):
    def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.setup_window()

    def setup_window(self):
        self.title("Добавить причину")
        self.geometry("500x100")
        self.entry = ctk.CTkEntry(self, placeholder_text="Введите причину", width=300)
        self.entry.grid(row=1, column=1, padx=10, pady=5)
        self.button = ctk.CTkButton(self, text="Добавить", command=self.add_reason_to_db)
        self.button.grid(row=1, column=2, pady=20)

    def add_reason_to_db(self):
        description = self.entry.get().strip()
        if description:
            add_reason(description)
            self.destroy()




if __name__ == "__main__":
    app = AnalyzerApp()
    app.mainloop()