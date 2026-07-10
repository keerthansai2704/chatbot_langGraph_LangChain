from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages



load_dotenv()


llm = init_chat_model("groq:llama-3.3-70b-versatile")
response=llm.invoke("what is console")

print(response)


class State(TypedDict):
    messages:Annotated[list,add_messages]


def chatbot_node(state: State) -> str:
    response =llm.invoke(state["messages"])

    return{
        "messages":[response]
        }

builder =StateGraph(State)

builder.add_node("chatbot",chatbot_node)

builder.add_edge(START,"chatbot")

builder.add_edge("chatbot",END)

graph = builder.compile()


message={"role":"user",
          "content":"what is console"
          }


response=graph.invoke({"messages":[message]})

# response["messages"]



state= None
while True:
    in_messages=input("YOU:")
    if in_messages.lower() in {"quit","exit"}:

        break
    if state is None:
        state :State ={
            "messages":[{"role":"user","content":in_messages}]

        }
    else:
        state["messages"].append({"role":"user","content":in_messages})


        state=graph.invoke(state)
        print("Bot: ",state["messages"][-1].content)


