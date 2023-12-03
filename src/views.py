import json

from src.utils import time_greeting, select_table, get_card_info, get_currency, get_stock



URL_CUR = "https://www.cbr-xml-daily.ru/daily_json.js"
CUR_LIST = ['USD', 'EUR']
URL_STOCK = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
USER_STOCK_LIST = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

def get_brief_report(file: str) -> dict:
    report_dict = (time_greeting() | get_card_info(select_table(file, '20.07.2021'))
                   | get_currency(URL_CUR, CUR_LIST) | get_stock(URL_STOCK, USER_STOCK_LIST))
    with open('report.json', 'w', encoding='utf-8') as f:
        json.dump(report_dict, f, ensure_ascii=False, indent='\t')
    report_json = json.dumps(report_dict, ensure_ascii=False)
    return report_json


print(get_brief_report('operations.xls'))
