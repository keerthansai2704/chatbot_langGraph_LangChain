from typing_extensions import TypedDict
from typing import Annotated 
from langgraph.graph import StateGraph ,START,END
from langgraph.graph.message import add_messages


# #this is state like data travelling inside the graph
# class Product(TypedDict):
#     text:str


# #node 

# def assemble_node(state:Product):
#     print("assembley Node")

#     return{
#         "text":state["text"] + "  assembled"

#     }

# def testing_node(state:Product):
#     print("Testing_node")

#     return{
#         "text":state["text"] +" tested"
#     }


# builder =StateGraph(Product)


# builder.add_node("assemble",assemble_node)
# builder.add_node("testing",testing_node)

# builder.add_edge(START,"assemble")
# builder.add_edge("assemble","testing")
# builder.add_edge("testing",END)

# graph=builder.compile()

# response =graph.invoke(
#     {
#         "text":"mobile parts"
#     }
# )

# print(response)



# class pizzahut(TypedDict):
#     pizza:str
#     status:str
#     bill:int

# def parcel_node(state:pizzahut):
#     print("parcel_node")
#     print(state)
#     return{
#         "status":" -> packed"
#     }

# def delivery_node(state:pizzahut):
#     print("delivery_node")
#     print(state)
#     return{
#         "status":" -> deliverd"
#     }


# builder = StateGraph(pizzahut)

# builder.add_node("parcel",parcel_node)
# builder.add_node("delivery",delivery_node)

# builder.add_edge(START,"parcel")
# builder.add_edge("parcel","delivery")
# builder.add_edge("delivery",END)


# graph = builder.compile()

# response=graph.invoke({
#     "pizza":"margaritta",
#     "status":"ready",
#     "bill":500

# })

# print(response)



# class PackageState(TypedDict):
#     package:str
#     quality:str
#     status :str
    

# def qualityCheck_node(state:PackageState) -> PackageState:
#     return {
#        "quality": state["quality"]
#     }
    
# def delivery_node(state:PackageState) -> PackageState:
    
#     print(state)
#     return{
#         "status":"deliverd to customer"
#     }

# def repack_node(state:PackageState) -> PackageState:
#     print(state)
#     return {
#        "status" :" repacked to store "
#     }

# def route(state:PackageState) -> PackageState:
#     if state["quality"] =="good":
#         return "delivery"
#     else:
#         return "repack"


# builder=StateGraph(PackageState)

# builder.add_node("qualityCheck",qualityCheck_node)
# builder.add_node("delivery",delivery_node)
# builder.add_node("repack",repack_node)



# builder.add_edge(START,"qualityCheck")
# builder.add_conditional_edges(
#     "qualityCheck",
#     route,
#     {"delivery":"delivery","repack":"repack"}
# )
# builder.add_edge("delivery",END)
# builder.add_edge("repack",END)
# graph=builder.compile()

# response=graph.invoke({
#     "package":"laptop",
#     "quality":"good",
#     "status":""

# })

# print(response)



class PackageState(TypedDict):

    messages:Annotated[list,add_messages]


def WareHouse(state:PackageState):
    return{
       "messages":["warehouse"]
    }

def DeliveryVan(state:PackageState):
    return{
        "messages":["deliveryvan"]
    }
def add_sacns(old,new):
    return old + new

builder = StateGraph(PackageState)

builder.add_node("warehouse",WareHouse)
builder.add_node("deliveryvan",DeliveryVan)

builder.add_edge(START,"warehouse")
builder.add_edge("warehouse","deliveryvan")
builder.add_edge("deliveryvan",END)

graph=builder.compile()
response=graph.invoke({
    "messages":[]

})

print(response)


