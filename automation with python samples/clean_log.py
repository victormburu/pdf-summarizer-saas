def is_important(line):
    return line.startswith("ERROR") or line.startswith("WARNING")

def clean_log_file(input_file, output_file):
    with open(input_file, "r") as file:
        lines = file.readlines()

    cleaned_lines = [line for line in lines if is_important(line.strip()) and line.strip()]

    with open(output_file, "w") as file:
        file.writelines(cleaned_lines)

    print(f"cleaned log saved to {output_file}")

    if __name__ == "__main__":
         clean_log_file("system.log", "cleaned_system.log")
