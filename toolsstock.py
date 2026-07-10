from typing import Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages



load_dotenv()


llm=init_chat_model("groq:llama-3.3-70b-versatile")



class AgentState(TypedDict):
    messages: Annotated[list,add_messages]

    query: str
    intent:str

    selected_agent:str

    retrieved_documents:list
    sources:list

    draft_answer:str

    confidence:float
    retry_count:int

    final_answer:str


def router_node(state:AgentState):
    query = state["query"]

    decision = llm.invoke(
        f""
    )

    return{

        "selected_agent":decision
    }



def router_agent(state:AgentState):
    return state["selected_agent"]


builder=StateGraph(AgentState)

builder.add_node("router_node",router_node)
builder.add_node("router_agent",router_agent)

builder.add_edge(START,"router_node")

builder.add_edge("router_node","router_agent")

builder.add_edge("router_agent",END)

graph=builder.compile()





builder.add_conditional_edges(
    "router",
    router_agent,{
        "policy":"policy_agent",
        "invoice":"invoice_agent",
        "finance":"finance_agent"
    }
)



