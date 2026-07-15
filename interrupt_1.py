from typing_extensions import TypedDict
from langgraph.types import interrupt

class ApproveState(TypedDict):
    username:str

def approval_node(state:ApproveState):
    
    interrupt(
        f"approved login for {state['username']}"
    )
    print("login approved")
    return {}
