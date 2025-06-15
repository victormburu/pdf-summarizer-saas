#!/usr/bin/env python 
with open("d_byzero.py", "r", encoding = "utf-8") as file:
    content = file.read()

cleaned = content.replace('\u00a0', '   ')

with open("d_byzero_cleaned.py", "w", encoding="utf-8") as file:
    file.write(cleaned)

print("cleaned file saved as d_byzero_cleaned.py")
    
import sys
import subprocess
with open(sys.argv[1]) as file:
    lines = file.readlines()
    for line in lines:
        oldvalue = line.strip()
        newvalue = oldvalue.replace("jane", "jdoe")
        subprocess.run(["mv", oldvalue, newvalue])
file.close()
