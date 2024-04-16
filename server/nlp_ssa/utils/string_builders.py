import csv
import io
from typing import Dict, List


def build_csv_string(fieldnames: List[str], data: List[Dict]) -> str:
    """Builds a CSV as a string from a collection of data

    Args:
        `fieldnames`: List of strings used to generate CSV's column headers
        `data`: Objects to be mapped to each row of CSV

    Returns:
        str: A string representation of a CSV file
    """

    csv_output = io.StringIO()
    csv_writer = csv.DictWriter(csv_output, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(data)
    csv_output.seek(0)  # reset pointer so that it will read the entire file

    csv_string = csv_output.read()

    csv_output.close()

    return csv_string
