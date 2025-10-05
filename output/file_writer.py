# 📁 Saves JSON/CSV locally
import csv
import os
from typing import Dict, List


def save_jobs_to_csv(jobs: List[Dict[str, str]], file_path: str):
    """Saves a list of job dictionaries to a CSV file at the specified path."""
    if not jobs:
        print("No jobs to save.")
        return

    # Ensure the output directory exists before writing
    output_dir = os.path.dirname(file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    keys = jobs[0].keys()
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(jobs)
        print(f"Successfully saved {len(jobs)} jobs to {file_path}")
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")