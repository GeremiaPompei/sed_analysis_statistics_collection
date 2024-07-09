import os


def create_csv_file(filepath, keys):
    if not os.path.exists(filepath):
        open(filepath, 'w').write(f'{",".join(["user", *keys, "created_at"])}\n')


def register_csv_row(data, filepath, user, keys, timestamp):
    with open(filepath, 'a') as fp:
        for d in data:
            buffer = f"{user},"
            for key in keys:
                buffer = f"{buffer}{d[key]},"
            buffer = f"{buffer}{timestamp}\n"
            fp.write(buffer)
