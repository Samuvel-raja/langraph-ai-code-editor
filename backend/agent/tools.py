import os
import subprocess

WORKSPACE = "workspace"

os.makedirs(WORKSPACE, exist_ok=True)


def write_file(filename: str, content: str):

   path=os.path.join(WORKSPACE,filename)

   os.makedirs(os.path.dirname(path),exist_ok=True)

   with open(path,"w",encoding="utf-8") as f:
       f.write(content)


def read_file(filename: str):

    path=os.path.join(WORKSPACE,filename)

    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return f.read()
    else:
        return ""
     


TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".json", ".md", ".txt",
    ".html", ".css", ".yaml", ".yml"
}


def list_files(workspace="workspace"):
   
   files={}


   for root,_,filenames in os.walk(workspace):
       
       for filename in filenames:
        path=os.path.join(root,filename)
        relativepath=os.path.relpath(path,workspace)

        ext=os.path.splitext(filename)[1]

        if ext in TEXT_EXTENSIONS:
            try:
                with open(path,"r",encoding="utf-8") as f:
                    files[relativepath]=f.read()
            except Exception as e:
                print("Can't read the files")
        else:
            return "Unsupported files types"

       return files
       
def apply_patches(file_path: str, patches: list):

    content = read_file(file_path)

    if not content:
        raise Exception("File not found")

    original = content

    for patch in patches:
        old = patch.get("search", "")
        new = patch.get("replace", "")

        if not old:
            # Nothing to search for; skip this patch
            continue

        if old not in content:
            # Be tolerant: log and skip instead of crashing the agent
            print(f"[apply_patches] Patch target not found in {file_path}: {old[:80]!r}")
            continue

        content = content.replace(old, new, 1)

    if content == original:
        # No effective change; do not error, just return
        print(f"[apply_patches] No changes applied to {file_path}")
        return

    write_file(file_path, content)

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
            timeout=10,  
            input="Enter the input"     
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


def search_codebase(query: str) -> str:

    results = []

    for root, _, files in os.walk("./workspace"):

        for file in files:

            if file.endswith((".py", ".js", ".ts")):

                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:

                        content = f.read()

                        if query.lower() in content.lower():

                            results.append(
                                f"File: {path}\n{content[:500]}"
                            )

                except:
                    pass

    return "\n\n".join(results)