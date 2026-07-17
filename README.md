# Employee Turnover Analysis Dashboard

A portfolio-ready HR analytics project using Python, Pandas, Plotly, Streamlit,
and Excel reporting to analyze employee attrition and workforce trends.

## Business questions

- What is the overall employee attrition rate?
- Which departments have the highest turnover?
- Is turnover higher among employees with short tenure?
- How do shift and overtime relate to attrition?
- Which managers have the highest attrition rates?
- How is monthly headcount changing?
- What is the basic six-month headcount forecast?

## Synthetic dataset

| Item | Value |
|---|---:|
| Employee records | 1,000 |
| Active employees | 823 |
| Exited employees | 177 |
| Attrition rate | 17.7% |
| Departments | 7 |
| Managers | 15 |
| Headcount history | 24 months |
| Forecast | 6 months |

All data is synthetic. No real company or employee information is included.

## Features

- Filters by department, shift, manager, and overtime
- KPI cards for total employees, active employees, exits, attrition rate,
  average tenure, and overtime
- Attrition by department
- Attrition by tenure
- Attrition by shift
- Attrition by manager
- Attrition by overtime
- Monthly exit trend
- Basic headcount forecast
- CSV download

## Project structure

```text
employee-turnover-analysis-dashboard/
├── app.py
├── data/
│   ├── raw/
│   │   ├── employee_turnover_1000.csv
│   │   ├── employee_turnover_1000.xlsx
│   │   ├── monthly_headcount_history.csv
│   │   └── headcount_forecast_6_months.csv
│   └── reference/
│       └── data_dictionary.csv
├── output/
│   └── employee_turnover_analysis_report.xlsx
├── screenshots/
├── src/
├── tests/
├── requirements.txt
└── README.md
```

## Run locally

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
python -m streamlit run app.py
```

## Deploy to Streamlit Community Cloud

- Repository: `employee-turnover-analysis-dashboard`
- Branch: `main`
- Main file path: `app.py`

## Next machine-learning phase

The first version focuses on business analysis. A later version can add:

- Logistic Regression
- Random Forest
- Recall for the attrition class
- Feature importance
- Synthetic high-risk employee list
