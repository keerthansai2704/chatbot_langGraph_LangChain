from typing_extensions import TypedDict
from langgraph.graph.message import add_messages,Annotated
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from typing import Literal
from langchain_core.messages import AIMessage


llm = init_chat_model("groq:llama-3.3-70b-versatile")

class MultiAgentGraph(TypedDict):
    messages:Annotated[list,add_messages]
    num:int
    greet_messages:str


class router(TypedDict):
    next: Literal[
        "calculate_agent",
        "greeting_agent"
    ]

route_llm=llm.with_structured_output(router)

def supervisor_node(state:MultiAgentGraph) -> Command:
    system_prompt="""

            you are a supervisor 
            your job is to not to answer the user qustion

            your job is to decide which agent should handle the request

            available agents:
            1.calculator_agent
            2.greeting_agent

            return correct agent
            """

    response=router.llm.invoke(
        [
            {
            "role":"system","content":system_prompt
        },*state["messages"]
        ]
    )
    return Command(
        goto=response["next"]
    )
    
def calc_graph(state:MultiAgentGraph):
    return{
            "num":state["num"]+10
        }
        

def greet_graph(state:MultiAgentGraph):
    return{
        "messages":[
            AIMessage(content="how can i help you ?") 
        ]
        
    }




