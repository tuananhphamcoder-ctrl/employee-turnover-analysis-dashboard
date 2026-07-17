# Hướng dẫn chạy dự án

## 1. Mở thư mục trong VS Code

Mở thư mục:

```text
employee-turnover-analysis-dashboard
```

## 2. Tạo môi trường Python

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.venv\Scripts\Activate.ps1
```

## 3. Cài thư viện

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Chạy kiểm thử

```powershell
python -m pytest
```

## 5. Chạy dashboard

```powershell
python -m streamlit run app.py
```

Mở:

```text
http://localhost:8501
```

## 6. Kiểm tra các bộ lọc

- Department
- Shift
- Manager
- Overtime

## 7. Kiểm tra các tab

- Turnover analysis
- Manager and shift
- Headcount forecast
- Employee data
