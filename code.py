from agent import ask_ai
from projects import select_project


def main():

    project_path = select_project()

    if not project_path:
        print("No project selected.")
        return

    print("\nNemo Code (stable v3)")
    print(f"Project: {project_path}\n")

    while True:
        try:
            prompt = input("code> ")

            if prompt.strip() in ["exit", "quit"]:
                break

            full_prompt = f"""
PROJECT: {project_path}

USER TASK:
{prompt}
"""

            response = ask_ai(full_prompt)
            print("\n" + response + "\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
