import tkinter as tk
from tkinter import ttk, messagebox as mb
import requests


class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курс обмена валюты к доллару")
        self.root.geometry("360x180")

        # Данные
        self.popular_currencies = [
            "EUR", "JPY", "GBP", "AUD", "CAD",
            "CHF", "CNY", "RUB", "KZT", "UZS"
        ]
        self.api_url = "https://open.er-api.com/v6/latest/USD"

        self._create_widgets()

    def _create_widgets(self):
        # Метка
        label = tk.Label(self.root, text="Выберите код валюты:")
        label.pack(padx=10, pady=10)

        # Выпадающий список
        self.combobox = ttk.Combobox(
            self.root,
            values=self.popular_currencies,
            state="readonly"
        )
        self.combobox.current(7)  # По умолчанию RUB
        self.combobox.pack(padx=10, pady=10)

        # Кнопка
        btn = tk.Button(
            self.root,
            text="Получить курс обмена к доллару",
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
                    "Курс обмена",
                    f"Курс к доллару: {exchange_rate:.1f} {code} за 1 доллар"
                )
            else:
                mb.showerror("Ошибка", f"Валюта {code} не найдена")
        except requests.exceptions.RequestException as e:
            mb.showerror("Ошибка сети", f"Ошибка запроса: {e}")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()