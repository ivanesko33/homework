import tkinter as tk
from tkinter import ttk, messagebox as mb
import requests


class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курс обмена валюты")
        self.root.geometry("360x450")

        # Данные
        self.currency_names = {
            "EUR": "Евро",
            "JPY": "Японская иена",
            "GBP": "Фунт стерлингов",
            "AUD": "Австралийский доллар",
            "CAD": "Канадский доллар",
            "CHF": "Швейцарский франк",
            "CNY": "Китайский юань",
            "RUB": "Российский рубль",
            "KZT": "Казахстанский тенге",
            "UZS": "Узбекский сум",
            "USD": "Американский доллар",
        }
        self.popular_currencies = list(self.currency_names.keys())
        self.api_url = "https://open.er-api.com/v6/latest/USD"

        self._create_widgets()

    def _create_widgets(self):
        def create_widget_base1():
            """ ПодВиджет Первая базовая валюта """
            self.label_base1 = tk.Label(
                self.root,
                text="Базовая валюта",
                font=("Arial", 14, "bold"))
            self.label_base1.pack(padx=10, pady=10)
            self.combobox_base1 = ttk.Combobox(
                self.root,
                values=self.popular_currencies,
                state="readonly"
            )
            self.combobox_base1.current(0)  # По умолчанию EUR
            self.combobox_base1.pack(padx=10, pady=10)
            def on_combobox_base1_change(event):
                selected = self.combobox_base1.get()
                self.label_base_name.config(
                    text=self.currency_names[selected])

            self.label_base_name = tk.Label(
                self.root,
                text=self.currency_names[self.combobox_base1.get()]
            )
            self.label_base_name.pack(padx=10, pady=10)

            self.combobox_base1.bind(
                "<<ComboboxSelected>>",
                on_combobox_base1_change)

        create_widget_base1()

        def create_widget_base2():
            """ Второй базовой валюты """
            self.label_base2 = tk.Label(
                self.root,
                text="Вторая базовая валюта",
                font=("Arial", 14, "bold")
            )
            self.label_base2.pack(padx=10, pady=10)
            self.combobox_base2 = ttk.Combobox(
                self.root,
                values=self.popular_currencies,
                state="readonly"
            )
            self.combobox_base2.current(1)  # По умолчанию JPY
            self.combobox_base2.pack(padx=10, pady=10)

            def on_combobox_base2_change(event):
                selected = self.combobox_base2.get()
                self.label_base2_name.config(
                    text=self.currency_names[selected])

            self.label_base2_name = tk.Label(
                self.root,
                text=self.currency_names[self.combobox_base2.get()]
            )
            self.label_base2_name.pack(padx=10, pady=10)

            self.combobox_base2.bind("<<ComboboxSelected>>",
                                     on_combobox_base2_change)

        create_widget_base2()

        def create_widget_target():
            """ Целевой валюты """
            self.label_target = tk.Label(
                self.root,
                text="Целевая валюта",
                font=("Arial", 14, "bold")
            )
            self.label_target.pack(padx=10, pady=10)
            self.combobox_target = ttk.Combobox(
                self.root,
                values=self.popular_currencies,
                state="readonly"
            )
            self.combobox_target.current(7)  # По умолчанию RUB
            self.combobox_target.pack(padx=10, pady=10)

            def on_combobox_target_change(event):
                selected = self.combobox_target.get()
                self.label_target_name.config(
                    text=self.currency_names[selected])
            self.label_target_name = tk.Label(
                self.root,
                text=self.currency_names[self.combobox_target.get()]
            )
            self.label_target_name.pack(padx=10, pady=10)

            self.combobox_target.bind("<<ComboboxSelected>>",
                                     on_combobox_target_change)

        create_widget_target()

        # Кнопка
        btn = tk.Button(
            self.root,
            text="Получить курс обмена",
            command=self.on_exchange_click
        )
        btn.pack(padx=10, pady=10)

    def on_exchange_click(self):
        code = self.combobox.get()
        if not code:
            mb.showwarning("Внимание", "Выберите код валюты")
            return

        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            data = response.json()

            rates = data.get("rates", {})
            if code in rates:
                exchange_rate = rates[code]
                mb.showinfo(
                    f"Курс обмена",
                    (f"Курс к доллару:"
                     f"{exchange_rate:.1f} {code} за 1 "
                     f"доллар")
                )
            else:
                mb.showerror(
                    "Ошибка",
                    f"Валюта {code} не найдена"
                )
        except requests.exceptions.RequestException as e:
            mb.showerror("Ошибка сети", f"Ошибка запроса: {e}")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()
