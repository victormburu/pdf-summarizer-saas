#!/usr/bin/env python3

import csv

# Function to read employee data from a CSV file
# The function takes a file path as an argument and returns a list of dictionaries
# where each dictionary represents an employee's data.
# The CSV file is expected to have a header row with the field names.
def read_employee_data(file_path):
    csv.register_dialect('empdialect', delimiter=',', skipinitialspace=True)
    employee_file = csv.DictReader(open(file_path), dialect='empdialect')
    employee_list = []
    for data in employee_file:
        employee_list.append(dict(data))
        return employee_list
def process_employee_data(employee_list):
    department_list = []
    for employee in employee_list:
        department_list.append(employee['Department'])
    department_data = {}
    for department_name in set(department_list):
        department_data[department_name] = department_list.count(department_name)
        return department_data
    
def write_report(dict, report_file):
    with open(report_file, "w+") as file:
        for key in sorted(dict):
            file.write(str(key) + ':' + str(dict[key]) + '\n')
        file.close()
