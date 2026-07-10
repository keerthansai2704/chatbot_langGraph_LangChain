from typing import TypedDict ,Annotated
from langgraph.graph import StateGraph,END
from langgraph.graph.message import add_messages


class Company(TypedDict):
    messages: Annotated[list,add_messages]
    investment:int
    profit:int
    outcome:int
    returns:int



def cal_investment_node(State:Company) -> dict:
    invst=10000 
    return {"investment":invst}

def cal_returns_node(State:Company) -> int:
    returns = -11000
    return {"returns":returns}

def cal_outcome_node(State:Company) -> dict:
    outcome=State["returns"] - State["investment"]
    return {"outcome":outcome}



def route_profit_or_loss(State:Company) -> dict:
    return "profit" if State["outcome"] >= 0 else "loss"


def profit_node(State:Company) -> dict:
    print(f'got Profit of rupess{State["outcome"]}')
    return {}


def cal_loss_node(State:Company) -> int:
    print(f'got loss of rupees{abs(State["outcome"])}')
    return {}


graph = StateGraph(Company)

graph.add_node("investment",cal_investment_node)
graph.add_node("profit",profit_node)
graph.add_node("loss",cal_loss_node)
graph.add_node("outcome",cal_outcome_node)
graph.add_node("returns",cal_returns_node)

graph.set_entry_point("investment")

graph.add_edge("investment","returns")
graph.add_edge("returns","outcome")

graph.add_conditional_edges(
    "outcome",
    route_profit_or_loss,
    {"profit":"profit","loss":"loss"}

)
graph.add_edge("loss",END)
graph.add_edge("profit",END)

app = graph.compile()


result= app.invoke({"messages":[]})

print(result["outcome"])
