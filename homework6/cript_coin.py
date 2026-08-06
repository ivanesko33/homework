"""
Приложение с графическим интерфейсом на языке Python, которое отображать
текущие курсы популярных криптовалют к доллару США,
используя данные открытого API CoinGecko. https://www.coingecko.com/en/api
"""
import requests
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from datetime import datetime
import sys
import os


# краткое описание программы для отображения в UI
DESCRIPTION = (
    'Запрос к API CoinGecko для отображения информации о '
    'стоимости пяти наиболее популярных криптовалют '
    'к доллару США'
)
# название файла с иконкой приложения и для кнопки
ICON_FILE = 'cript_coin.gif'
# названия файла для логов, используется если только существует
LOG_FILE = 'cript_coin.log'
# названия файла для хранения архива, используется если только существует
DAT_FILE = 'cript_coin.txt'

# Пять наиболее популярных криптовалют
CRYPTO = {
    'bitcoin': 'Bitcoin (BTC)',
    'ethereum': 'Ethereum (ETH)',
    'solana': 'Solana (SOL)',
    'binancecoin': 'Binance Coin (BNB)',
    'ripple': 'Ripple (XRP)'
}
# url строка для get запроса
PARAM = ','.join(CRYPTO.keys())
URL = (f'https://api.coingecko.com/api/v3/simple/price?ids'
       f'={PARAM}&vs_currencies=usd')

# сообщения для вывода в msgbox или в log
WARNING_MSGS = {
    'api429': (
        'Предел запросов к API превышен, повторите '
        'запрос через некоторое время ~20..30 секунд.'
    ),
    'netExcept': (
        'Ошибка сети, проверьти что сайт '
        'https://coingecko.com/ доступен'
    ),
    'apiErr': 'Ошибка API: ',
    'iconLoadFailed': ''
}


def show_warning(err_code: str, msg='', logging=True) -> None:
    """  отобразить модальный предупреждающий диалог и/или лог в файл """
    now = datetime.now()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(
                f"{now.strftime("%Y-%m-%d %H:%M:%S")}"
                f"[{WARNING_MSGS.get(err_code)}] {msg}"
            )
    if logging:
        print(
            f"{now.strftime("%Y-%m-%d %H:%M:%S")}"
            f"[{WARNING_MSGS.get(err_code)}] {msg}")
    messagebox.showwarning(
        'Внимание',
        WARNING_MSGS.get(err_code)
    )


def parse_data_from_api(data_: dict | None) -> list | None:
    """ парсит полученный json от api в словать для отображения """
    result = []  # локальный список

    def write_data_to_archive(data_: dict | None) -> None:
        """ если файл для записи результутов запросов есть, добавить """
        now = datetime.now()
        if os.path.exists(DAT_FILE):
            with open(DAT_FILE, "a", encoding="utf-8") as f:
                f.write(
                    f"{now.strftime("%Y-%m-%d %H:%M:%S")}\t"
                    f"{data_}"
                )

    if data_ is not None:
        write_data_to_archive(data_)
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


def get_data_by_api(url_: str) -> dict | None:
    """ GET запрос к API CoinGecko """
    try:
        response = requests.get(url_, timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            show_warning('api429')
            return None
        else:
            show_warning('apiErr', f'{response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        show_warning('netExcept', f'{str(e)}')
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

    def show_window_icon(window_: tk.Tk, icon_: PhotoImage | None) -> None:
        """ установить иконку окна """
        if icon_ is not None:
            window_.iconphoto(False, icon_)

    # Храним ссылки на метки, чтобы обновлять их
    price_labels = []

    def coin_info_for_lable(coin: dict) -> str:
        """ словарь описания монеты в строку """
        price = coin['price_usd']
        if price is None:
            return f'{coin['display_name']}: нет данных'
        return f'{coin['display_name']}: {price}'

    def show_coin_prices(result_: list | None) -> None:
        """  вывести информацию о стоймости криптовалют """
        # если нет новых данных, то оставить предыдущие
        if result_ is None:
            return

        # Очищаем старые метки
        for label in price_labels:
            label.destroy()
        price_labels.clear()

        for i, coin in enumerate(result_):
            label = tk.Label(
                window,
                text=coin_info_for_lable(coin),
                wraplength=380,
                justify=tk.LEFT,
                font=("Arial", 14)
            )
            # Без sticky — виджет центрируется в ячейке
            label.grid(row=1 + i, column=1, pady=5)
            price_labels.append(label)

    def fn_refresh():
        """ Обновление по нажатию на кнопку Обновить """
        data = get_data_by_api(URL)
        prices = parse_data_from_api(data)
        if len(prices) != 0:
            show_coin_prices(prices)

    def show_refresh_button(
            window_,
            fn_refresh_,
            icon_=PhotoImage | None) -> tk.Button:
        """ отображает refresh кнопку для запроса новых данных """
        if icon_ is not None:  ## иконка загрузилась
            btn = tk.Button(
                window_,
                text="Обновить",
                image=icon_,
                compound=tk.LEFT,
                command=fn_refresh,
                padx=10,
                pady=5
            )
            btn.image = icon_
        else:
            btn = tk.Button(
                window_,
                text="Обновить",
                command=fn_refresh,
                padx=10,
                pady=5
            )
        # Кнопка тоже в центральном столбце (column=1)
        btn.grid(row=6, column=1, pady=20)
        return btn

    # главное окно
    window = tk.Tk()
    window.title("Курсы популярных криптовалют")
    window.geometry("500x550")
    window.resizable(width=False, height=False)

    # Ключевой момент: растягиваем центральный столбец
    window.grid_columnconfigure(1, weight=1)
    # Опционально: можно растянуть и по вертикали, если нужно
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(6, weight=1)

    # загружаем иконку для отображения в окне и на кнопке
    icon = load_icon(ICON_FILE)
    show_window_icon(window, icon)

    # Описание — в центральном столбце
    desc_label = tk.Label(
        window,
        text=(
            "Запрос к API CoinGecko для отображения информации о "
            "стоимости пяти наиболее популярных криптовалют "
            "к доллару США"
        ),
        wraplength=380,
        justify=tk.LEFT,
        font=("Arial", 10),
        fg="#333333"
    )
    desc_label.grid(row=0, column=1, sticky="n", pady=(30, 10))

    # загружаем данные
    initial_data = get_data_by_api(URL)
    initial_prices = parse_data_from_api(initial_data)

    # отображаем данные
    show_coin_prices(initial_prices)

    # добавляем кнопку для обновления данных
    show_refresh_button(window, fn_refresh, icon)

    window.mainloop()


# main
if __name__ == '__main__':
    if sys.version_info >= (3, 11):  # для версии 3.11 или выше
        create_tk_interface()
    else:
        print('Программа разработана для версия Python 3.11 или выше')
        print((f'Текущая версия {sys.version_info.major}'
               f'.{sys.version_info.minor} — ниже 3.11'))
        sys.exit(1)
