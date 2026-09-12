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

**Using MCP Servers with Claude Desktop**

To use **MCP servers with Claude Desktop** and set up the provided MCP server configuration, follow these steps:

**1. Prerequisites**

* **Install Claude Desktop**: Download and install the Claude Desktop application if you haven't already.

<https://claude.ai/download>

* **Install Node.js**: MCP servers like the **filesystem server** require Node.js. Check if it’s installed by running node --version in your command prompt. If not, download and install it from the official Node.js website.

**2. Locate the Configuration File**

* **Windows**: The configuration file is located at
  %APPDATA%\Claude\claude\_desktop\_config.json
* **macOS**: The file is at
  ~/Library/Application Support/Claude/claude\_desktop\_config.json.

You can access this file via:

* Open Claude Desktop
* Go to **Settings > Developer**
* Click **Edit Config** to open the file in your default text editor.

**3. Update MCP Server Configuration file**

Replace or update the "mcpServers" section in your claude\_desktop\_config.json with your provided configuration:

{

"**mcpServers**": {

"**filesystem**": {

"command": "npx",

"args": [

"-y",

"@modelcontextprotocol/server-filesystem",

"C:\\Users\\**<Your Name>**\\Desktop",

"C:\\Users\\**<Your Name>**[\\Downloads](file:///%5C%5CDownloads)"

"<any folder>"

]

},

"**BestItCourses**": {

"command": "npx",

"args": ["mcp-remote", "https://dssbitcagent.azurewebsites.net/sse"]

}

}

}

* The **filesystem** server lets Claude access your Desktop and Downloads folders.
* The **BestItCourses** server connects to a remote MCP endpoint to fetch latest events, webinars and course details.

4. Save and Restart Claude Desktop

* Save the **claude\_desktop\_config.json** file.
* **Restart Claude Desktop** to load the new MCP server configurations (Use system tray).

5. Verify and Use MCP Servers

1. After restarting, open Claude Desktop.
2. Go to **Settings > Developer** or look for a hammer/plug icon indicating MCP servers are active.

![A screenshot of a computer  AI-generated content may be incorrect.](data:image/png;base64...)

1. In the Claude interface, use the **Search and tools** (toggle slider) to view and enable the connected MCP servers and their tools.

![A screenshot of a computer  AI-generated content may be incorrect.](data:image/png;base64...)

1. You can now interact with these servers using natural language prompts (e.g., “**search my downloads for images**”)

**Sample Prompts:**

1. Search my downloads for images
2. Get all webinars from bestitcourses
3. What is the size of largest image file

STDIO vs SSE

**1. STDIO (Standard Input/Output)**

* This is the **oldest, simplest way** for two programs to talk.
* One program writes text/data to **stdout** (standard output).
* The other reads it from **stdin** (standard input).
* It’s like passing notes back and forth through a single pipe.

**In MCP context:**

* The AI client and the MCP server (local) can run in the same process environment.
* They exchange JSON-RPC messages over **STDIO** streams (no network needed).
* Example: You run a local script that the AI calls as a tool — MCP just reads/writes JSON via STDIO.

**When to use STDIO**

* **Local development**: Your MCP server runs as a local script/program.
* **Lightweight tools**: Small utilities like file search, DB query, calculator, or custom scripts.
* **Security-sensitive**: No open network port → data stays within the process.
* **Fast prototyping**: Easiest to set up; just read/write JSON to stdin/stdout.

**2. SSE (Server-Sent Events)**

* A **web protocol** for sending continuous updates from a server to a client over HTTP.
* Unlike WebSockets (two-way), **SSE is one-way**: server → client.
* Good for **streaming data** (like logs, chat responses, live updates).

**In MCP context:**

* If your AI client is remote, it can connect to the MCP server over HTTP.
* The server **streams** results back using **SSE** so the model sees partial responses in real time.
* Example: An AI asks for stock prices → MCP server streams price updates via SSE.

