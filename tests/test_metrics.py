import pandas as pd
import pytest

from src.metrics import (
    calculate_kpis,
    group_attrition,
)


def sample_data():
    return pd.DataFrame(
        {
            "employee_id": [
                "E1",
                "E2",
                "E3",
                "E4",
            ],
            "department": [
                "Production",
                "Production",
                "Quality",
                "Quality",
            ],
            "attrition": [
                "Yes",
                "No",
                "No",
                "Yes",
            ],
            "tenure_years": [
                1.0,
                2.0,
                3.0,
                4.0,
            ],
            "avg_monthly_overtime_hours": [
                20.0,
                10.0,
                8.0,
                12.0,
            ],
        }
    )


def test_calculate_kpis():
    result = calculate_kpis(
        sample_data()
    )

    assert result[
        "total_employees"
    ] == 4
    assert result[
        "attrited_employees"
    ] == 2
    assert result[
        "attrition_rate"
    ] == pytest.approx(0.5)


def test_group_attrition():
    summary = group_attrition(
        sample_data(),
        "department",
    )

    production = summary.loc[
        summary["department"]
        == "Production"
    ].iloc[0]

    assert production[
        "employee_count"
    ] == 2
    assert production[
        "attrition_count"
    ] == 1
