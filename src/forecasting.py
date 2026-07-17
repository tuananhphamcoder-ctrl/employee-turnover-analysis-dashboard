from __future__ import annotations

import pandas as pd


def basic_headcount_forecast(
    monthly_history: pd.DataFrame,
    forecast_months: int = 6,
) -> pd.DataFrame:
    work = monthly_history.copy()
    work["month"] = pd.to_datetime(
        work["month"]
    )

    average_net_change = (
        work["net_change"]
        .tail(6)
        .mean()
    )

    current_headcount = float(
        work.iloc[-1]["headcount"]
    )
    current_month = work.iloc[-1]["month"]

    rows = []

    for step in range(
        1,
        forecast_months + 1,
    ):
        current_headcount += (
            average_net_change
        )
        forecast_month = (
            current_month
            + pd.offsets.MonthEnd(step)
        )

        rows.append(
            {
                "month": forecast_month,
                "forecast_headcount": round(
                    current_headcount
                ),
                "forecast_method": (
                    "6-month average net change"
                ),
            }
        )

    return pd.DataFrame(rows)