**When to use SSE**

* **Remote services**: Your MCP server is hosted in the cloud or another machine.
* **Streaming results**: You want partial outputs (like logs, stock prices, or chat responses).
* **Scalable tools**: Multiple AI clients can connect over HTTP.
* **Integration with web APIs**: Natural fit since SSE is HTTP-based.

**In short:**

* **STDIO = local, simple, process-to-process communication.**
* **SSE = remote, streaming communication over HTTP.**

STDIO MCP Server (Console app in C#)

**1) New project + packages**

dotnet new console -n DemoMcpServer

cd **DemoMcpServer**

dotnet add package **ModelContextProtocol**

dotnet add package Microsoft.Extensions.Hosting

**2) Program.cs**

using Microsoft.Extensions.DependencyInjection;

using Microsoft.Extensions.Hosting;

using Microsoft.Extensions.Logging;

using ModelContextProtocol.Server;

using System.ComponentModel;

var builder = Host.CreateApplicationBuilder(args);

// Write logs to stderr (so stdout stays clean for JSON-RPC)

builder.Logging.AddConsole(o => o.LogToStandardErrorThreshold = LogLevel.Trace);

**builder.Services.AddMcpServer(options =>**

**{**

**options.ServerInfo = new() { Name = "DemoMcpServer", Version = "0.1.0" };**

**})**

    .WithStdioServerTransport()   // stdio transport (ideal for local dev)

    .WithToolsFromAssembly();     // scan this assembly for [McpServerTool]s

await builder.Build().RunAsync();

**[McpServerToolType]**

public static class **MathTools**

{

    [**McpServerTool**, Description("Bingo two integers")]

    public static int **Bingo**(

        [Description("First Number")] int a,

        [Description("Second Number")] int b) => a + b;

}

**[McpServerToolType]**

public static class **EchoTools**

{

    [**McpServerTool**, Description("Echoes the provided message back.")]

    public static string **Echo**([Description("Message to echo back")] string message)

        => $"Echo: {message}";

}

**3) Run and then Publish**

dotnet run

Nothing “prints” (stdout is reserved for JSON-RPC), but the process is ready for a client to connect over stdio.

Clients discover and call tools via tools/list and tools/call in the protocol.

**4) Test it (two easy options)**

**Option A) Inspector / CLI clients**

You can also poke your server with community tools like **MCP Inspector** or **mcptools** (list tools, call them against a stdio command)

