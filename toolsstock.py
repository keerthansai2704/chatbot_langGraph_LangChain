from typing import Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages



load_dotenv()


llm=init_chat_model("groq:llama-3.3-70b-versatile")



class state(TypedDict):
    message= Annotated[list,add_messages]

    