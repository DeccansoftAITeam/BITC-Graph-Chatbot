# %% List the tools exposed to a Student MCP client.
import asyncio
from course_knowledge.mcp_servers import create_student_server

print([tool.name for tool in asyncio.run(create_student_server().list_tools())])
