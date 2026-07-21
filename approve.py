from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command


memory = MemorySaver()

class GraphState(TypedDict):
    pass

def approval_node(state: GraphState):

    print("Node Started")

    approval = interrupt("Approve this request?")

    print(f"Approval received : {approval}")

    print("Node Finished")

    return state

builder = StateGraph(GraphState)

builder.add_node("approval", approval_node)

builder.add_edge(START, "approval")
builder.add_edge("approval", END)

graph = builder.compile(
    checkpointer=memory
)

config = {
    "configurable": {
        "thread_id": "thread_1"
    }
}

graph.invoke(
    {},
    config=config
)