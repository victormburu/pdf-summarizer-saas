#!/usr/bin/env python
with open("d_byzero1.py", "r", encoding="utf-8") as file:
    content = file.read()
    
    cleaned = content.replace('\u00a0', '   ')

with open("d_byzero1_cleaned.py", "w", encoding="utf-8") as file:
    file.write(cleaned)
print("file already cleaned ")
