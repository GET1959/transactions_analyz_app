import os
import requests
import pandas as pd
import re
from datetime import datetime


def time_greeting() -> dict:
    """
    Функция возвращает приветствие в соответствии с текущим временем.
    :return greeting:
    """
    if 4 <= datetime.now().hour < 11:
        return {"greeting": "Доброе утро"}
    elif 11 <= datetime.now().hour < 16:
        return {"greeting": "Добрый день"}
    elif 16 <= datetime.now().hour < 23:
        return {"greeting": "Добрый вечер"}
    else:
        return {"greeting": "Доброй ночи"}


def select_table(file: str, input_date: str) -> pd.DataFrame:
    """
    Функция принимает на вход файл в формате excel и дату в формате str. Возвращает фрейм данных, относящихся к периоду
    от начала месяца до полученной даты.
    :param file:
    :param input_date:
    :return df_selected:
    """
    cur_dir = os.path.dirname(os.path.dirname(__file__))
    path_to_file = os.path.join(cur_dir + "/data/" + file)
    df = pd.read_excel(path_to_file)
    df = df.dropna(subset=['Номер карты'])
    df['Кэшбэк'] = df['Кэшбэк'].fillna(0)
    df.rename(columns={'Дата платежа': 'date', 'Категория': 'category', 'Описание': 'description'}, inplace=True)
    df['amount'] = abs(df['Сумма операции'])
    df['last_digits'] = [re.findall(r'\d+', string)[0] for string in df['Номер карты']]
    df['total_spent'] = abs(df['Сумма операции']) * (df['Сумма операции'] < 0)
    df['cashback'] = round(
        df['Бонусы (включая кэшбэк)'] + (abs(df['Сумма платежа']) * 0.01) * (df['Сумма платежа'] <= -100))
    start = '01' + input_date[2:]

    df['date_date'] = pd.to_datetime(df['date'], dayfirst=True)
    start_date = datetime.strptime(start, "%d.%m.%Y")
    end_date = datetime.strptime(input_date, "%d.%m.%Y")

    mask = (df['date_date'] >= start_date) & (df['date_date'] <= end_date)
    df_selected = df.loc[mask].sort_values('amount', axis=0, ascending=False)
    return df_selected

#print(select_table('operations.xls', '20.07.2021'))

def get_card_info(df: pd.DataFrame) -> dict:
    df_cards = df[['last_digits', 'total_spent', 'cashback']].groupby('last_digits').sum().reset_index()
    dict_cards = {'cards': [dict(row) for index, row in df_cards.iterrows()]}

    return dict_cards


URL_CUR = "https://www.cbr-xml-daily.ru/daily_json.js"
CUR_LIST = ['USD', 'EUR']
def get_currency(url_cur: str, cur_list: list) -> dict:
    """
    Функция принимает url для получения курса валюты по API и список валют для запроса
    и возврацает словарь, где ключ - валюта, значание - ее курс.
    :param url_cur:
    :param cur_list:
    :return currency_dict:
    """
    response = requests.get(url_cur)
    if response.status_code == 200:
        data = response.json()
        data_dict = {currency: data["Valute"][currency]["Value"] for currency in data["Valute"]}
        cur_dict = {"currency_rates": [{"currency": cur, "rate": data_dict[cur]} for cur in data_dict if
                                       cur in cur_list]}
        return cur_dict



print(time_greeting() | get_card_info(select_table('operations.xls', '20.07.2021')) | get_currency(URL_CUR, CUR_LIST))


URL_STOCK = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
USER_STOCK_LIST = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def get_stock(url: str, users_stock_list: list) -> dict:
    """
    Функция принимает на вход url для запроса по API и список акций для получения котировок и
    возвращает словарь с котировками.
    """
    alpha_token = os.getenv('ALPHA_KEY')

    stock_dict = {"stock_prices": []}
    for symbol in users_stock_list:
        response = requests.get(f"{url}&symbol={symbol}&apikey={alpha_token}")
        if response.status_code == 200:
            data = response.json()
            stock_dict["stock_prices"].append({"stock": data["Global Quote"]["01. symbol"],
                                               "price": data["Global Quote"]["05. price"]})

    return stock_dict

