import os

BASE_DIR = "/root/projects"


def list_projects():
    return [
        f for f in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, f))
    ]


def select_project():
    projects = list_projects()

    if not projects:
        print("No projects found.")
        return None

    print("\nProjects:\n")

    for i, p in enumerate(projects, 1):
        print(f"{i}) {p}")

    print(f"{len(projects)+1}) Create new project")

    choice = input("\nSelect project: ")

    try:
        choice = int(choice)
    except:
        return None

    if choice == len(projects) + 1:
        name = input("New project name: ")
        path = os.path.join(BASE_DIR, name)
        os.makedirs(path, exist_ok=True)
        return path

    if 1 <= choice <= len(projects):
        return os.path.join(BASE_DIR, projects[choice - 1])

    return None
