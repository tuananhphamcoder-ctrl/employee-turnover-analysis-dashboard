from __future__ import annotations

import pandas as pd
import streamlit as st

from src.charts import (
    attrition_bar_chart,
    monthly_exit_chart,
    risk_factor_scatter,
)
from src.data_loader import (
    load_employee_data,
)
from src.forecasting import (
    basic_headcount_forecast,
)
from src.metrics import (
    calculate_kpis,
    group_attrition,
)


st.set_page_config(
    page_title=(
        "Employee Turnover Analysis"
    ),
    page_icon="👥",
    layout="wide",
)

st.title(
    "Employee Turnover Analysis Dashboard"
)
st.caption(
    "Analyze employee attrition by department, "
    "tenure, shift, manager, overtime, and "
    "workforce trends using synthetic data."
)

with st.sidebar:
    st.header("1. Choose data")

    source = st.radio(
        "Data source",
        [
            "Use sample data",
            "Upload my CSV",
        ],
    )

    uploaded_file = None

    if source == "Upload my CSV":
        uploaded_file = st.file_uploader(
            "Upload employee CSV",
            type=["csv"],
        )

if source == "Use sample data":
    dataframe = load_employee_data(
        "data/raw/employee_turnover_1000.csv"
    )
else:
    if uploaded_file is None:
        st.info(
            "Upload a CSV file to begin."
        )
        st.stop()

    dataframe = pd.read_csv(
        uploaded_file,
        parse_dates=[
            "hire_date",
            "exit_date",
        ],
    )

with st.sidebar:
    st.header("2. Filters")

    departments = sorted(
        dataframe["department"]
        .dropna()
        .unique()
        .tolist()
    )
    shifts = sorted(
        dataframe["shift"]
        .dropna()
        .unique()
        .tolist()
    )
    managers = sorted(
        dataframe["manager_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_departments = st.multiselect(
        "Department",
        departments,
        default=departments,
    )
    selected_shifts = st.multiselect(
        "Shift",
        shifts,
        default=shifts,
    )
    selected_managers = st.multiselect(
        "Manager",
        managers,
        default=managers,
    )
    selected_overtime = st.multiselect(
        "Overtime",
        ["Yes", "No"],
        default=["Yes", "No"],
    )

filtered = dataframe[
    dataframe["department"].isin(
        selected_departments
    )
    & dataframe["shift"].isin(
        selected_shifts
    )
    & dataframe["manager_name"].isin(
        selected_managers
    )
    & dataframe["overtime_flag"].isin(
        selected_overtime
    )
].copy()

if filtered.empty:
    st.warning(
        "No employees match the selected filters."
    )
    st.stop()

kpis = calculate_kpis(
    filtered
)

first_row = st.columns(4)
second_row = st.columns(2)

first_row[0].metric(
    "Total Employees",
    f"{kpis['total_employees']:,}",
)
first_row[1].metric(
    "Active Employees",
    f"{kpis['active_employees']:,}",
)
first_row[2].metric(
    "Employees Exited",
    f"{kpis['attrited_employees']:,}",
)
first_row[3].metric(
    "Attrition Rate",
    f"{kpis['attrition_rate']:.1%}",
)

second_row[0].metric(
    "Average Tenure",
    f"{kpis['average_tenure']:.1f} years",
)
second_row[1].metric(
    "Average Monthly Overtime",
    (
        f"{kpis['average_overtime_hours']:.1f} "
        "hours"
    ),
)

(
    tab_overview,
    tab_manager,
    tab_forecast,
    tab_data,
) = st.tabs(
    [
        "Turnover analysis",
        "Manager and shift",
        "Headcount forecast",
        "Employee data",
    ]
)

with tab_overview:
    department_summary = (
        group_attrition(
            filtered,
            "department",
        )
    )
    tenure_work = filtered.copy()
    tenure_work["tenure_band"] = pd.cut(
        tenure_work["tenure_years"],
        bins=[0, 1, 3, 5, float("inf")],
        labels=[
            "< 1 year",
            "1–3 years",
            "3–5 years",
            "5+ years",
        ],
        right=False,
    )
    tenure_summary = group_attrition(
        tenure_work,
        "tenure_band",
    )

    chart_1, chart_2 = st.columns(2)

    with chart_1:
        st.plotly_chart(
            attrition_bar_chart(
                department_summary,
                "department",
                "Attrition Rate by Department",
            ),
            use_container_width=True,
        )

    with chart_2:
        st.plotly_chart(
            attrition_bar_chart(
                tenure_summary,
                "tenure_band",
                "Attrition Rate by Tenure",
            ),
            use_container_width=True,
        )

    st.plotly_chart(
        monthly_exit_chart(
            filtered
        ),
        use_container_width=True,
    )

    st.plotly_chart(
        risk_factor_scatter(
            filtered
        ),
        use_container_width=True,
    )

with tab_manager:
    manager_summary = (
        group_attrition(
            filtered,
            "manager_name",
        )
        .sort_values(
            "attrition_rate",
            ascending=False,
        )
        .head(12)
    )

    shift_summary = group_attrition(
        filtered,
        "shift",
    )
    overtime_summary = group_attrition(
        filtered,
        "overtime_flag",
    )

    manager_chart, shift_chart = (
        st.columns(2)
    )

    with manager_chart:
        st.plotly_chart(
            attrition_bar_chart(
                manager_summary,
                "manager_name",
                "Managers with Highest Attrition",
            ),
            use_container_width=True,
        )

    with shift_chart:
        st.plotly_chart(
            attrition_bar_chart(
                shift_summary,
                "shift",
                "Attrition Rate by Shift",
            ),
            use_container_width=True,
        )

    st.plotly_chart(
        attrition_bar_chart(
            overtime_summary,
            "overtime_flag",
            "Attrition Rate by Overtime",
        ),
        use_container_width=True,
    )

with tab_forecast:
    history = pd.read_csv(
        "data/raw/monthly_headcount_history.csv",
        parse_dates=["month"],
    )
    forecast = basic_headcount_forecast(
        history,
        forecast_months=6,
    )

    actual = history[
        ["month", "headcount"]
    ].rename(
        columns={"headcount": "Headcount"}
    )
    actual["Series"] = "Actual"

    predicted = forecast[
        ["month", "forecast_headcount"]
    ].rename(
        columns={
            "forecast_headcount": "Headcount"
        }
    )
    predicted["Series"] = "Forecast"

    chart_data = pd.concat(
        [actual, predicted],
        ignore_index=True,
    )

    import plotly.express as px

    figure = px.line(
        chart_data,
        x="month",
        y="Headcount",
        color="Series",
        markers=True,
        title=(
            "Actual and Forecast Headcount"
        ),
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )

    st.dataframe(
        forecast,
        use_container_width=True,
    )

with tab_data:
    st.dataframe(
        filtered,
        use_container_width=True,
        height=520,
    )

    st.download_button(
        "Download filtered employee data",
        data=filtered.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name=(
            "filtered_employee_turnover_data.csv"
        ),
        mime="text/csv",
    )
