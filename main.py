from __future__ import annotations
from database.dbconn import fetch_result, sql_loader
from utilities import CSV_FOLDER
import pandas as pd
from pathlib import Path
from typing import Any


def employee_360_dataset() -> None:
    sql = sql_loader("employee_360_dataset.sql")
    rows = fetch_result(sql)
    df = pd.DataFrame(rows)
    df.to_excel(Path("csv_files") / "employee_360_dataset.xlsx")


def main() -> None:
    employee_360_dataset()


if __name__ == "__main__":
    main()
