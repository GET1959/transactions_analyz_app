import glob
import os

import pandas as pd
import pytest

from src.reports import get_costs


@pytest.mark.parametrize(
    "file, cat, date, expected",
    [
        (
            "operations.xls",
            "Жд билеты",
            "31.12.2021",
            {
                "Жд билеты": [
                    {"date": "30.12.2021", "costs": 1411.0},
                    {"date": "30.12.2021", "costs": 1411.0},
                    {"date": "07.12.2021", "costs": 838.0},
                    {"date": "03.10.2021", "costs": 93.0},
                    {"date": "03.10.2021", "costs": 93.0},
                ]
            },
        ),
    ],
)
def test_get_costs(file, cat, date, expected):
    filename = glob.glob("*_costs.xlsx")[0]
    if os.path.exists(filename):
        os.remove(filename)

    assert get_costs(file, cat, date) == expected
    df = pd.read_excel("zhd _costs.xlsx")
    df = df.drop("Unnamed: 0", axis=1)
    df_dict = df.to_dict("records")
    assert df_dict == expected["Жд билеты"]
