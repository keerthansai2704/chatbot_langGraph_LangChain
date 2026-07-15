from typing_extensions import TypedDict ,Annotated
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph ,START,END
from langchain_core.messages import HumanMessage

load_dotenv()


llm = init_chat_model("groq:llama-3.3-70b-versatile")

class chatState(TypedDict):
    messages:Annotated[list,add_messages]

def chatBot(state:chatState):
    response=llm.invoke(state["messages"])
    return{

        "messages":[response]
    }


builder= StateGraph(chatState)

builder.add_node("bot",chatBot)

builder.add_edge(START,"bot")

builder.add_edge("bot",END)

graph= builder.compile()


response = graph.invoke(
    {
        "messages": [
            HumanMessage("what is my name?.")
        ]
    }
)

print(response["messages"][-1].content)