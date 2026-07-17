import pandas as pd

from src.forecasting import (
    basic_headcount_forecast,
)


def test_basic_headcount_forecast():
    history = pd.DataFrame(
        {
            "month": pd.date_range(
                "2025-01-31",
                periods=6,
                freq="ME",
            ),
            "headcount": [
                100,
                101,
                102,
                104,
                105,
                106,
            ],
            "net_change": [
                1,
                1,
                1,
                2,
                1,
                1,
            ],
        }
    )

    forecast = basic_headcount_forecast(
        history,
        forecast_months=3,
    )

    assert len(forecast) == 3
    assert forecast.iloc[0][
        "forecast_headcount"
    ] > 106
