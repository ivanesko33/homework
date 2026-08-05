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
# utl строка для get запроса
param = ",".join(CRYPTO.keys())
url = (f"https://api.coingecko.com/api/v3/simple/price?ids"
       f"={param}&vs_currencies=usd")
# список курсы популярных криптовалют к доллару США
result = list()


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

try:
    # Установка таймаута на случай проблем со связью
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        result  = parsing_data(response.json())
        # Создаём главное окно
        root = tk.Tk()
        root.title("курсы популярных криптовалют")
        root.geometry("400x450")
        import tkinter as tk
        # Загрузка и установка изображение для иконки окна
        icon = tk.PhotoImage(file="cript_coin.png")
        root.iconphoto(False, icon)

        for coin in result:
            label = tk.Label(root, text=show_coint_info(coin),
                             wraplength=350,
                            justify="left")
            label.pack(pady=20)
        # Запуск цикла
        root.mainloop()

        for item in result:
            print(item)
    else:
        print(f"Ошибка API: код {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка сети: {str(e)}")
