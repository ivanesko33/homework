import requests
import tkinter as tk

# Пять наиболее популярных криптовалют
CRYPTO = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "solana": "Solana (SOL)",
    "binancecoin": "Binance Coin (BNB)",
    "ripple": "Ripple (XRP)"
}
# название файла с иконкой приложения и для кнопки
ICON_FILE = 'cript_coin.png'
# url строка для get запроса
PARAM = ','.join(CRYPTO.keys())
URL = (f"https://api.coingecko.com/api/v3/simple/price?ids"
       f"={PARAM}&vs_currencies=usd")
# список курсы популярных криптовалют к доллару США
result = list()
# иконка для криптовалют, для основного окна и для кнопки
# главное окно
root = tk.Tk()
root.title("курсы популярных криптовалют")
root.geometry("400x450")
# установка иконки окна
icon = tk.PhotoImage(file=ICON_FILE)
root.iconphoto(False, icon)

def parsing_data(data):
    """ GET запрос к coingecko для криптовалют в CRYPTO_MAP """
    global result
    for coin_id, display_name in CRYPTO.items():
        if coin_id in data:
            price_usd = data[coin_id].get("usd", 0)
            formatted_price = f"{price_usd:,.2f}"
            result.append({
                "coin_id": coin_id,
                "display_name": display_name,
                "price_usd": formatted_price,
                "status": "available"
            })
        else:
            result.append({
                "coin_id": coin_id,
                "display_name": display_name,
                "price_usd": None,
                "status": "missing"
            })
    return result

def show_coint_info(coin: dict) -> str:
    """ словарь описания монеты в строку """
    return f'{coin["display_name"]}: {coin["price_usd"]}'

def on_click():
    print("Кнопка нажата!")


try:
    # Установка таймаута на случай проблем со связью
    response = requests.get(URL, timeout=10)
    if response.status_code == 200:
        result  = parsing_data(response.json())


        for coin in result:
            label = tk.Label(
                root,
                text=show_coint_info(coin),
                wraplength=350,
                justify="left",
                font=("Arial", 14)
            )
            label.pack(pady=20)
        # кнопка для обновления
        btn = tk.Button(
            root,
            text="Обновить",
            image=icon,
            compound=tk.LEFT,
            command=on_click,
            padx=10,
            pady=5
        )
        btn.pack(pady=20)

        root.mainloop()

        for item in result:
            print(item)
    else:
        print(f"Ошибка API: код {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка сети: {str(e)}")
