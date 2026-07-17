from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph,START,END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.types import Command
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from typing import Literal

load_dotenv()

class MainGraph(TypedDict):
    messages :Annotated[list,add_messages]
    num:int



llm=init_chat_model("groq:llama-3.3-70b-versatile")

class Router(TypedDict):
    next:Literal["calculator_agent","greeting_agent"]
route_llm = llm.with_structured_output(Router)


def supervisor_node(state:MainGraph):
    system_prompt="""
    you are supervisor you are here to not to answer
    your job is to direct which agent is perfec to anser user query 

    avalable agents:
    -calculator_agent
    -greetings_agent

"""
    response=llm.invoke(
        [
            {
                "role":"system",
                "content":system_prompt,

            },*state["messages"]
        ]
    )
    return Command(

        goto=response["next"]
    )
@tool
def add(a:int,b:int)->int:
    """ add two numbers"""
    return a+b
@tool
def multi(a:int,b:int)->int:
    """ multiply two numbers """
    return a*b

# def calculator_agent(state:MainGraph):
#     return{
#         "num":state["num"]+1
    # }

# def greetng_agent(state:MainGraph):
#     return{

    # }

llm_with_tool= llm.bind_tools([add,multi])

def llm_node(state:MainGraph):
    response = llm_with_tool.invoke(state["messages"])
    return{
        "messages":[response]
    }

def should_continue(state:MainGraph):
    last_message=state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

tool_node= ToolNode([add,multi])


calculator_builder=StateGraph(MainGraph)
calculator_builder.add_node("llm",llm_node)
calculator_builder.add_node('tool',tool_node)

calculator_builder.add_edge(START,"llm")

calculator_builder.add_conditional_edges(
    "llm",
    should_continue
)
calculator_builder.add_edge("tool","llm")
calculator_builder.add_edge("tool",END)


calculator_agent=calculator_builder.compile()

greetng_builder=StateGraph(MainGraph)

greeting_agent=greetng_builder.compile()

