from langgraph.constants import Send
from typing_extensions import TypedDict ,Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END

def add_result(old, new):
    return old + new

class send_exp(TypedDict):
    maths:int
    eng:int
    result:Annotated[list,add_result]
    average:float

def math_node(state:send_exp):
    return{
        "result":[state["maths"]]
    }

def eng_node(state:send_exp):
    return{
        "result":[state["eng"]]
    }
def distributor(state):
    print("distrubotr")
    return{}

def distributor_route(state:send_exp):
    return[

        Send("maths",state),
        Send("eng",state),
        Send('average',state)
        
    ]

def calculate_node(state:send_exp):

    result=state["result"]
    print(result)

    average= sum(result)/len(result)
    print(average)

    return{
        "average":average
    }

builder = StateGraph(send_exp)

builder.add_node("maths",math_node)
builder.add_node("eng",eng_node)
builder.add_node("distr",distributor)
builder.add_node("calc",calculate_node)


builder.add_edge(START,"distr")

builder.add_conditional_edges(
    "distr",
    distributor_route
)

builder.add_edge("maths","calc")
builder.add_edge("eng","calc")
builder.add_edge("calc",END)

graph =builder.compile()

response=graph.invoke(
    {
        "maths":98,
        "eng":62,
        "result":[],
        "average":"average"

    }
)

print(response)