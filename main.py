from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from prompts.system import system_prompt
from langchain_core.messages import HumanMessage


# Custom tools that we will use. These are pulled from our tools.py
from tools import save_tool, scrape_tool, search_tool

class LeadResponse(BaseModel):
    company: str
    contact_info: str
    email: str
    summary: str
    outreach_message: str
    tools_used: list[str]

class LeadResponseList(BaseModel):
    leads: list[LeadResponse]

llm = ChatOllama(model="glm-5:cloud")
parser = PydanticOutputParser(pydantic_object=LeadResponseList)
tools = [save_tool, scrape_tool, search_tool]
checkpoint = MemorySaver()
system_prompt = system_prompt.format(format_instructions=parser.get_format_instructions())

agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpoint,
    system_prompt=system_prompt
)

config = {"configurable": {"thread_id": "conversation1"}}

result = agent.invoke(
    {"messages": [HumanMessage(content="Find 5 local small businesses in Vancouver, British Columbia, that might need IT services and provide detailed information about them.")]}, 
    config
)

print(result["messages"][-1].content)