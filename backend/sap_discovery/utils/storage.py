"""Local file storage utility."""

import os
import uuid
from typing import List, Dict
import pandas as pd
from fastapi import UploadFile
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)

# Base upload directory (relative to project root, not backend/)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads")


def get_upload_path(session_id: str, filename: str) -> str:
    """Get upload path for a file.

    Args:
        session_id: User session ID
        filename: Original filename

    Returns:
        Full path to save file
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, filename)


async def save_file(file: UploadFile, session_id: str) -> str:
    """Save uploaded file to local storage.

    Args:
        file: Uploaded file object
        session_id: User session ID

    Returns:
        File path where file was saved
    """
    try:
        # Sanitize filename
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = get_upload_path(session_id, filename)

        # Read and save file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        logger.info(f"File saved: {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise


def validate_excel(filename: str) -> bool:
    """Validate file is an Excel file.

    Args:
        filename: Name of the file

    Returns:
        True if valid Excel file
    """
    return filename.endswith(('.xlsx', '.xls'))


def parse_excel_processes(file_path: str) -> List[Dict[str, str]]:
    """Parse business processes from an Excel file.

    Extracts process information from Excel file with flexible column mapping.
    Supports various column name variations for common fields.

    Args:
        file_path: Path to the Excel file

    Returns:
        List of process dictionaries with extracted fields

    Raises:
        ValueError: If file cannot be parsed or is invalid format
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        processes = []

        logger.info(f"Parsing Excel file with {len(df)} rows and columns: {list(df.columns)}")

        # Extract processes from each row
        for _, row in df.iterrows():
            process = {}

            # Try different column name variations
            for col in df.columns:
                col_lower = col.lower()

                # Process name/title
                if 'process' in col_lower and ('name' in col_lower or 'title' in col_lower):
                    process['name'] = str(row[col]) if pd.notna(row[col]) else ""

                # Process ID
                elif 'id' in col_lower:
                    process['id'] = str(row[col]) if pd.notna(row[col]) else ""

                # Description
                elif 'description' in col_lower or 'desc' in col_lower:
                    process['description'] = str(row[col]) if pd.notna(row[col]) else ""

                # Category/Type
                elif 'category' in col_lower or 'type' in col_lower:
                    process['category'] = str(row[col]) if pd.notna(row[col]) else ""

            # Only include rows with at least a name
            if 'name' in process and process['name'].strip():
                processes.append(process)

        logger.info(f"Extracted {len(processes)} valid processes from Excel")
        return processes

    except Exception as e:
        logger.error(f"Failed to parse Excel file: {e}")
        raise ValueError(f"Failed to parse Excel file: {str(e)}")