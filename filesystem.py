import os

def write_file(project_path, filename, content):
    path = os.path.join(project_path, filename)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    # backup once (not chain backups)
    if os.path.exists(path):
        backup = path + ".bak"
        if not os.path.exists(backup):
            os.rename(path, backup)

    with open(path, "w") as f:
        f.write(content)


def delete_file(project_path, filename):
    path = os.path.join(project_path, filename)

    if os.path.exists(path):
        os.remove(path)
