import requests

CRYPTO_MAP = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "solana": "Solana (SOL)",
    "binancecoin": "Binance Coin (BNB)",
    "ripple": "Ripple (XRP)"
}

ids_param = ",".join(CRYPTO_MAP.keys())
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_param}&vs_currencies=usd"


def parsing_data(data):
    # pprint(data, indent=4, width=30)
    for coin_id, display_name in CRYPTO_MAP.items():
        if coin_id in data:
            price_usd = data[coin_id].get("usd", 0)
            # Форматируем цену: отделяем тысячи запятыми и оставляем 2 знака после запятой
            print(f"{display_name:<20} : $ {price_usd:,.2f}")
        else:
            print(f"{display_name:<20} : Данные отсутствуют")


try:
    # Установка таймаута на случай проблем со связью
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        parsing_data(data)
    else:
        print(f"Ошибка API: код {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка сети: {str(e)}")