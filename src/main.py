from typing import Any

from reports import get_costs
from services import get_cashback
from views import get_brief_report


FILE_NAME = "operations.xls"
USERS_DATE = input("Введите дату в формате DD.MM.YYYY")
USERS_CAT = input("Категория")


def main() -> Any:
    """
    Функция запускает приложение и возвращает результат трех функций:
    краткий отчет по картам с курсами валют и основных акций,
    результаты по кэшбэку,
    траты по категории.
    :return report_dict, cashback_dict, category_dict:
    """
    return (
        get_brief_report(FILE_NAME),
        get_cashback(FILE_NAME, int(USERS_DATE[6:]), int(USERS_DATE[3:5])),
        get_costs(FILE_NAME, USERS_CAT, USERS_DATE),
    )


if __name__ == "__main__":
    main()
