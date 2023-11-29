import pandas as pd
from datetime import datetime



def time_greeting() -> str:
    if 4 <= datetime.now().hour < 11:
        return "Доброе утро"
    elif 11 <= datetime.now().hour < 16:
        return "Добрый день"
    elif 16 <= datetime.now().hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def get_brief_report(file: str) -> dict:
    df = pd.read_excel('operations.xls')
def get_common_info():
    print(time_greeting())