npx @modelcontextprotocol/inspector -- dotnet run --project ./**DemoMcpServer**.csproj

**5) Debugging code of your MCP Server**

1. **Install extension**: Install the C# extension (**ms-dotnettools.csharp**) in VS Code and reload the window
2. Create launch profile: ( .vscode/launch.json)

{

  "version": "0.2.0",

  "configurations": [

    {

      "name": ".NET: Attach",

      "type": "coreclr",

      "request": "attach",

      "processId": "${command:pickProcess}"

    }

  ]

}

1. Open a Terminal and execute following command to the MCP Inspector

npx @modelcontextprotocol/inspector -- dotnet run --project ./

1. Open Run and Debug (Ctrl+Shift+D), pick .NET: Attach, then click the green play. The process picker will show running processes — choose the correct one - **DemoMCPServer**

![](data:image/png;base64...)

1. **Put the break point in Code**
2. **Go to MCP Inspector in Browser 🡪 Connect 🡪 List Tools 🡪 Select a Tool and run.**

**Option B) VS Code + GitHub Copilot (recommended)**

a) Publish the MCP Server Project

mkdir d:\temp

mkdir d:\temp\mcp

dotnet publish DemoMcpServer.csproj -o d:\temp\mcp

b) Create **.vscode/mcp.json** in your project with:

{

  "servers": {

    "DemoMcpServer": {

      "type": "stdio",

      "command": "d:\\temp\\mcp\\DemoMCPServer.exe",

      "args": [],

      "env": {}

    }

  }

}

**Note: Path of Global JSON file:** C:\Users\<Username>\AppData\Roaming\Code\User\**mcp.json**

b) Open Copilot Chat → “Select tools” → you should see your server/tools. Try: “Using **#Bingo**, get result for 2 and 3.”
Note: You can pick the **tool** from the list or reference it by name with **Bingo**

Using Local MCP Server in Python Client

**Following is the code to use MCP Server in a regular Python Client Application**

import asyncio

import json

from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio\_client

from mcp.shared.exceptions import McpError

async def main():

    # Configure the server (mirrors your JSON config)

    server\_params = StdioServerParameters(

        command=r"d:\\temp\\mcp\\DemoMCPServer.exe",

        args=[],

        env=None

    )

    # Connect to the MCP server via stdio

    async with stdio\_client(server\_params) as (read\_stream, write\_stream):

        async with ClientSession(read\_stream, write\_stream) as session:

            # Initialize the connection (handshake)

            await session.initialize()

            # 1. List available tools

            tools\_result = await session.list\_tools()

            print("Available Tools:")

            for tool in tools\_result.tools:

                print(f"  - {tool.name}: {tool.description}")

            # 2. List available resources (if any)

            print("\nAvailable Resources:")

            try:

                resources\_result = await session.list\_resources()

                if not resources\_result.resources:

                    print("  - (none)")

                for resource in resources\_result.resources:

                    print(f"  - {resource.uri}: {resource.name}")

            except McpError as e:

                if "resources/list" in str(e):

                    print("  - (server does not support resources/list)")

                else:

                    raise

            # 3. List available prompts (if any)

            print("\nAvailable Prompts:")

            try:

                prompts\_result = await session.list\_prompts()

                if not prompts\_result.prompts:

                    print("  - (none)")

                for prompt in prompts\_result.prompts:

                    print(f"  - {prompt.name}: {prompt.description}")

            except McpError as e:

                if "prompts/list" in str(e):

                    print("  - (server does not support prompts/list)")

                else:

                    raise

            # 4. Call a tool (replace with your actual tool name and args)

            result = await session.call\_tool(

                name="bingo",

                arguments={"a": 5, "b": 3}

            )

            print(f"\nTool Result: {result.content}")

if \_\_name\_\_ == "\_\_main\_\_":

    asyncio.run(main())

Using MCP with OpenAI API

**The Schema of Tools used in MCP Server and OpenAI are not same and if the client app is using OpenAI API we have to convert the Schema from MCP to OpenAI format**

|  |  |
| --- | --- |
| **MCP Tool Schema** | **OpenAI Tool Schema** |
| {    "name": "get\_news",    "description": "Retrieve the latest news articles on a given topic.",  **"input\_schema":** {      "type": "object",      "properties": {        "topic": {          "type": "string",          "description": "The topic to search news articles for."        }      },      "required": ["topic"]    }  } | {      "name": "get\_news",      "description": "Retrieve the latest news articles on a given topic.",  **"parameters":** {          "type": "object",          "properties": {              "topic": {                  "type": "string",                  "description": "The topic to search news articles for.",              }          },          "required": ["topic"],      },  } |

**Execute the following commands:**

mkdir pythondemos

cd pythondemos

python -m venv venv

.\venv\Scripts\Activate

pip install mcp openai

code .

**Note: Don’t use Console.Out because that can interfere with JSON-RPC**

**mcp\_chat\_client.py**

import asyncio,  json,  os

from typing import Dict, Any

from openai import OpenAI

# MCP types and helpers for stdio-based MCP servers

from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio\_client

# Model to use for chat completions

MODEL = "gpt-5.2"

# Path to your compiled .NET MCP server executable. Update to your actual location.

DOTNET\_SERVER\_CMD = "D:\\temp\\mcp\\DemoMcpServer.exe"

# Arguments to pass to the server process. Use a list (e.g. ["--port", "5000"]) or [] when none.

DOTNET\_SERVER\_ARGS = []

#Utilitiy Function

def **mcp\_tools\_to\_openai\_schema**(tools):

    oa\_tools = []

    for t in tools.tools:

        # Map MCP tool -> OpenAI function-style tool

        oa\_tools.append({

            "type": "function",

            "function": {

                "name": t.name,

                "description": t.description or "",

                # Provide a safe default JSON schema if none is supplied

                "parameters": t.inputSchema or {"type": "object", "properties": {}},

            },

        })

    return oa\_tools

async def **run\_chat\_with\_mcp**(prompt: str) -> str:

    # Create an OpenAI client instance (uses env var OPENAI\_API\_KEY by default)

    client = OpenAI()

    # 1) Prepare parameters to launch/connect to your MCP server over stdio.

    server\_params = StdioServerParameters(

        command=DOTNET\_SERVER\_CMD,  # path to server executable

        args=DOTNET\_SERVER\_ARGS,    # list of command-line args for the server

        env=os.environ.copy()       # inherit current environment (copy to avoid mutation)

    )

    # 2) Open an stdio-based client to the MCP server. The stdio\_client context returns

    #    a (read, write) pair used by the MCP ClientSession to communicate with the server.

    async with stdio\_client(server\_params) as (read, write):

        async with ClientSession(read, write) as session\_between\_mcp\_client\_and\_server:

            # 3) Initialize the session and ask the server which tools it exposes

            await session\_between\_mcp\_client\_and\_server.initialize()     # handshake / service discovery

            tools = await session\_between\_mcp\_client\_and\_server.list\_tools()  # list available MCP tools

            # 4) Convert MCP tool schemas into the OpenAI 'function' tool format

            openai\_tools = mcp\_tools\_to\_openai\_schema(tools)

            # 5) Prepare initial message history for the chat completion request

            messages = [

                {"role": "system", "content": "You can call tools when useful."},

                {"role": "user", "content": prompt},

            ]

            # 6) Chat loop: request completions and handle any tool calls the model requests

            while True:

                # Send chat completion request to OpenAI, providing tool definitions

                resp = **client.chat.completions.create**(

                    model=MODEL,

                    messages=messages,

                    tools=openai\_tools,   # expose tools to the model so it may call them

                )

                # The model's assistant message is present in resp.choices[0].message

                msg = resp.choices[0].message

                tool\_calls = msg.tool\_calls or []  # tool calls requested by the model

                # If no tool calls were requested, return the assistant's content as final

                if not tool\_calls:

                    return msg.content or ""

                # The assistant message that requested tool calls can be re-appended

                messages.append(msg)  # add assistant turn to the conversation history

                # 7) Execute each tool call by invoking the MCP server

                for tc in tool\_calls:

                    fn = tc.function

                    name = fn.name  # tool name requested by the model

                    args = json.loads(fn.arguments or "{}")  # parse JSON arguments

                    # Execute the tool on the MCP server and get the result

                    result = await session\_between\_mcp\_client\_and\_server.call\_tool(name, arguments=args)

                    # Add the tool's output back into the conversation as a 'tool' role

                    messages.append({

                        "role": "tool",

                        "tool\_call\_id": tc.id,

                        "content": result.content[0].text

                    })

# Example use:

if \_\_name\_\_ == "\_\_main\_\_":

    print(asyncio.run(run\_chat\_with\_mcp("Bingo a=5 and b=9 using the math tool, then echo 'sum complete'.")))

Remote MCP SSE Server (ASP.NET Core)

Prefer an HTTP transport (e.g., for remote or decoupled testing)?

**1) Create a Project**

dotnet new **web** -n DemoMcpHttp

cd DemoMcpHttp

dotnet add package **ModelContextProtocol.AspNetCore**

**2) Program.cs**

This uses the **ModelContextProtocol.AspNetCore** package and adds an **HTTP/SSE** endpoint that many hosts can connect to.

using ModelContextProtocol.Server;

using System.ComponentModel;

var builder = WebApplication.CreateBuilder(args);

builder.Services.**AddMcpServer**(options =>

    {

        options.ServerInfo = new() { Name = "DemoMcpHttp", Version = "0.1.0" };

    })

    .WithHttpTransport()

    .WithToolsFromAssembly();

var app = builder.Build();

**app.MapMcp();**                     // expose MCP endpoints (SSE)

app.Run("http://localhost:3001"); // choose a port

// Same tool classes as before:

**[McpServerToolType]**

public static class EchoTools

{

    [**McpServerTool**, Description("Echoes the provided message back.")]

    public static string Echo([Description("Message to echo back")] string message)

        => $"Echo: {message}";

}

**Testing the Remote MCP Server.**

**3) Add the following to:**

**Open VS Code 🡪.vscode/mcp.json #Repository and Shared by all Users having access to the Repository**

**OR**

C:\Users\<Username>\AppData\Roaming\Code\User\**mcp.json #Used by Current Logged-In User only**

{

    "servers": {

        "**MyDemoServer**": {

            "url": "http://localhost:3001/sse",

            "type": "http"

        },

    },

    "inputs": []

}

4) Try the prompts in VS Code

**Following can be used in Claude Desktop:**

{

  "mcpServers": {

    "filesystem": {

      "command": "npx",

      "args": [

        "-y",

        "@modelcontextprotocol/server-filesystem",

        "D:\\Courses\\AI\\"

      ]

    },

    "BestItCourses": {

      "command": "npx",

      "args": ["mcp-remote", "https://dssbitcagent.azurewebsites.net/sse"]

    },

    "MyEchoMCPServer": {

      "command": "npx",

      "args": ["mcp-remote", "https://localhost:3001/sse"]

    }

  }

}

Using Remote MCP in OpenAI Chat Completion API

Python Host - Demo.py

import asyncio, json, os

from typing import Any, Dict, List

# Import OpenAI Python SDK

from openai import OpenAI

# Import MCP client and types for tool integration

from mcp import ClientSession, types

from mcp.client.sse import sse\_client

# If your C# server exposes Streamable HTTP instead of SSE, use:

# from mcp.client.streamable\_http import streamablehttp\_client

OPENAI\_MODEL = os.getenv("OPENAI\_MODEL", "gpt-5")

MCP\_URL =  "http://localhost:3001/sse"

# MCP\_URL =  "https://dssbitcagent.azurewebsites.net/sse"

# If using Streamable HTTP, typical path is /mcp per SDK docs:

# MCP\_URL = "http://localhost:3001/mcp"  # and swap the client factory below

# Create OpenAI client instance

client = OpenAI()

def mcp\_tools\_to\_openai(tools):

    oa\_tools = []

    for t in tools.tools:

        # Map MCP tool -> OpenAI function-style tool

        oa\_tools.append(

            {

                "type": "function",

                "function": {

                    "name": t.name,

                    "description": t.description or "",

                    # Provide a safe default JSON schema if none is supplied

                    "parameters": t.inputSchema or {"type": "object", "properties": {}},

                },

            }

        )

    return oa\_tools

async def run\_chat\_with\_mcp(user\_prompt: str) -> str:

    # Connect to your ASP.NET Core MCP server over SSE.

    # (If using Streamable HTTP, swap to: `streamablehttp\_client(MCP\_URL)`).

    async with sse\_client(MCP\_URL) as (read,write):  # Establish SSE connection to MCP server

        async with ClientSession(read, write) as session:

            await session.initialize()  # Initialize session (handshake/setup)

            # Discover tools and expose them to the OpenAI model

            tools = await session.list\_tools()  # Get available MCP tools

            # 4) Convert MCP tool schemas into the OpenAI 'function' tool format

            openai\_tools = mcp\_tools\_to\_openai(tools)

            # Initial message history for OpenAI chat

            messages = [

                {"role": "system","content": "You can use tools when helpful."},

                {"role": "user", "content": user\_prompt},

            ]

            while True:

                # Request a chat completion from OpenAI, passing available tools

                resp = client.chat.completions.create(

                    model=OPENAI\_MODEL,

                    messages=messages,

                    tools=openai\_tools,

                )

                msg = resp.choices[0].message  # Get model's response message

                tool\_calls = msg.tool\_calls or []  # Get any tool calls requested by model

                # If the model didn't request any tool calls, we're done

                if not tool\_calls:

                    return msg.content or ""  # Return final answer

                # The assistant message that requested tool calls can be re-appended

                messages.append(msg)  # add assistant turn to the conversation history

                # 7) Execute each tool call by invoking the MCP server

                for tc in tool\_calls:

                    fn = tc.function

                    name = fn.name  # tool name requested by the model

                    args = json.loads(fn.arguments or "{}")  # parse JSON arguments

                    # Execute the tool on the MCP server and get the result

                    print(f"Calling tool {name} with args {args}")

                    result = await session.call\_tool(name, arguments=args)

                    # Add the tool's output back into the conversation as a 'tool' role

                    messages.append({

                        "role": "tool",

                        "tool\_call\_id": tc.id,

                        "content": result.content[0].text

                    })

if \_\_name\_\_ == "\_\_main\_\_":

    # Entry point for running the demo

    prompt = "List all AI courses"  # Example user prompt

    print(asyncio.run(run\_chat\_with\_mcp(prompt)))  # Run the chat loop and print result

MCP Server as Wrapper over OpenAPI (Not OpenAI)

**Key differences between MCP and REST API:**

|  |  |  |
| --- | --- | --- |
| **Feature** | **MCP Server** | **REST API** |
| **Target User** | Designed for AI agents (LLMs) | Designed for developers and their applications |
| **State Management** | **Stateful**: Remembers context (e.g., conversation, workflow state) | **Stateless**: Each request is independent; context must be resent each time |
| **Integration Approach** | Provides a **unified, AI-friendly interface** to multiple tools/services | Each service exposes its own API, often requiring custom code per integration |
| **Use Case** | Ideal for AI-driven, dynamic, multi-tool integrations | Ideal for predictable, well-defined service boundaries |

The **awslabs.openapi-mcp-server** is an executable (a command-line tool or server) provided by AWS Labs that implements the OpenAPI MCP (Model Conversion Protocol). Its main purpose is to act as a backend server that can process OpenAPI specifications and expose API endpoints for interacting with those specs.

**Typical use cases:**

* Validating OpenAPI specs
* Generating code or documentation from specs
* Providing a local server for API development/testing

**Rest API:** <https://petstore3.swagger.io/>

**Swagger Metadata:** <https://petstore3.swagger.io/api/v3/openapi.json>

**Use openapi-mcpserver-generator**

mkdir D:\mcpdemo\

cd D:\mcpdemo\

**# Local MCP Server**

npm install -g openapi-mcpserver-generator

openapi-mcpserver-generator --openapi https://petstore3.swagger.io/api/v3/openapi.json --output ./petstore-mcp

OR

**# Remote MCP Server**

# npm install -g openapi-mcp-generator
# openapi-mcp-generator --input https://petstore3.swagger.io/api/v3/openapi.json --output ./petstore-mcp-http --transport http

**# Install dependencies**

cd petstore-mcp

npm install

**This generates a complete MCP server with tools for each API endpoint, plus the MCP server configuration**

**Testing the Petstore MCP Server in VS Code**

In your project root (or workspace), create .vscode/mcp.json:

{

"servers": {

"petstore": {

"command": "node",

"args": ["D:\\mcpdemo\\petstore-mcp\\server.js"]

}

}

}

**Test it using the prompt:**

Find all available pets in the store

Get the pet with ID 1