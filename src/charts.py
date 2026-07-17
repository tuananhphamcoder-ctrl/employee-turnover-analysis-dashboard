from __future__ import annotations

import pandas as pd
import plotly.express as px


def attrition_bar_chart(
    summary: pd.DataFrame,
    category_column: str,
    title: str,
):
    return px.bar(
        summary,
        x=category_column,
        y="attrition_rate",
        text_auto=".1%",
        title=title,
        labels={
            "attrition_rate": "Attrition Rate",
        },
    )


def monthly_exit_chart(
    dataframe: pd.DataFrame,
):
    exits = (
        dataframe.loc[
            dataframe["attrition"] == "Yes"
        ]
        .dropna(
            subset=["exit_date"]
        )
        .assign(
            month=lambda frame: (
                frame["exit_date"]
                .dt.to_period("M")
                .dt.to_timestamp()
            )
        )
        .groupby(
            "month",
            as_index=False,
        )
        .size()
        .rename(
            columns={"size": "exits"}
        )
    )

    return px.line(
        exits,
        x="month",
        y="exits",
        markers=True,
        title="Monthly Employee Exits",
    )


def risk_factor_scatter(
    dataframe: pd.DataFrame,
):
    return px.scatter(
        dataframe,
        x="avg_monthly_overtime_hours",
        y="absenteeism_days_12m",
        color="attrition",
        size="tenure_years",
        hover_data=[
            "employee_id",
            "department",
            "shift",
            "job_satisfaction",
        ],
        title=(
            "Overtime, Absence, Tenure, "
            "and Attrition"
        ),
    )
