from langchain_core.tools import tool


#core execution on ToolNode
class MyToolNode():


    def __init__(self,tools):

        self.tools = {}

        for tool in tools:
            self.tools[tool.name] = tool

    def execute(self,tool_call):

        tool_name =tool_call["name"]

        args=tool_call["args"]

        tool =self.tools[tool_name]

        result = tool.invoke(args)

        return result 

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.
    """
    return a * b
    

tool_call = {
    "name":"multiply",

    "args":{
        "a":25,

        "b":25
    }
}


node = MyToolNode([multiply])

print(
    node.execute(tool_call)
)