import requests

# Пять наиболее популярных криптовалют
CRYPTO_MAP = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "solana": "Solana (SOL)",
    "binancecoin": "Binance Coin (BNB)",
    "ripple": "Ripple (XRP)"
}
# строка для get запроса
ids_param = ",".join(CRYPTO_MAP.keys())
url = (f"https://api.coingecko.com/api/v3/simple/price?ids"
       f"={ids_param}&vs_currencies=usd")


def parsing_data(data):
    """ GET запрос к coingecko для криптовалют в CRYPTO_MAP """
    result = []
    for coin_id, display_name in CRYPTO_MAP.items():
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


try:
    # Установка таймаута на случай проблем со связью
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        prices = response.json()
        print(parsing_data(prices))
    else:
        print(f"Ошибка API: код {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка сети: {str(e)}")
