"""Data loading utilities for SAP Process Discovery."""

import pandas as pd
from typing import List, Dict


def load_processes(filepath: str) -> List[Dict]:
    """Load business processes from Excel file.

    Args:
        filepath: Path to Excel file containing business processes

    Returns:
        List of process dictionaries with _row_id added
    """
    df = pd.read_excel(filepath)
    df.dropna(how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)

    processes = []
    for idx, row in df.iterrows():
        process = row.to_dict()
        process["_row_id"] = idx
        processes.append(process)

    print(f"Loaded {len(processes)} processes")
    return processes
