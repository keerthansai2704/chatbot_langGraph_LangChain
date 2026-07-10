from typing import Annotated, TypedDict
from urllib import response
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model



load_dotenv()


llm = init_chat_model("groq:llama-3.3-70b-versatile")
response=llm.invoke("what is console")

print(response)



