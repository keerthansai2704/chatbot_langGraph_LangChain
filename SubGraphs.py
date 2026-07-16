from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
class MainState(TypedDict):
    username:str
    password:int
    num:int

def login_node(state:MainState):
    print ("login sucess")

    return{
        
    }

class MathGraph(TypedDict):
    num:int

def addition_node(state:MathGraph):
    print("addtion node")
    return{
        "num":state["num"]+10
    }

def multiplication_node(state:MathGraph):
    print("multiplication node")
    return{
        "num":state["num"]*10
    }

math_builder = StateGraph(MathGraph)

math_builder.add_node("add",addition_node)

math_builder.add_node("multi",multiplication_node)

math_builder.add_edge(START,"add")
math_builder.add_edge("add","multi")
math_builder.add_edge("multi",END)

math_graph =math_builder.compile()

main_builder = StateGraph(MainState)


main_builder.add_node(
    "math",
    math_graph
)
main_builder.add_node("login",login_node)

main_builder.add_edge(START,"login")
main_builder.add_edge("login","math")
main_builder.add_edge("math",END)

main_graph= main_builder.compile()

response = main_graph.invoke(
    {
        "username":"kerthan",
        "password":1234,
        "num":5
    }
)

print(response)