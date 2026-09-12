What is MCP?

An **MCP server** (Model Context Protocol server) is a system designed to act as an interface layer between AI agents and external tools or services.

**MCP is an Open standard** for connecting AI assistants to external data sources and tools.

Developed by **Anthropic**.

MCP serves acts as a universal interface that enables AI models to interact with external systems, ranging from cloud platforms like GitHub and Slack to enterprise databases and local files, without requiring custom integrations for each new data source or tool.

**Before MCP, integrations were:**

* **Ad-hoc** (different plugin systems: ChatGPT Plugins, LangChain, custom APIs).
* **Insecure** (models could over-request, leak keys, etc.).
* **Not portable** (a plugin for one system wouldn’t work in another).

**MCP solves this by being:**

* **Open standard** (like HTTP for web).
* **Safe** (clear permissions + sandboxing).
* **Portable** (one MCP server can connect to multiple AI clients).

![How MCP solves the MxN integration problem. Source: SalesforceDevops](data:image/png;base64...)

**MCP provides:**

* **A growing list of pre-built integrations** that your LLM can directly plug into
* **A standardized way** to build custom integrations for AI applications
* **An open protocol** that everyone is free to implement and use
* **The flexibility to change** between different apps and take your context with you

**MCP Architecture:**
The key participants in the MCP architecture are:

* **MCP Server**: A program that expose specific functionalities, data sources, or tools to AI models through a standardized interface. These can run either locally or remotely.
* **MCP Client**: A component for every MCP Server that maintains a connection to an MCP server and **obtains context** from an MCP server for the MCP host to use.
* **MCP Host**: The AI powered applications like VS Code and Claude Desktop that coordinates and manages one or multiple MCP clients. When a user interacts with the AI model, the host enriches the model's context with relevant information from connected MCP servers. Examples MCP Host: VS Code or Claude Desktop
* **AI Model:** Based on the user's query and available tools, the AI model decides which **MCP tools** to use. The **MCP client** then executes these tools via the appropriate MCP server.

![](data:image/png;base64...)

![The Architectural Elegance of Model Context Protocol (MCP) - The ML  Architect](data:image/png;base64...)

|  |  |
| --- | --- |
| **Arch Component** | **Example** |
| Host Appplication | VS Code |
| MCP Client | GitHub Copilot Agent |
| MCP Server | Copilot Tool Server |
| External Services | GitHub Repo, Slack, Local File System |
| LLM | GPT 5.2, Claude Opus, Claude Sonnet etc… |

**Copilot MCP Flow (Realistic Example)**

**Developer asks Copilot:** “Find similar auth logic and open a PR fixing the bug”

**What happens:**

1. Copilot (MCP Client) interprets intent
2. Claude Sonnet decides:
   * call search\_repo()
   * then create\_pull\_request()
3. MCP Server executes:
   * queries GitHub API
   * creates PR
4. Results returned to Copilot
5. Copilot summarizes in chat

