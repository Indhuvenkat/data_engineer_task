import pytest
import pandas as pd
import numpy as np
from clean_employees import (
    standardize_name,
    normalize_date,
    clean_salary,
    calculate_experience
)
from datetime import datetime

# -----------------------------
# Test standardize_name
# -----------------------------
def test_standardize_name_normal():
    assert standardize_name("john DOE") == "John Doe"

def test_standardize_name_empty():
    assert standardize_name(None) == ""

# -----------------------------
# Test normalize_date
# -----------------------------
def test_normalize_date_formats():
    # Different formats
    assert normalize_date("12/03/2021") == "2021-12-03" or "2021-03-12"
    assert normalize_date("March 12, 2021") == "2021-03-12"
    assert normalize_date("2021-03-12") == "2021-03-12"

def test_normalize_date_invalid():
    assert normalize_date("invalid") is None
    assert normalize_date(None) is None

# -----------------------------
# Test clean_salary
# -----------------------------
def test_clean_salary_normal():
    assert clean_salary("₹10,000") == 10000.0
    assert clean_salary("$5,500") == 5500.0
    assert clean_salary("1000") == 1000.0

def test_clean_salary_invalid():
    assert np.isnan(clean_salary("abc"))
    assert np.isnan(clean_salary(None))

# -----------------------------
# Test calculate_experience
# -----------------------------
def test_calculate_experience_valid():
    today = pd.Timestamp.now()
    joining_date = (today - pd.Timedelta(days=365*3)).strftime("%Y-%m-%d")
    experience = calculate_experience(joining_date)
    assert 2.9 <= experience <= 3.1  # approximately 3 years

def test_calculate_experience_invalid():
    assert np.isnan(calculate_experience(None))
    assert np.isnan(calculate_experience("invalid"))
