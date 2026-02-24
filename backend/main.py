from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain_core.messages import HumanMessage

from agent.graph import agent
from agent.state import AgentState
from agent.tools import list_files, read_file, write_file

app = FastAPI()

LANGCHAIN_TRACING_V2=True


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/run")
def run_agent(task: str):

    initial_state = AgentState(
        messages=[HumanMessage(content=task)]
    )

    result = agent.invoke(initial_state)

    return result

@app.get("/files")
def get_files():

    return list_files()


@app.get("/file")
def get_file(name: str):

    return {
        "content": read_file(name)
    }


@app.post("/file")
def save_file(name: str, content: str):

    write_file(name, content)

    return {"status": "saved"}
