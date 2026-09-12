# %% After cloning the repository, create the student MCP executable.
# py -m venv .venv
# .\.venv\Scripts\Activate.ps1
# python -m pip install -e .
from pathlib import Path
print(Path('.venv/Scripts/course-knowledge-student-mcp.exe').exists())