STDIO MCP Server (Console app in C#)

**Create server.py**

from mcp.server.mcpserver import MCPServer

# Create an STDIO/HTTP MCP server

mcp = MCPServer("Demo")

# Add an addition tool

**@mcp.tool()**

def **add**(a: int, b: int) -> int:

    """Add two numbers"""

    return a + b

**@mcp.tool()**

def **subtract**(a: int, b: int) -> int:

    """Subtract two numbers"""

    return a - b

**@mcp.tool()**

def multiply(a: float, b: float) -> float:

    """Multiply two numbers together and return the result."""

    return a \* b

**@mcp.tool()**

def **divide**(a: float, b: float) -> float:

    """

    Divide a by b and return the result.

    Raises: ValueError: If b is zero

    """

    if b == 0:

        raise **ValueError**("Cannot divide by zero")

    return a / b

# Add a dynamic greeting resource

**@mcp.resource**("greeting://{name}")

def get\_greeting(name: str) -> str:

    """Get a personalized greeting"""

    return f"Hello, {name}!"

# Main execution block - this is required to run the server

if **\_\_name\_\_ == "\_\_main\_\_":**

    mcp.run(transport="stdio")  #local

    #mcp.run(transport="streamable-http")  #remote

1. **🡪 List Tools 🡪 Select a Tool and run.**

**stdio\_client.py**

import asyncio

import sys

from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio\_client

async def main() -> None:

    # Launch the local MCP server over stdio.

    server\_params = StdioServerParameters(

        command="python",

        args=["server.py"],

    )

    async with stdio\_client(server\_params) as (read\_stream, write\_stream):

        async with ClientSession(read\_stream, write\_stream) as session:

            await session.initialize()

            result = await session.**call\_tool**("add", {"a": 5, "b": 7})

            print("add(5, 7) =", result.content[0].text)

            greeting = await session.**read\_resource**("greeting://Alice")

            print("greeting://Alice =", greeting.contents[0].text)

if \_\_name\_\_ == "\_\_main\_\_":

    asyncio.run(main())

Key difference: tools return **.content**, resources return **.contents** (plural).

**If Streamable HTTP is used:**

**http\_client.py**

import asyncio

from mcp import ClientSession

from mcp.client.streamable\_http import streamable\_http\_client

async def main() -> None:

    # Default FastMCP streamable-http endpoint is /mcp.

    async with streamable\_http\_client("http://localhost:8000/mcp") as (

        read\_stream,

        write\_stream,

        \_get\_session\_id,

    ):

        async with ClientSession(read\_stream, write\_stream) as session:

            await session.initialize()

            result = await session.call\_tool("add", {"a": 5, "b": 7})

            print("add(5, 7) =", result.content[0].text)

            greeting = await session.read\_resource("greeting://Alice")

            print("greeting://Alice =", greeting.contents[0].text)

if \_\_name\_\_ == "\_\_main\_\_":

    asyncio.run(main())

The pattern is identical — just swap the transport context manager. The HTTP client hits /mcp by default on the streamable-http server.

**Terminal 1:** Run the Server

uv run server.py

**Terminal 2:** Run the Client

**uv run http\_client.py**

Using MCP with OpenAI API

**The Schema of Tools used in MCP Server and OpenAI are not same and if the client app is using OpenAI API we have to convert the Schema from MCP to OpenAI format**

|  |  |
| --- | --- |
| **MCP Tool Schema** | **OpenAI Tool Schema** |
| {    "name": "get\_news",    "description": "Retrieve the latest news articles on a given topic.",  **"input\_schema":** {      "type": "object",      "properties": {        "topic": {          "type": "string",          "description": "The topic to search news articles for."        }      },      "required": ["topic"]    }  } | {      "name": "get\_news",      "description": "Retrieve the latest news articles on a given topic.",  **"parameters":** {          "type": "object",          "properties": {              "topic": {                  "type": "string",                  "description": "The topic to search news articles for.",              }          },          "required": ["topic"],      },  } |

**Execute the following commands:**

pip install mcp openai

**Note: Don’t use Console.Out because that can interfere with JSON-RPC**

import asyncio

import json

import os

from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio\_client

from openai import OpenAI

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI(api\_key=os.getenv("OPENAI\_API\_KEY"))

from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio\_client

async def main() -> None:

    # Launch the local MCP server over stdio.

    server\_params = StdioServerParameters(

        command="python",

        args=["math\_server.py"],

    )

    async with stdio\_client(server\_params) as (read\_stream, write\_stream):

        async with ClientSession(read\_stream, write\_stream) as session:

            await session.initialize()

            inputs = [

                {

                    "role": "user",

                    "content": "what is sum of 2 and 3 and multiplication of 4 and 5.",

                }

            ]

            mcp\_tools = await session.list\_tools()

            openai\_tools = [

                {

                    "type": "function",

                    "name": tool.name,

                    "description": tool.description,

                    "parameters": tool.input\_schema,

                }

                for tool in mcp\_tools.tools

            ]

            previous\_response\_Id = None

            while True:

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    input=inputs,

                    previous\_response\_id=previous\_response\_Id,

                    tools= openai\_tools,

                )

                previous\_response\_Id = response.id

                if response.output\_text:

                    print(response.output\_text)

                    break

                inputs = []

                for item in response.output:

                    if item.type == "function\_call":

                        args = json.loads(item.arguments)

                        result = await session.call\_tool(item.name, args)

                        # if item.name == "get\_weather":

                        #     result = get\_weather(args["latitude"], args["longitude"])

                        # elif item.name == "get\_news":

                        #     result = get\_news(args["topic"])

                        inputs.append(

                            {

                                "type": "function\_call\_output",

                                "call\_id": item.call\_id,

                                "output": str(result),

                            }

                        )

if \_\_name\_\_ == "\_\_main\_\_":

    asyncio.run(main())