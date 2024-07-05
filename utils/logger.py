import os


def check_create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def log_message(message="", log_dir="logs"):
    check_create_dir(log_dir)
    with open(log_dir, "a") as f:
        f.write(message + "\n")
