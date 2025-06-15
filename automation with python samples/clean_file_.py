#clean_file_.py

with open("pytestfixture.py", "r", encoding="utf-8") as file:
    content = file.read()

# Replace non-breaking spaces (U+00A0) with normal space
cleaned = content.replace('\u00a0', '  ')

with open("pytestfixture_cleaned.py", "w", encoding="utf-8") as file:
    file.write(cleaned)

print("cleaned file saved as pytestfixture_cleaned.py")
