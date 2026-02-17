import json
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from .state import AgentState
from .tools import write_file, list_files, execute_file
from .prompt import PLANNER_PROMPT, DEBUGGER_PROMPT
from dotenv import load_dotenv
import os
load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

# Initialize LLM once (production pattern)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)


# -------------------------
# PLANNER NODE
# -------------------------
def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Creates execution plan and initial files.
    Updates:
        - plan
        - files
        - active_file
        - messages
    """

    user_task = state.messages[-1].content

    prompt = PLANNER_PROMPT.format(task=user_task)

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    try:
        print(response.content,"data")
        data = json.loads(response.content)
        
        raw_plan = data.get("plan", "")

        if isinstance(raw_plan, list):
          plan = "\n".join(raw_plan)
          files = data.get("files", {})
          active_file = data.get("active_file", "main.py")
        else:
                plan = str(raw_plan)
                files = data.get("files", {})
                active_file = data.get("active_file", "main.py")

    except Exception as e:
        raise Exception(f"Planner returned invalid JSON: {str(e)}")

    return {

        "plan": plan,

        "files": files,

        "active_file": active_file,

        "messages": [
            AIMessage(content="Planning completed")
        ]
    }


# -------------------------
# WRITER NODE
# -------------------------
def writer_node(state: AgentState) -> Dict[str, Any]:
    """
    Writes files to workspace.
    Uses:
        state.files
    """

    for filename, content in state.files.items():

        write_file(filename, content)

    return {}


# -------------------------
# LOADER NODE
# -------------------------
def loader_node(state: AgentState) -> Dict[str, Any]:
    """
    Loads all workspace files into state.
    Updates:
        state.files
    """

    files = list_files()

    return {
        "files": files
    }


# -------------------------
# EXECUTOR NODE
# -------------------------
def executor_node(state: AgentState) -> Dict[str, Any]:
    """
    Executes active file.
    Updates:
        state.output
        state.error
        state.iteration
    """

    active_file = state.active_file

    stdout, stderr, returncode = execute_file(active_file)

    return {

        "output": stdout,

        "error": stderr,

        "iteration": state.iteration + 1

    }


# -------------------------
# DEBUGGER NODE
# -------------------------
def debugger_node(state: AgentState) -> Dict[str, Any]:
    """
    Fixes code based on error.
    Uses:
        state.plan
        state.files
        state.error

    Updates:
        state.files
        state.messages
    """

    prompt = DEBUGGER_PROMPT.format(
        plan=state.plan,
        files=json.dumps(state.files, indent=2),
        error=state.error
    )

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    try:
        fixed_files = json.loads(response.content)

        if not isinstance(fixed_files, dict):
            raise Exception("Debugger returned invalid format")

    except Exception:
        # fallback: keep existing files
        fixed_files = state.files

    return {

        "files": fixed_files,

        "messages": [
            AIMessage(content="Debug fix applied")
        ]
    }


# -------------------------
# DECISION NODE
# -------------------------
def decision_node(state: AgentState) -> str:
    """
    Determines next step.

    Returns:
        "debug" or "end"
    """

    if state.error == "":
        return "end"

    if state.iteration >= state.max_iterations:
        return "end"

    return "debug"
