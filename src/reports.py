import os
from datetime import datetime
from functools import wraps
from typing import Callable

import pandas as pd
from dateutil.relativedelta import relativedelta
from transliterate import translit


def excel_writer(func: Callable) -> Callable:
    """
    Записывает в файл формата excel результат задекорированной функции.
    Имя файла формирует из первых букв названия категории.
    :param func:
    :return function:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_dict = func(*args, **kwargs)
        df_category = pd.DataFrame.from_dict(list(func_dict.values())[0])
        file_name = (
            translit(list(func_dict.keys())[0].lower()[:3], language_code="ru", reversed=True)
            + "_costs.xlsx"
        )
        df_category.to_excel(file_name)
        return func_dict

    return wrapper


@excel_writer
def get_costs(
    file: str, users_category: str, users_date: str = datetime.now().strftime("%d.%m.%Y")
) -> dict:
    """
    Функция принимает на вход датафрейм с транзакциями,
    название категории,опциональную дату.
    Если дата не передана, то берется текущая дата.
    Функция возвращает траты по заданной категории за последние 3 месяца от переданной даты.
    Если история операций на чинается позднее, чем за 3 месяца от переданной даты,
    траты возвращаются от начала истории.
    """
    cur_dir = os.path.dirname(os.path.dirname(__file__))
    path_to_file = os.path.join(cur_dir + "/data/" + file)
    df = pd.read_excel(path_to_file)
    df.dropna(subset=["Номер карты", "Категория"], inplace=True)
    df.fillna({"Кэшбэк": 0}, inplace=True)
    df["costs"] = round(abs(df["Сумма платежа"])) * (df["Сумма платежа"] < 0)
    df["date"] = pd.to_datetime(df["Дата платежа"], dayfirst=True, format="%d.%m.%Y")
    df = df.loc[df["costs"] > 0]
    list_cat = list(df["Категория"])
    for i in range(len(list_cat)):
        if "/" in list_cat[i]:
            list_cat[i] = list_cat[i].replace("/", "")
    df["Категория"] = list_cat
    df_targ = df.loc[:, ["Категория", "costs", "date"]]
    earliest_date = df_targ["date"].min()
    date_3_month_behind = pd.to_datetime(
        users_date, dayfirst=True, format="%d.%m.%Y"
    ) - relativedelta(months=3)
    date_from = max(earliest_date, date_3_month_behind)
    df_result = df_targ.loc[(df_targ["date"] <= users_date) & (df_targ["date"] > date_from)]
    df_targ = df_result.loc[(df_result["Категория"] == users_category)].loc[:, ["date", "costs"]]
    df_targ["date"] = df_targ["date"].dt.strftime("%d.%m.%Y")
    return {users_category: df_targ.to_dict(orient="records")}
print(get_costs('operations.xls', 'Дом и ремонт', '31.12.2021'))