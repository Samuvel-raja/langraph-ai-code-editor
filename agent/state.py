from typing import Dict, List,Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages



class AgentState(BaseModel):

    messages: Annotated[List[BaseMessage],add_messages] = Field(
        default_factory=list,
        description="Conversation history"
    )

    plan: str = Field(
        default="",
        description="Execution plan"
    )

    files: Dict[str, str] = Field(
        default_factory=dict,
        description="Workspace files"
    )

    active_file: str = Field(
        default="main.py",
        description="Entry file"
    )

    output: str = Field(
        default="",
        description="Execution output"
    )

    error: str = Field(
        default="",
        description="Execution error"
    )

    iteration: int = Field(
        default=0,
        description="Current retry count"
    )

    max_iterations: int = Field(
        default=5,
        description="Max retries allowed"
    )
