"""CSV input/output handlers."""

from pathlib import Path
from typing import List, Optional

import pandas as pd

from .pipeline import AnalysisResult


def read_csv_column(
    file_path: str,
    column_name: str,
    encoding: str = "utf-8"
) -> List[str]:
    """
    Read a specific column from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        column_name: Name of the column to extract
        encoding: File encoding (default: utf-8 for multilingual support)
        
    Returns:
        List of text values from the specified column
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        KeyError: If the column name is not found
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    
    df = pd.read_csv(path, encoding=encoding)
    
    if column_name not in df.columns:
        available = ", ".join(df.columns.tolist())
        raise KeyError(
            f"Column '{column_name}' not found. Available columns: {available}"
        )
    
    # Convert to list, handling NaN values
    return df[column_name].fillna("").astype(str).tolist()


def save_results_csv(
    results: List[AnalysisResult],
    output_path: str,
    encoding: str = "utf-8"
) -> None:
    """
    Save analysis results to a CSV file.
    
    Args:
        results: List of AnalysisResult objects
        output_path: Path for the output CSV file
        encoding: File encoding (default: utf-8)
    """
    data = {
        "Original Text": [r.original_text for r in results],
        "Sentiment": [r.sentiment for r in results],
        "Extracted Topics": [", ".join(r.topics) for r in results]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding=encoding)


def generate_output_path(input_path: str) -> str:
    """
    Generate output file path by adding '_analyzed' suffix.
    
    Args:
        input_path: Original input file path
        
    Returns:
        Output path with '_analyzed' suffix before extension
    """
    path = Path(input_path)
    return str(path.parent / f"{path.stem}_analyzed{path.suffix}")
