import os
from clean_log import clean_log_file

def test_clean_log_file(tmp_path):
    input_data = """INFO: System booted
DEBUG: CPU usage at 20%
WARNING: High memory usage
ERROR: Disk not found
DEBUG: Process started
WARNING: Battery low

INFO: Task complete
"""
    input_file = tmp_path/ "tmp_system.log"
    output_file = tmp_path / "temp_cleaned_system.log"

    input_file.write_text(input_data)

    clean_log_file(input_file, output_file)

    cleaned_data = output_file.read_text().strip().split("\n")

    expected = [
         "WARNING: High memory usage",
        "ERROR: Disk not found",
        "WARNING: Battery low"
         ]
    assert cleaned_data == expected
