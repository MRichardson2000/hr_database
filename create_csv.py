import csv
from utilities import CSV_FOLDER
from pathlib import Path
import os
from typing import Any


def create_csv(
    row_input: list[dict[str, Any]],
    file_name: str,
    headers: list[str],
    folder: Path = CSV_FOLDER,
) -> None:
    full_path = os.path.join(folder, file_name)
    with open(full_path + ".csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for item in row_input:
            writer.writerow(item.values())
