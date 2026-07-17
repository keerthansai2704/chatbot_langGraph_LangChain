from typing_extensions import TypedDict
from langgraph.graph.message import add_messages,Annotated
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from typing import Literal
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph,START,END

llm = init_chat_model("groq:llama-3.3-70b-versatile")

class MultiAgentGraph(TypedDict):
    messages:Annotated[list,add_messages]
    num:int
    greet_messages:str

def calculator_graph(state:MultiAgentGraph):
    return{
            "num":state["num"]+10
        }
        
def greeting_graph(state:MultiAgentGraph):
    return{
        "messages":[
            AIMessage(content="how can i help you ?") 
        ]
        
    }

class Router(TypedDict):
    next: Literal[
        "calculator_graph",
        "greeting_graph"
    ]

route_llm=llm.with_structured_output(Router)
# this is LLMM supervisor
def supervisor_node(state:MultiAgentGraph) -> Command:
    system_prompt="""

            you are a supervisor 
            your job is to not to answer the user question

            your job is to decide which agent should handle the request

            available agents:
            1.calculator_graph
            2.greeting_graph

            return correct agent
            """

    response=route_llm.invoke(
        [
            {
            "role":"system",
            "content":system_prompt
        },*state["messages"]
        ]
    )
    return Command(
        goto=response["next"]
    )
    
calculator_builder=StateGraph(MultiAgentGraph)


calculator_builder.add_node("calculator_node",calculator_graph)
calculator_builder.add_node("greeting_node",greeting_graph)
