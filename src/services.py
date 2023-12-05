import pandas as pd
import os
import json


def get_cashback(file: str, year: int, month: int) -> dict:
    """
    Функция принимает на вход данные в виде файла excel, год, месяц и
    формирует ответ в виде файла json с суммой кэшбэка по каждой
    категории для заданного года и месяца
    """
    cur_dir = os.path.dirname(os.path.dirname(__file__))
    path_to_file = os.path.join(cur_dir + "/data/" + file)
    df = pd.read_excel(path_to_file)
    df.dropna(subset=["Номер карты", "Категория"], inplace=True)
    df.fillna({"Кэшбэк": 0})
    df["cashback"] = round(df["Бонусы (включая кэшбэк)"] + abs(df["Сумма платежа"] * 0.01)) * (
            df["Сумма платежа"] <= 100
    )
    df["date"] = pd.to_datetime(df["Дата платежа"], dayfirst=True, format="%d.%m.%Y")
    df["year"] = pd.DatetimeIndex(df["date"]).year
    df["month"] = pd.DatetimeIndex(df["date"]).month
    df_cashback = df.groupby(["Категория", "year", "month"])["cashback"].sum().reset_index()
    df_targ = df_cashback.loc[
        (df_cashback["year"] == year) & (df_cashback["month"] == month)
        ].sort_values(by=["cashback"], ascending=False)
    cashback_dict = {k: v for k, v in zip(df_targ["Категория"], df_targ["cashback"])}
    with open("cashback.json", "w", encoding="utf-8") as f:
        json.dump(cashback_dict, f, ensure_ascii=False, indent="\t")
    return cashback_dict
