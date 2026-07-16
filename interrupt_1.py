from typing_extensions import TypedDict
from langgraph.types import interrupt ,Command
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.graph import StateGraph ,END,START

load_dotenv()

memory = MemorySaver()
llm = init_chat_model("groq:llama-3.3-70b-versatile")

class ApproveState(TypedDict):
    username:str

def approval_node(state:ApproveState):
    
    approved=interrupt(
        f"Approved login for {state['username']}?"
    )
    if approved == "YES":

        print(" login approved")
    else:
        print("login rejcted ")
    
    return {

    }
builder  =StateGraph(ApproveState)

builder.add_node("approve",approval_node)

builder.add_edge(START,"approve")

builder.add_edge("approve",END)

graph=builder.compile(

    checkpointer=memory
)

config = {
    "configurable":{
        "thread_id":"thread_1"
    }
}
# for event in graph.stream(
#     {
#         "username":"username"
#     },
#     config=config,
#     stream_mode="updates"
# ):
#     print(event)

response = graph.invoke(
    {
     "username":"keerthan sai "   
    },
    config=config
)
# print(response)
    

response = graph.invoke(
    Command(
        resume="YES"
    ),
    config=config
)
# print(response)