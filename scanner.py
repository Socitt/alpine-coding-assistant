import os

MAX_FILE_SIZE = 3000  # keep it small for iSH

def scan_project(project_path):

    summary = []

    for root, dirs, files in os.walk(project_path):

        # skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for f in files:

            if f.endswith(".bak"):
                continue

            path = os.path.join(root, f)

            rel = os.path.relpath(path, project_path)

            summary.append(f"- {rel}")

    return "\n".join(summary)


def read_key_files(project_path):

    output = []

    for root, dirs, files in os.walk(project_path):

        for f in files:

            if not f.endswith(".py"):
                continue

            path = os.path.join(root, f)

            try:
                size = os.path.getsize(path)
                if size > MAX_FILE_SIZE:
                    continue

                with open(path, "r") as file:
                    content = file.read()

                rel = os.path.relpath(path, project_path)

                output.append(f"\nFILE: {rel}\n{content[:2000]}")

            except:
                pass

    return "\n".join(output)
