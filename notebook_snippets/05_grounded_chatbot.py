# %% Call the same grounded service used by FastAPI and MCP.
from course_knowledge.services import CourseKnowledgeService

response = CourseKnowledgeService().ask("How is MCP related to GitHub Copilot?", moderate=True)
print(response["answer"])
print(response.get("citations"))
