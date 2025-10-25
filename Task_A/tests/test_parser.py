# tests/test_parser.py
from pathlib import Path
import pandas as pd
import pytest
from fileparser.parser import parse_directory_parallel

def create_csv(path: Path, rows=5):
    df = pd.DataFrame({
        "id": range(rows),
        "value": [x * 1.1 for x in range(rows)],
        "name": [f"name{x}" for x in range(rows)],
    })
    df.to_csv(path, index=False)

def create_bad_csv(path: Path):
    with open(path, "w") as f:
        f.write("id,value\n1,2\n3\n4,5,6")

def test_parse_success(tmp_path):
    create_csv(tmp_path / "good.csv", 5)
    result = parse_directory_parallel(tmp_path)
    assert result["summary"]["total_files_processed"] == 1
    assert result["summary"]["total_rows"] == 5

def test_parse_with_error(tmp_path):
    create_bad_csv(tmp_path / "bad.csv")
    result = parse_directory_parallel(tmp_path)
    assert len(result["summary"]["errors"]) >= 1
