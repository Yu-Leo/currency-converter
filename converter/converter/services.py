import requests

API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'


def get_currencies_values() -> dict[str, float]:
    """
    :return: dictionary with currencies from API
    """
    resource = requests.get(url=API_URL).json()
    return resource.get('rates')


def convert(amount: float, from_currency: str, to_currency: str, currencies: dict) -> float:
    """
    :param amount: amount to be converted
    :param from_currency: currency of the amount to be converted
    :param to_currency: currency to convert to
    :param currencies: dictionary from API
    :return: amount in 'to_currency' currency
    """
    return round((currencies[to_currency] / currencies[from_currency]) * amount, 2)
