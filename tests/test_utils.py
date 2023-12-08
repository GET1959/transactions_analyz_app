import os
from datetime import datetime

import pandas as pd
import requests

from src.utils import (get_card_info, get_currency, get_stock,
                       get_top_transactions, select_table,
                       time_greeting,)


URL_CUR = "https://www.cbr-xml-daily.ru/daily_json.js"
URL_STOCK = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
DICT_GREETING = {
    "greeting": "Доброе утро" * (4 <= datetime.now().hour < 11)
    + "Добрый день" * (11 <= datetime.now().hour < 16)
    + "Добрый вечер" * (16 <= datetime.now().hour < 23)
    + "Доброй ночи" * (datetime.now().hour == 23)
    + "Доброй ночи" * (0 <= datetime.now().hour < 4)
}


def test_time_greeting():
    assert time_greeting() == DICT_GREETING


cur_dir = os.path.dirname(os.path.dirname(__file__))
selected_df = pd.read_csv(cur_dir + "/data/selected.csv")
selected_df = selected_df.drop(["Unnamed: 0"], axis=1)
selected_df["last_digits"] = selected_df["last_digits"].astype("str")


def test_select_table():
    assert select_table("operations.xls", "31.12.2021").equals(selected_df)


def test_get_card_info():
    assert get_card_info(select_table("operations.xls", "20.07.2021")) == {
        "cards": [
            {"last_digits": "4556", "total_spent": 1300.0, "cashback": 13.0},
            {"last_digits": "7197", "total_spent": 23087.97, "cashback": 608.0},
        ]
    }
    assert get_card_info(select_table("operations.xls", "31.12.2021")) == {
        "cards": [
            {"last_digits": "4556", "total_spent": 4075.7000000000003, "cashback": 224.0},
            {"last_digits": "5091", "total_spent": 15393.33, "cashback": 556.0},
            {"last_digits": "7197", "total_spent": 24576.63, "cashback": 639.0},
        ]
    }


def test_get_top_transactions():
    assert get_top_transactions(select_table("operations.xls", "20.07.2021")) == {
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
        ]
    }
    assert get_top_transactions(select_table("operations.xls", "31.12.2021")) == {
        "top_transactions": [
            {
                "date": "30.12.2021",
                "amount": 174000.0,
                "category": "Пополнения",
                "description": "Пополнение через Газпромбанк",
            },
            {
                "date": "23.12.2021",
                "amount": 20000.0,
                "category": "Другое",
                "description": "Иван С.",
            },
            {
                "date": "02.12.2021",
                "amount": 5510.8,
                "category": "Каршеринг",
                "description": "Ситидрайв",
            },
            {
                "date": "30.12.2021",
                "amount": 5046.0,
                "category": "Пополнения",
                "description": "Пополнение через Газпромбанк",
            },
            {
                "date": "05.12.2021",
                "amount": 3500.0,
                "category": "Пополнения",
                "description": "Внесение наличных через банкомат Тинькофф",
            },
        ]
    }


data = requests.get(URL_CUR).json()
data_dict = {currency: data["Valute"][currency]["Value"] for currency in data["Valute"]}


def test_get_currency():
    assert get_currency(URL_CUR, ["USD", "EUR"]) == {
        "currency_rates": [
            {"currency": "USD", "rate": data_dict["USD"]},
            {"currency": "EUR", "rate": data_dict["EUR"]},
        ]
    }
    assert get_currency(URL_CUR, ["AUD", "GBP"]) == {
        "currency_rates": [
            {"currency": "AUD", "rate": data_dict["AUD"]},
            {"currency": "GBP", "rate": data_dict["GBP"]},
        ]
    }


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


def test_get_stock():
    assert get_stock(URL_STOCK, ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) == {
        "stock_prices": [
            {"stock": "AAPL", "price": response_aapl.json()["Global Quote"]["05. price"]},
            {"stock": "AMZN", "price": response_amzn.json()["Global Quote"]["05. price"]},
            {"stock": "GOOGL", "price": response_googl.json()["Global Quote"]["05. price"]},
            {"stock": "MSFT", "price": response_msft.json()["Global Quote"]["05. price"]},
            {"stock": "TSLA", "price": response_tsla.json()["Global Quote"]["05. price"]},
        ]
    }
