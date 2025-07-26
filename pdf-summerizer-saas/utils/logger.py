def log_disabled_user(email):
    with open("disabled_users.log", "a") as log_file:
        log_file.write(f"{email}\n")