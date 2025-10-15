import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from database import get_analysis_data, add_reason, add_analysis
from main import analyze_single_value

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class AnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Проверка анализов")
        self.geometry("550x800")
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

            main_frame = ctk.CTkFrame(self)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)

            for col in range(6):
                main_frame.grid_columnconfigure(col, weight=1)

            headers = ["ID", "Название", "Мин", "Макс", "Причины пониженных значений", "Причины повышенных значений"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(main_frame, text=header, font=("Arial", 14, "bold")).grid(row=0, column=col, padx=5, pady=10, sticky="ew")

            table_frame = ctk.CTkScrollableFrame(main_frame, height=300)
            table_frame.grid(row=1, column=0, columnspan=6, sticky="nsew", pady=10)

            for col in range(6):
                table_frame.grid_columnconfigure(col, weight=1)

            for i, analysis in enumerate(self.analyses, start=1):
                id, name, min_val, max_val, low_reasons, high_reasons = analysis
                ctk.CTkLabel(table_frame, text=str(id)).grid(row=i, column=0, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(table_frame, text=name).grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(table_frame, text=str(min_val)).grid(row=i, column=2, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(table_frame, text=str(max_val)).grid(row=i, column=3, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(table_frame, text=str(low_reasons)).grid(row=i, column=4, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(table_frame, text=str(high_reasons)).grid(row=i, column=5, padx=10, pady=5, sticky="ew")

            input_frame = ctk.CTkFrame(main_frame)
            input_frame.grid(row=2, column=0, columnspan=6, sticky="ew", pady=10)

            self.name_entry = ctk.CTkEntry(input_frame, placeholder_text='Название', width=300)
            self.name_entry.grid(row=0, column=1, padx=10, pady=5)
            self.min_value_entry = ctk.CTkEntry(input_frame, placeholder_text='Мин', width=50)
            self.min_value_entry.grid(row=0, column=2, padx=10, pady=5)
            self.max_value_entry = ctk.CTkEntry(input_frame, placeholder_text='Макс', width=50)
            self.max_value_entry.grid(row=0, column=3, padx=10, pady=5)

            self.selected_low_reasons = []
            self.selected_high_reasons = []

            self.low_reasons_btn = ctk.CTkButton(input_frame, text="Список пониженных причин", width=30, command=self.add_low_reasons_btn)
            self.low_reasons_btn.grid(row=0, column=4, padx=10, pady=5)
            self.high_reasons_btn = ctk.CTkButton(input_frame, text="Список повышенных причин", width=30, command=self.add_high_reasons_btn)
            self.high_reasons_btn.grid(row=0, column=5, padx=10, pady=5)
            self.add_button = ctk.CTkButton(input_frame, text="Добавить анализ", command=self.add_analysis)
            self.add_button.grid(row=1, column=0, columnspan=6, pady=10)

            main_frame.grid_rowconfigure(1, weight=1)
            main_frame.grid_columnconfigure(0, weight=1)

        def update_buttons_text(self):
            if self.selected_low_reasons:
                ids_text = ' '.join(map(str, self.selected_low_reasons))
                self.low_reasons_btn.configure(text=ids_text)
            if self.selected_high_reasons:
                ids_text = ' '.join(map(str, self.selected_high_reasons))
                self.high_reasons_btn.configure(text=ids_text)

        def add_low_reasons_btn(self):
            window = ReasonSelectorWindow(self, reason_type="low")
            window.grab_set()
            window.focus_force()

        def add_high_reasons_btn(self):
            window = ReasonSelectorWindow(self, reason_type="high")
            window.grab_set()
            window.focus_force()

        def add_analysis(self):
            name = self.name_entry.get().strip()
            min_val_str = self.min_value_entry.get().strip()
            max_val_str = self.max_value_entry.get().strip()
            low_reasons_str = ' '.join(map(str, self.selected_low_reasons))
            high_reasons_str = ' '.join(map(str, self.selected_high_reasons))

            if name and min_val_str and max_val_str:
                try:
                    min_val = float(min_val_str)
                    max_val = float(max_val_str)
                    add_analysis(name, min_val, max_val, low_reasons_str, high_reasons_str)
                    CTkMessagebox(
                        title="Успех!",
                        message="Анализ успешно добавлен!",
                        icon="check"
                    )
                    self.name_entry.delete(0, "end")
                    self.min_value_entry.delete(0, "end")
                    self.max_value_entry.delete(0, "end")
                    self.selected_low_reasons = []
                    self.selected_high_reasons = []
                    self.update_buttons_text()
                except ValueError:
                    CTkMessagebox(title="Ошибка", message="Мин и макс должны быть числами!", icon="cancel")
                    return
            else:
                CTkMessagebox(title="Ошибка", message="Заполните все обязательные поля!", icon="cancel")


class ReasonSelectorWindow(ctk.CTkToplevel):
    def __init__(self, parent, reason_type):
        super().__init__(parent)
        self.parent = parent
        self.reason_type = reason_type
        self.selected_reasons = []
        self.setup_window()

    def setup_window(self):
        self.title(f"Выбор причин для {'пониженных' if self.reason_type=='low' else 'повышенных'} значений")
        self.geometry("600x500")
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Поиск причин...",
            width=400
        )
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.search_reasons)
        self.scroll_frame = ctk.CTkScrollableFrame(main_frame)
        self.scroll_frame.pack(fill="both", expand=True, pady=10)

        confirm_btn = ctk.CTkButton(
            main_frame,
            text="Подтвердить выбор",
            command=self.confirm_selection
        )
        confirm_btn.pack(pady=10)

        self.load_all_reasons()

    def load_all_reasons(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        from database import get_analysis_data
        _, reasons= get_analysis_data()

        self.checkboxes = {}
        sorted_reasons = sorted(reasons.items(), key=lambda x: x[1])

        for i, (reason_id, description) in enumerate(sorted_reasons):
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                self.scroll_frame,
                text=description,
                variable=var,
                command=lambda rid=reason_id, v=var: self.toggle_reason(rid, v)
            )
            checkbox.grid(row=i, column=0, sticky="w", padx=10, pady=2)
            self.checkboxes[reason_id] = var

    def toggle_reason(self, reason_id, var):
        if var.get():
            self.selected_reasons.append(reason_id)
        else:
            self.selected_reasons.remove(reason_id)

    def search_reasons(self, event=None):
        search_text = self.search_entry.get().lower().strip()
        for widget in self.scroll_frame.winfo_children():
                widget.destroy()
        _, reasons = get_analysis_data()

        filtered_reasons = [(id, desc) for id, desc in reasons.items()
                            if search_text in desc.lower()]

            # Если поиск пустой, показываем все причины
        if not search_text:
            filtered_reasons = list(reasons.items())

            # Показываем отфильтрованные причины
        self.checkboxes = {}
        sorted_reasons = sorted(filtered_reasons, key=lambda x: x[1])

        for i, (reason_id, description) in enumerate(sorted_reasons):
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                    self.scroll_frame,
                    text=description,
                    variable=var,
                    command=lambda rid=reason_id, v=var: self.toggle_reason(rid, v)
                )
            checkbox.grid(row=i, column=0, sticky="w", padx=10, pady=2)
            self.checkboxes[reason_id] = var

    def confirm_selection(self):
        if self.reason_type == "low":
            self.parent.selected_low_reasons = self.selected_reasons
        else:
            self.parent.selected_high_reasons = self.selected_reasons
        self.parent.update_buttons_text()
        self.destroy()

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
            self.search_frame = ctk.CTkFrame(self)
            self.search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
            self.search_entry = ctk.CTkEntry(
                self.search_frame,
                placeholder_text="Поиск причины...",
                width=400
            )
            self.search_entry.grid(row=0, column=0, padx=10, pady=5)
            self.search_entry.bind("<KeyRelease>", self.search_reasons)  # Поиск при вводе

            self.add_button = ctk.CTkButton(
                self.search_frame,
                text="Добавить причину",
                command=self.add_current_reason,
                width=150
            )
            self.add_button.grid(row=0, column=1, padx=10, pady=5)
            self.scrollable_frame = ctk.CTkScrollableFrame(self)
            self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.show_all_reasons()

        def search_reasons(self, event=None):
            search_text = self.search_entry.get().lower().strip()
            if search_text:
                self.filter_reasons(search_text)
            else:
                self.show_all_reasons()

        def filter_reasons(self, search_text):
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            filtered_reasons = [(id, desc) for id, desc in self.reasons.items() if search_text in desc.lower()]
            for i, (id, description) in enumerate(filtered_reasons):
                label = ctk.CTkLabel(self.scrollable_frame, text=description)
                label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        def show_all_reasons(self):
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            sorted_reasons = sorted(self.reasons.items(), key=lambda x: x[1])
            for i, (id, description) in enumerate(sorted_reasons):
                label = ctk.CTkLabel(self.scrollable_frame, text=f"{i+1}. {description}")
                label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        def add_current_reason(self):
            description = self.search_entry.get().strip()
            if description:
                add_reason(description)
                CTkMessagebox(
                        title="Успех!",
                        message="Причина успешно добавлена!",
                        icon="check"
                    )
                self.search_entry.delete(0, "end")
                _, self.reasons = get_analysis_data()
                self.show_all_reasons()





if __name__ == "__main__":
    app = AnalyzerApp()
    app.mainloop()