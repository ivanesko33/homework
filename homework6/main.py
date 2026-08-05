"""
Приложение с графическим интерфейсом на языке Python, которое отображать
текущие курсы популярных криптовалют к доллару США,
используя данные открытого API CoinGecko. https://www.coingecko.com/en/api .
"""
import requests
import tkinter as tk
from tkinter import PhotoImage
from tkinter import Button
from tkinter import Label
import sys

# название файла с иконкой приложения и для кнопки
ICON_FILE = 'cript_coin.gif'
# Пять наиболее популярных криптовалют
CRYPTO = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "solana": "Solana (SOL)",
    "binancecoin": "Binance Coin (BNB)",
    "ripple": "Ripple (XRP)"
}
# url строка для get запроса
PARAM = ','.join(CRYPTO.keys())
URL = (f"https://api.coingecko.com/api/v3/simple/price?ids"
       f"={PARAM}&vs_currencies=usd")

def parse_data_from_api(data_: dict | None) -> list | None :
    result = []  # локальный список
    if data_ is not None:
        for coin_id, display_name in CRYPTO.items():
            if coin_id in data_:
                price_usd = data_[coin_id].get("usd", 0)
                formatted_price = f"{price_usd:,.2f}"
                result.append({
                    "coin_id": coin_id,
                    "display_name": display_name,
                    "price_usd": formatted_price,
                    "status": "ok"
                })
            else:
                result.append({
                    "coin_id": coin_id,
                    "display_name": display_name,
                    "price_usd": None,
                    "status": "missing"
                })
        return result
    else:
        return None


def get_data_by_api(url_: str) -> dict | None:
    """ GET запрос к API CoinGecko """
    try:
        response = requests.get(url_, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"ОШИБКА API: код {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"ОШИБКА сети: {str(e)}")
        return None


def create_tk_interface():
    """ работа с UI """
    def load_icon(icon_file_name: str) -> PhotoImage | None:
        """ загрузка иконки, если нет то без иконки, вернуть None """
        try:
            return PhotoImage(file=icon_file_name)
        except tk.TclError as e:
            print(f'ОШИБКА загрузки иконки: {e}')
            return None

    def show_window_icon(window_ : tk.Tk, icon_: PhotoImage | None) -> None:
        """установить иконку окна """
        if icon_ is not None:
            window_.iconphoto(False, icon_)

    # Храним ссылки на метки, чтобы обновлять их
    price_labels = []

    def coin_info_for_lable(coin: dict) -> str:
        """ словарь описания монеты в строку """
        price = coin["price_usd"]
        if price is None:
            return f'{coin["display_name"]}: нет данных'
        return f'{coin["display_name"]}: {price}'

    def show_coin_prices(result_: list) -> None:
        """  вывести информацию о стоймости криптовалют """
        # Очищаем старые метки
        for label in price_labels:
            label.destroy()
        price_labels.clear()

        for coin in result_:
            label = tk.Label(
                window,
                text=coin_info_for_lable(coin),
                wraplength=350,
                justify="left",
                font=("Arial", 14)
            )
            label.pack(pady=10)
            price_labels.append(label)

    def refresh():
        """ Обновление по нажатию на кнопку Обновить """
        data = get_data_by_api(URL)
        prices = parse_data_from_api(data)
        show_coin_prices(prices)

    def show_refresh_button(window_, fn_refresh_, icon_ = PhotoImage |
                                                          None) -> Button:
        if icon_ is not None:
            btn = tk.Button( # иконка загрузилась
                window_,
                text="Обновить",
                image=icon_,
                compound=tk.LEFT,
                command=fn_refresh_,
                padx=10,
                pady=5
            )
            btn.image = icon_
        else:
            btn = tk.Button( # без иконки
                window_,
                text="Обновить",
                command=fn_refresh_,
                padx=10,
                pady=5
            )
        btn.pack(pady=20)
        return btn

    # главное окно
    window = tk.Tk() # объект Tk
    window.title("курсы популярных криптовалют")
    window.geometry("400x450")

    # загружаем иконку для отображения в окне и на кнопке
    icon = load_icon(ICON_FILE)
    show_window_icon(window, icon)

    # загружаем данные
    initial_data = get_data_by_api(URL)
    initial_prices = parse_data_from_api(initial_data)

    # отображаем данные
    show_coin_prices(initial_prices)

    # добавляем кнопку для обновления данных
    show_refresh_button(window, refresh, icon)

    window.mainloop()

if __name__ == "__main__":
    if sys.version_info >= (3, 11):
        create_tk_interface()
    else:
        print("Программа разработана для версия Python 3.11 или выше")
        print((f"Текущая версия {sys.version_info.major}"
               f".{sys.version_info.minor} — ниже 3.11"))
        sys.exit(1)


