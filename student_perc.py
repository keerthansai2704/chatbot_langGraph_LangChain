from typing_extensions import TypedDict ,Annotated
from langgraph.graph.message import add_messages
from langgraph.types import Command
from typing import Literal

class calc_percent(TypedDict):
    maths:int
    english:int
    science:int
    evaluated_subjects:list
    percentage:float

def math_node(state:calc_percent):
    return{
        "evaluated_subjects":["maths"]
    }

def science_node(state:calc_percent):
    return{
        "evaluated_subjects":["science"]
    }

def english_node(state:calc_percent):
    return{
        "evaluated_subjects":["english"]
    }

def calculate_node(state:calc_percent) -> Command[Literal["merit","not merit"]]:
    maths =state["maths"]
    science =state["science"]
    english=state["english"]

    percentage=(maths+english+science)/3

    if percentage >= 91:
        
        return Command(
            update={
                "percentage"=percentage
                
            },
            goto="merit"
        )
    else:
        return Command(
            update={
                "percentage"=percentage
                
            },
            goto="not merit"
        )


def maths_node(state:calc_percent):

