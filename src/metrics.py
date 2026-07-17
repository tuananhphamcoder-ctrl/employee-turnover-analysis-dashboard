from __future__ import annotations

import pandas as pd


def calculate_kpis(
    dataframe: pd.DataFrame,
) -> dict[str, float]:
    total_employees = len(dataframe)
    attrited = int(
        (dataframe["attrition"] == "Yes").sum()
    )
    active = total_employees - attrited

    return {
        "total_employees": total_employees,
        "active_employees": active,
        "attrited_employees": attrited,
        "attrition_rate": (
            attrited / total_employees
            if total_employees
            else 0
        ),
        "average_tenure": float(
            dataframe["tenure_years"].mean()
        ),
        "average_overtime_hours": float(
            dataframe[
                "avg_monthly_overtime_hours"
            ].mean()
        ),
    }


def group_attrition(
    dataframe: pd.DataFrame,
    group_column: str,
) -> pd.DataFrame:
    summary = (
        dataframe
        .groupby(
            group_column,
            dropna=False,
        )
        .agg(
            employee_count=(
                "employee_id",
                "count",
            ),
            attrition_count=(
                "attrition",
                lambda values: (
                    values == "Yes"
                ).sum(),
            ),
        )
        .reset_index()
    )

    summary["attrition_rate"] = (
        summary["attrition_count"]
        / summary["employee_count"]
    )

    return summary
