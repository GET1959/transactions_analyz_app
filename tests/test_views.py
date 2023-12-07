import json
import os

import pytest
import requests

from src.views import get_brief_report


URL_CUR = "https://www.cbr-xml-daily.ru/daily_json.js"
URL_STOCK = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
data = requests.get(URL_CUR).json()
data_dict = {currency: data["Valute"][currency]["Value"] for currency in data["Valute"]}
alpha_token = os.getenv("ALPHA_KEY")
response_aapl = requests.get(
    f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={alpha_token}"
)
response_amzn = requests.get(
    f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AMZN&apikey={alpha_token}"
)
response_googl = requests.get(
    f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GOOGL&apikey={alpha_token}"
)
response_msft = requests.get(
    f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey={alpha_token}"
)
response_tsla = requests.get(
    f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=TSLA&apikey={alpha_token}"
)


@pytest.mark.parametrize(
    "file, expected",
    [
        (
            "operations.xls",
            {
                "greeting": "Добрый вечер",
                "cards": [
                    {"last_digits": "4556", "total_spent": 1300.0, "cashback": 13.0},
                    {"last_digits": "7197", "total_spent": 23087.97, "cashback": 608.0},
                ],
                "top_transactions": [
                    {
                        "date": "14.07.2021",
                        "amount": 8400.0,
                        "category": "Дом и ремонт",
                        "description": "Magazin Mebel",
                    },
                    {
                        "date": "14.07.2021",
                        "amount": 2569.16,
                        "category": "Супермаркеты",
                        "description": "Дикси",
                    },
                    {
                        "date": "05.07.2021",
                        "amount": 2122.24,
                        "category": "Другое",
                        "description": "Петроэлектросбыт",
                    },
                    {
                        "date": "19.07.2021",
                        "amount": 1759.96,
                        "category": "Супермаркеты",
                        "description": "Магнит",
                    },
                    {
                        "date": "14.07.2021",
                        "amount": 1000.0,
                        "category": "Наличные",
                        "description": "Снятие в банкомате Тинькофф",
                    },
                ],
                "currency_rates": [
                    {"currency": "USD", "rate": data_dict["USD"]},
                    {"currency": "EUR", "rate": data_dict["EUR"]},
                ],
                "stock_prices": [
                    {"stock": "AAPL", "price": response_aapl.json()["Global Quote"]["05. price"]},
                    {"stock": "AMZN", "price": response_amzn.json()["Global Quote"]["05. price"]},
                    {"stock": "GOOGL", "price": response_googl.json()["Global Quote"]["05. price"]},
                    {"stock": "MSFT", "price": response_msft.json()["Global Quote"]["05. price"]},
                    {"stock": "TSLA", "price": response_tsla.json()["Global Quote"]["05. price"]},
                ]
            },
        )
    ],
)
def test_get_brief_report(file, expected):
    filename = "report.json"
    if os.path.exists(filename):
        os.remove(filename)
    assert get_brief_report(file) == expected
    with open("report.json") as f:
        report_dict = json.load(f)
        assert report_dict == expected
