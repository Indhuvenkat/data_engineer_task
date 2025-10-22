import pytest
import os
from parser import parse_file, process_directory

def test_parse_csv(tmp_path):
    # Create a temporary CSV
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("a,b\n1,2\n3,4")
    
    summary = parse_file(str(csv_file))
    assert summary["rows"] == 2
    assert "a" in summary["schema"]
    assert "b" in summary["schema"]

def test_process_directory(tmp_path):
    # Create CSV and JSON
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("a,b\n1,2\n3,4")
    
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"a":5,"b":6}]')
    
    report = process_directory(str(tmp_path))
    assert report["files_processed"] == 2
    assert report["total_rows"] == 3
