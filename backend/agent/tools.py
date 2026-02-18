import os
import subprocess

WORKSPACE = "workspace"

os.makedirs(WORKSPACE, exist_ok=True)


def write_file(filename: str, content: str):

    path = os.path.join(WORKSPACE, filename)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_file(filename: str):

    path = os.path.join(WORKSPACE, filename)

    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".json", ".md", ".txt",
    ".html", ".css", ".yaml", ".yml"
}


def list_files(workspace="workspace"):

    files = {}

    for root, _, filenames in os.walk(workspace):

        for filename in filenames:

            path = os.path.join(root, filename)

            relative = os.path.relpath(path, workspace)

            ext = os.path.splitext(filename)[1]

            # Skip binary files
            if ext not in TEXT_EXTENSIONS:
                continue

            try:

                with open(path, "r", encoding="utf-8") as f:

                    files[relative] = f.read()

            except UnicodeDecodeError:

                print(f"Skipped binary file: {relative}")

            except Exception as e:

                print(f"Error reading file {relative}: {e}")

    return files

def execute_file(filename: str):

    ext = filename.split(".")[-1]

    commands = {
        "py": ["python", filename],
        "js": ["node", filename],
        "sh": ["bash", filename],
    }

    if ext not in commands:
        return "", f"Unsupported file type: {ext}", 1

    try:

        process = subprocess.run(
            commands[ext],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=10,  # reduce timeout
            input="Enter the input"     # prevent input blocking
        )

        return process.stdout, process.stderr, process.returncode

    except subprocess.TimeoutExpired:

        return (
            "",
            "Execution timed out. Likely waiting for input() or infinite loop.",
            1
        )

    except Exception as e:

        return (
            "",
            f"Execution failed: {str(e)}",
            1
        )
