import tkinter as tk
from tkinter import ttk, messagebox as mb
import requests


class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курс обмена валюты к доллару")
        self.root.geometry("360x380")

        # Данные
        self.popular_currencies = [
            "EUR", "JPY", "GBP", "AUD", "CAD",
            "CHF", "CNY", "RUB", "KZT", "UZS", "USD"
        ]
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
        self.api_url = "https://open.er-api.com/v6/latest/USD"

        self._create_widgets()

    def _create_widgets(self):
        # Метка для базовой валюты
        label_base1 = tk.Label(self.root, text="Базовая валюта")
        label_base1.pack(padx=10, pady=10)
        self.combobox_base1 = ttk.Combobox(
            self.root,
            values=self.popular_currencies,
            state="readonly"
        )
        self.combobox_base1.current(0)  # По умолчанию EUR
        self.combobox_base1.pack(padx=10, pady=10)

        def on_combobox_base_change(event):
            # Получаем текущее значение из Combobox
            selected = self.combobox_base1.get()
            # Обновляем текст в Label
            label_base_name.config(text=self.currency_names[selected])
        label_base_name = tk.Label(self.root)
        label_base_name.pack(padx=10, pady=10)

        self.combobox_base1.bind("<<ComboboxSelected>>",
                               on_combobox_base_change)


        # Метка для второй базовой валюты
        label_base2 = tk.Label(self.root, text="Вторая базовая валюта")
        label_base2.pack(padx=10, pady=10)

        # Выпадающий список для второй базовой волюты
        self.combobox_base2 = ttk.Combobox(
            self.root,
            values=self.popular_currencies,
            state="readonly"
        )
        self.combobox_base2.current(1)  # По умолчанию JPY
        self.combobox_base2.pack(padx=10, pady=10)

        # Метка для целевой валюты
        label_target = tk.Label(self.root, text="Целевая валюта")
        label_target.pack(padx=10, pady=10)

        # Выпадающий список для второй базовой волюты
        self.combobox_target = ttk.Combobox(
            self.root,
            values=self.popular_currencies,
            state="readonly"
        )
        self.combobox_target.current(7)  # По умолчанию RUB
        self.combobox_target.pack(padx=10, pady=10)

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
