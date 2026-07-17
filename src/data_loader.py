from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_employee_data(
    path: str | Path,
) -> pd.DataFrame:
    dataframe = pd.read_csv(
        path,
        parse_dates=[
            "hire_date",
            "exit_date",
        ],
    )

    return dataframe
