def apply_actions(project_path, text):

    import re
    from filesystem import write_file, delete_file

    # ONLY match clean blocks
    writes = re.findall(
        r"WRITE (.*?)\\n<<<\\n(.*?)\\n>>>",
        text,
        re.S
    )

    deletes = re.findall(r"DELETE (.*)", text)

    seen = set()

    print("\nPlan:")

    for f, _ in writes:
        print("WRITE", f)
        seen.add(f)

    for f in deletes:
        if f not in seen:
            print("DELETE", f)

    for filename, content in writes:
        write_file(project_path, filename.strip(), content)

    for filename in deletes:
        if filename.strip() not in seen:
            delete_file(project_path, filename.strip())
