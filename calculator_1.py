# import numpy as np
import math
from typing_extensions import TypedDict, Annotated
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph ,START,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv


load_dotenv()

class Calci(TypedDict):
    messages:Annotated[list,add_messages]


allowed_functions={"sqrt":math.sqrt,
                   "factorial":math.factorial,"sin":math.sin,"cos":math.cos,"tan":math.tan,"log":math.log,
                   "pow":math.pow}

llm = init_chat_model("groq:llama-3.3-70b-versatile")



@tool
def calculate(expression:str)->str:
    """
    evaluate the expression when user asks with any expression 
    """
llm_with_tools=llm.bind_tools([calculate])

def chat_node(state:Calci):
    response=llm_with_tools.invoke(
        state["messages"]
    )
    return{
        "messages":[response]
    }

tool_node=ToolNode([calculate]

)

def routing(state:Calci):
    last_message = state["messages"][-1]
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        return "tool"
    return END

builder = StateGraph(Calci)

builder.add_node("chatnode",chat_node)
builder.add_node("tool",tool_node)


builder.add_edge(START,"chatnode")

builder.add_conditional_edges(
    "chatnode",
    routing,{
        "tool":"tool",
        END:END

    }


)


builder.add_edge("tool","chatnode")


graph = builder.compile()


response = graph.invoke(
    {
        "messages":[
            HumanMessage(
                content="what is sqrt of 39 ?"
            )
        ]
    }
)

print(response["messages"][-1].content)






