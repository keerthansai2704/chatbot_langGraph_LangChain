from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict ,Annotated
from langgraph.graph.message import add_messages
load_dotenv()

llm =init_chat_model("groq:llama-3.3-70b-versatile")

class mat(TypedDict):
   messages:Annotated[list,add_messages]

@tool
def suming_numbers(a:int,b:int)->int:
   """ a==2,b==3
   """
   return a + b

llm_with_tools= llm.bind_tools([suming_numbers])

response = llm_with_tools.invoke(
   "what is 25+25"
)


tool_node = ToolNode([suming_numbers])
# print(response)


# {
#     "suming_numbers": <StructuredTool object>
# }

# tools = {
#    "suming_numbers":suming_numbers
# }

# tool_call = response.tool_calls[0]

# tool_name=tool_call["name"]

# args= tool_call["args"]

# tool =tools[tool_name]

# result= tool.invoke(args)

# print(result)
# print(response.tool_calls[0]["id"])



# print(langchain.__version__)
# print(langchain_core.__version__)
# print(langchain_groq.__version__)

builder=StateGraph(suming_numbers)

builder.add_node("tools",tool_node)




