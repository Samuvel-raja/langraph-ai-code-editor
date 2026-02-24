from typing import Dict, List, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(BaseModel):

    messages: Annotated[List[BaseMessage], add_messages] = Field(
        default_factory=list
    )

    # -------- CONTROL PLANE --------
    plan: str = ""

    operation: str = Field(
        default="create",  # create | modify | create_and_modify
        description="Type of operation"
    )

    files_to_create: List[str] = Field(
        default_factory=list
    )

    files_to_modify: List[str] = Field(
        default_factory=list
    )

    patches: list = Field(
    default_factory=list,
    description="Patch operations for modify"
)

    need_search: bool = False

    search_results: str = ""

    # -------- WORKSPACE --------
    files: Dict[str, str] = Field(
        default_factory=dict
    )

    active_file: str | None = None

    # -------- EXECUTION --------
    output: str = ""
    error: str = ""
    iteration: int = 0
    max_iterations: int = 5