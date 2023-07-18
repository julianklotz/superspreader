import os
from pathlib import Path


def file_path(file_name):
    tests_dir = Path(__file__).parent.absolute()
    path = os.path.join(tests_dir, "spreadsheets", file_name)
    return path
