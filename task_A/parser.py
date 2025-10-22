import os
import pandas as pd
import numpy as np
from .utils import setup_logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

logger = setup_logger()

def parse_file(filepath: str):
    try:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(filepath)
        elif ext == ".json":
            df = pd.read_json(filepath)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        summary = {
            "file": os.path.basename(filepath),
            "rows": len(df),
            "columns": len(df.columns),
            "schema": {},
            "numeric_summary": {},
        }

        for col in df.columns:
            dtype = df[col].dtype
            summary["schema"][col] = str(dtype)
            if np.issubdtype(dtype, np.number):
                summary["numeric_summary"][col] = {
                    "mean": float(df[col].mean(skipna=True)),
                    "min": float(df[col].min(skipna=True)),
                    "max": float(df[col].max(skipna=True))
                }

        logger.info(f"Processed: {filepath}")
        return summary

    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
        return {"file": filepath, "error": str(e)}



def process_directory(input_dir: str):
    files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith((".csv", ".json", ".xls", ".xlsx"))
    ]

    results, errors = [], []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(parse_file, f): f for f in files}
        for future in as_completed(futures):
            result = future.result()
            if "error" in result:
                errors.append(result)
            else:
                results.append(result)

    total_rows = sum(r.get("rows", 0) for r in results)
    return {
        "files_processed": len(results),
        "total_rows": total_rows,
        "errors": errors,
        "file_summaries": results
    }


def save_report(report_data, output_path):
    with open(output_path, "w") as f:
        json.dump(report_data, f, indent=4)
