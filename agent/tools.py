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


def list_files():

    files = {}

    for root, _, filenames in os.walk(WORKSPACE):

        for name in filenames:

            full = os.path.join(root, name)

            relative = os.path.relpath(full, WORKSPACE)

            with open(full, "r", encoding="utf-8") as f:
                files[relative] = f.read()

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

    process = subprocess.run(
        commands[ext],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
        timeout=20
    )

    return process.stdout, process.stderr, process.returncode
