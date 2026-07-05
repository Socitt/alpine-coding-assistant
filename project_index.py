import os

def find_python_files(project_path):
    matches = []

    for root, _, files in os.walk(project_path):
        for f in files:
            if f.endswith(".py"):
                full = os.path.join(root, f)
                matches.append(full)

    return matches


def best_match_file(project_path, query):
    files = find_python_files(project_path)

    query = query.lower()

    # simple scoring
    for f in files:
        if query in f.lower():
            return f

    # fallback: return largest python file (main logic file)
    return files[0] if files else None
