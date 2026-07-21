from typing_extensions import TypedDict ,Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.types import interrupt,Command

memory=MemorySaver()
load_dotenv()

llm = init_chat_model("groq:llama-3.3-70b-versatile")

class MainGraph(TypedDict):
    messages:Annotated[list,add_messages]
    username:str


def approval_node(state:MainGraph):
    approve=interrupt(
        f"approve login for{state["username"]}"
    )
    if approve=="YES":
        print("login sucess")
    else:
        print("login rejected")
    return state

def chat_bot(state:MainGraph):
    response=llm.invoke(state["messages"]
    )
    return{
"messages":[response]
    }

MainGraph_builder=StateGraph(MainGraph)


MainGraph_builder.add_node("bot",chat_bot)
MainGraph_builder.add_node("approve",approval_node)

MainGraph_builder.add_edge(START,"bot")
MainGraph_builder.add_edge("bot","approve")

MainGraph_builder.add_edge("approve",END)

graph=MainGraph_builder.compile(
    checkpointer=memory
)
config={
        "configurable":{
            "thread_id":"chat_1"
        }
    }
# response=graph.invoke(
#     {
#         "messages":[
#             HumanMessage("iam keerthan sai")
#         ]
#     },config=config
# )

# for event in graph.stream(
#     {
#         "messages":[
#             HumanMessage("what is my name")
           
#         ]
#     },config=config
#     ,stream_mode="messages"
#     # ,stream_mode="debug",
#     # stream_mode="values"
# ):
#     # print(event)

#     # print(response["messages"][-1].content)
#     for node_name,node_output in event.items():
#         if "messages" in node_output:
#             print(node_output)
#             print(node_output["messages"][-1].content)


while True:

    user_input=input("user: ")
    
    if user_input.lower() in ["exit","stop"]:
        print("bye goodbye")
        break
    state =graph.get_state(config)

    if state.tasks and state.tasks[0].interrupts:

        input_data= Command(resume=user_input)
    else :
        input_data={
            "messages":[
            HumanMessage(content=user_input)
        ]}



    print("bot: ",end="",flush=True)


    for chunk ,metadata in graph.stream(
        input_data
        ,config=config,
        stream_mode="messages"

    ):
        print(chunk.content ,end="",flush=True)
        # for node_name ,node_output in event.items():
        #     if "messages" in node_output:
        #         print(node_output["messages"][-1].content)
            
    print()