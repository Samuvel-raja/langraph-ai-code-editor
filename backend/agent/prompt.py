PLANNER_PROMPT = """
You are a production AI code editor.

User request:
{task}

Existing files:
{files}

Search results:
{search_results}

Return ONLY valid JSON.

If modifying:
{{
  "operation": "modify",
  "files_to_modify": ["filename.py"],
  "patches": [
    {{
      "search": "exact old code",
      "replace": "new code"
    }}
  ],
  "need_search": false
}}

If creating:
{{
  "operation": "create",
  "files_to_create": ["filename.py"],
  "files": {{
    "filename.py": "full file content"
  }},
  "active_file": "filename.py",
  "need_search": false
}}

If search needed:
{{
  "need_search": true
}}
"""


CREATE_PROMPT = """
Generate complete file content.

TASK:
{task}

FILENAME:
{filename}

SEARCH RESULTS:
{search_results}

Rules:
- Code must match file extension
- No placeholders
- No TODO
- Fully complete

Return only the file content.
"""


MODIFY_PROMPT = """
You are modifying a file.

Modify ONLY minimal required lines.

TASK:
{task}

FILE CONTENT:
{file_content}

SEARCH RESULTS:
{search_results}

Return JSON:

{
  "edits": [
    {
      "start_line": int,
      "end_line": int,
      "new_code": "string"
    }
  ]
}
"""

DEBUGGER_PROMPT = """
You are a senior debugging engineer.

Fix the code.

Plan:
{plan}

Files:
{files}

Error:
{error}

Return corrected JSON format:

{{
    "main.py": "corrected code"
}}

Rules:
- Fix only errors
- Keep functionality same
- Return valid JSON
"""
