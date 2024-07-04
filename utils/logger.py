import os


def check_create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def log_message(message="", log_dir="logs"):
    check_create_dir(log_dir)
    log_file = os.path.join(log_dir, "log.txt")
    with open(log_file, "a") as f:
        f.write(message + "\n")
