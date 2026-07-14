from typing import TypedDict
from typing_extensions import TypedDict , Annotated
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, StateGraph ,START
class CalAgent(TypedDict):
    messages:Annotated[list,add_messages]

load_dotenv()
llm=init_chat_model("groq:llama-3.3-70b-versatile")

@tool
def multiply(a:int,b:int)->int:
    """ 
    Multiply two integers
    use this tools whenever the usr ask for the multiplication
    """
    return a*b
@tool
def add(a:int,b:int)->int:
    """
    Add two integres 
    use this tools whenver the user adk fr addition
    
    """
    return a+b
@tool
def subtract(a:int,b:int)->int:
    """
    Subtract two integres 
    use this tools whenver the user ask for subtracion
    
    """
    return a-b ,b-a
@tool
def divide(a:int,b:int)->float:
    """
    divide two integres 
    use this tools whenver the user ask for division
    
    """
    return a/b , b/a

llm_with_tools  = llm.bind_tools([multiply])

def chatbot_node(state:CalAgent):

    response=llm_with_tools.invoke(
        state["messages"]
    )

    return{
        "messages":[response]
    }


tool_node=ToolNode(
    [multiply,add,subtract,divide]
)

def should_continue(state:CalAgent):

    last_message= state["messages"][-1]

    if last_message.tool_calls:
        return "tools"
    
    return END


builder =StateGraph(CalAgent)

builder.add_node("chatnode",chatbot_node)
builder.add_node("tools",tool_node)

builder.add_edge(START,"chatnode")

builder.add_conditional_edges(
    "chatnode",
    should_continue,{
        "tools":"tools",
    
        END:END

    },
)

builder.add_edge("tools","chatnode")

graph =builder.compile()

response = graph.invoke(
    {
        "messages":[
            HumanMessage(content="what is 2/3 and 2*3 and 2+3 and 2-3")
        ]
    }
)

print(response["messages"][-1].content)