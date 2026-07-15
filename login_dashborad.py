from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from typing import Literal
from langgraph.types import Command
from langgraph.graph import StateGraph ,START,END

load_dotenv()

# llm=init_chat_model("groq:llama-3.3-70b-versatile")

class LoginState(TypedDict):

    username:str 

    password: str

    authentication:bool


# def login_node(state:LoginState):
#     state={
#         "username":state["username"],
#         "password":state["password"],
#         "authentication":state['authentication']
#     }


def login_node(state:LoginState) -> Command[Literal["dashboard","retry_login"]]:
    username= state["username"]
    password=state["password"]


    if username == "keerthan27" and password == "1234":
        return Command(
            update={
                "authenticated":True
            },
            goto="dashboard"
        )
    else:
        return Command(
            update={
                "authenticated":False

            },
            goto="retry_login"
        )
    
def dashboard(state:LoginState):
    print(
        f"welcome {state['username']}"
    )
    return{}

def retry_login(state:LoginState):
    print(
        f" not found {state['username']}"
    )
    return {}


builder = StateGraph(LoginState)

builder.add_node("login",login_node)
builder.add_node("dashboard",dashboard)
builder.add_node("retry_login",retry_login)

builder.add_edge(START,"login")
# builder.add_edge("login","dashboard")
builder.add_edge("dashboard",END)
builder.add_edge("retry_login",END)

graph =builder.compile()

response = graph.invoke(
    {
        "username":"keerthan27",
        "password":"1234"
    }
)
