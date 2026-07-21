from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph,START,END
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.types import Command
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from typing import Literal

load_dotenv()

class MainGraph(TypedDict):
    messages :Annotated[list,add_messages]
    # num:int

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
    response=route_llm.invoke(
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

def greeting_node(state:MainGraph):
   response=llm.invoke(state["messages"])

   return{
       "messages":[response]
   }

llm_with_tools= llm.bind_tools([add,multi])

def llm_node(state:MainGraph):
    response = llm_with_tools.invoke(state["messages"])
    return{
        "messages":[response]
    }

def should_continue(state:MainGraph):
    last_message=state["messages"][-1]
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        return "tool"
    return END

tool_node= ToolNode([add,multi])


calculator_builder=StateGraph(MainGraph)
calculator_builder.add_node("llm",
                            llm_node)
calculator_builder.add_node('tool',
                            tool_node)

calculator_builder.add_edge(START,
                            "llm")

calculator_builder.add_conditional_edges(
    "llm",
    should_continue
)
calculator_builder.add_edge("tool",
                            "llm")



calculator_agent=calculator_builder.compile()

greeting_builder=StateGraph(MainGraph)

greeting_builder.add_node("greeting",greeting_node)
greeting_builder.add_edge(START,"greeting")
greeting_builder.add_edge("greeting",END)


greeting_agent=greeting_builder.compile()


main_builder =StateGraph(MainGraph)

main_builder.add_node("calculator_agent",
                      calculator_agent
)
main_builder.add_node("greeting_agent",
                      greeting_agent)

main_builder.add_node("supervisor",
                      supervisor_node)

main_builder.add_edge(START,
                      "supervisor")


main_graph = main_builder.compile()

res= main_graph.invoke(
    {
        "messages":[
            HumanMessage(content="hello how you  ")
        ]
    }

    
)
print(res["messages"][-1].content)