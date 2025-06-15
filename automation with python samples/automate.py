import csv # import csv module to read and write csv files
import secrets # import secrets module to generate secure random numbers passwords
import subprocess # import subprocess module to run system commands
from pathlib import Path # import Path class from pathlib module to work with file paths

cwd = Path.cwd() # get the current working directory
with open(cwd / "users_in.csv", "r") as file_input, open(cwd / "users_out.csv", "w") as file_output: # open the input and output files
    reader = csv.DictReader(file_input) # create a csv reader object
    writer = csv.DictWriter(file_output, fieldnames=reader.fieldnames) # create a csv writer object to write the output file
    writer.writeheader() # write the header of the output file with the same fieldnames as the input file

    for user in reader:
        if "name" in user and "username" in user:  # check if 'name' and 'username' keys exist
            user["password"] = secrets.token_hex(8) # generate a random password for each user
            # Full path to PowerShell executable
            powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
            # PowerShell command to create a user on Windows with elevated privileges
            useradd_cmd = [
                powershell_path, "-Command",
                f"Start-Process powershell -ArgumentList 'New-LocalUser -Name \"{user['username']}\" -Password (ConvertTo-SecureString \"{user['password']}\" -AsPlainText -Force) -FullName \"{user['name']}\"' -Verb RunAs"
            ]
            try:
                subprocess.run(useradd_cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to create user {user['username']}: {e}")
            writer.writerow(user) # write the user information to the output file
        else:
            print(f"Skipping user entry due to missing 'name' or 'username': {user}")