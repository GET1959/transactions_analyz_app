import json

from src.utils import get_top_transactions, get_stock
from src.utils import get_card_info, get_currency, select_table, time_greeting


URL_CUR = "https://www.cbr-xml-daily.ru/daily_json.js"
CUR_LIST = ["USD", "EUR"]
URL_STOCK = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
USER_STOCK_LIST = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def get_brief_report(file: str) -> str:
    """
    Функция принимает на вход файл в формате excel и записывает в json-файл приветствие,
    краткие данные по карте, топ-5 транзакций, курсы основных валют, котировки акций.
    :param file:
    :return dict_report:
    """
    report_dict = (
        time_greeting()
        | get_card_info(select_table(file, "20.07.2021"))
        | get_top_transactions(select_table(file, "20.07.2021"))
        | get_currency(URL_CUR, CUR_LIST)
        | get_stock(URL_STOCK, USER_STOCK_LIST))
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_dict, f, indent="\t")
    return report_dict
