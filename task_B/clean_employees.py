import sys, pandas as pd, numpy as np
from datetime import datetime
from pathlib import Path

def standardize_name(name):
    if pd.isna(name): return ""
    return str(name).title()

def normalize_date(date_value):
    try:
        return pd.to_datetime(date_value, errors="coerce").strftime("%Y-%m-%d")
    except Exception:
        return None

def clean_salary(value):
    if pd.isna(value): return np.nan
    value = str(value).replace(",", "").replace("₹", "").replace("$", "").strip()
    try:
        return float(value)
    except:
        return np.nan

def clean_employees(input_path, output_path):
    df = pd.read_excel(input_path)

    df["FullName"] = df["FullName"].apply(standardize_name)
    df["JoiningDate"] = df["JoiningDate"].apply(normalize_date)
    df["Salary"] = df["Salary"].apply(clean_salary)
    df["Email"] = df["Email"].fillna("not_provided@company.com")

    today = pd.Timestamp.now()
    df["Experience_Years"] = df["JoiningDate"].apply(
        lambda d: round((today - pd.Timestamp(d)).days / 365, 2)
        if pd.notna(d) else np.nan
    )

    df.to_excel(output_path, index=False)
    print(f"✅ Cleaned file saved at {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_employees.py input.xlsx output.xlsx")
    else:
        clean_employees(sys.argv[1], sys.argv[2])

#command to run the file: python clean_employees.py employees.xlsx employees_cleaned.xlsx
import pandas as pd

df = pd.read_excel("employees_cleaned.xlsx")
print(df.head())

