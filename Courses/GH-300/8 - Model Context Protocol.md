**What is Model Context Protocol (MCP)**

An **MCP Server** (Model Context Protocol Server) is basically a *context provider* for AI tools like GitHub Copilot.

Its an Open Standard developed by **Anthropic**, supported by GitHub Copilot

**Why MCP Matters**

* **Access enterprise systems:** Databases, APIs, internal tools
* **Standardized integration:** One protocol, multiple data sources
* **Security & control:** Fine-grained permissions for AI access
* **Context enrichment:** AI gets real-time data from your systems

**MCP Architecture:**
The key participants in the MCP architecture are:

|  |  |
| --- | --- |
| **Arch Component** | **Example** |
| MCP Host | GitHub Copilot Chat Agent |
| MCP Client | Agent Tools |
| MCP Server | Copilot Tool Server |
| External Services | GitHub Repo, Slack, Local File System |
| LLM | GPT 5.2, Claude Opus, Claude Sonnet etc… |

![The Architectural Elegance of Model Context Protocol (MCP) - The ML  Architect](data:image/png;base64...)

* **MCP Server**: A program that expose specific functionalities, data sources, or tools to AI models through a standardized interface. These can run either locally or remotely.
* **MCP Client**: A component for every MCP Server that maintains a connection to an MCP server and **obtains context** from an MCP server for the MCP host to use.
* **MCP Host**: The AI powered applications like VS Code and Claude Desktop that coordinates and manages one or multiple MCP clients. When a user interacts with the AI model, the host enriches the model's context with relevant information from connected MCP servers. Examples MCP Host: VS Code or Claude Desktop
* **AI Model:** Based on the user's query and available tools, the AI model  which **MCP tools** to use. The **MCP client** then executes these tools via the appropriate MCP server.

**Without MPC**

1. User to Copilot to GPT5.2: What should be my clothing in Paris.
2. Result: AI might hallucinate and incorrect response.

**With MCP**

1. User to Copilot: What should be my clothing in Paris..
2. Copilot to GPT5.2: What should be my clothing in Paris.. + I have facility to fetch temperature based on city
3. GPT Response: Tell me what is temperature of Paris
4. Copilot call MCP Server Method => GetTemperature(paris) => MCP Server Returns 10C
5. Copilot to GPT = What should be my clothing in Paris. + I have facility to fetch temperature based on city + Temperature at Paris is: 10C
6. GPT = Wear so and so clothes...

**Copilot MCP Flow (Realistic Example)**

**Developer asks Copilot:** “Find similar auth logic and open a PR fixing the bug”

**What happens: Copilot asks → Claude decides → MCP Server executes → VS Code governs**

1. Copilot (MCP Client) interprets intent
2. Claude decides:
   * call search\_repo()
   * then create\_pull\_request()
3. MCP Server executes:
   * queries GitHub API
   * creates PR
4. Results returned to Copilot
5. Copilot summarizes in chat

**Using GitHub MCP Registry**

In Visual Studio Code, open the extensions panel by clicking the extensions icon in the sidebar

In the extensions search bar, click the filter icon and select **MCP Registry** from the dropdown.

**Configuring MCP Servers Manually**

* **A specific repository.** This enables you to share MCP servers with anyone who opens the project in Visual Studio Code. To do this, create a **.vscode/mcp.json** file in the root of your repository.

1. **Your personal instance of Visual Studio Code.** To do this, add the configuration to your **settings.json** file in Visual Studio Code. MCP servers configured this way will be available in all workspaces. **Goto Command and Search > MCP Servers**

**Example: Edit either .vscode/mcp.json or settings.json**

{

    "servers": {

        "io.github.ChromeDevTools/chrome-devtools-mcp": {

            "type": "stdio",

            "command": "npx",

            "args": [

                "--registry",

                "https://registry.npmjs.org",

                "chrome-devtools-mcp@0.17.0"

            ],

            "gallery": "https://api.mcp.github.com",

            "version": "0.17.0"

        },

        "microsoft/playwright-mcp": {

            "type": "stdio",

            "command": "npx",

            "args": [

                "@playwright/mcp@latest"

            ],

            "gallery": "https://api.mcp.github.com",

            "version": "0.0.1-seed"

        }

    },

    "inputs": []

}

1. Save and Start the MCP Servers

**MCP Server List in Copilot**

1. **GitHub MCP Server**: This is how Copilot understands your repo beyond just open files.
   * Repos Access, PRs / Issues / Commits, Code search & context building
   * Tools: search\_code, list\_pull\_requests, create\_pull\_request, get\_issue\_details
   * Example Prompt: “Analyze this repo and find issues in product creation logic.”
2. **Filesystem MCP Server**: Enables “refactor these files” or “generate tests across folders”.
   * Read/write local files safely
   * Tools: read\_file, write\_file, list\_directory
   * Example: “Fix the bug and add validation.”
3. **Shell / Process MCP Server**: *Used in Copilot Agent mode.*
   * Run commands (controlled)
   * Tools: run\_tests, run\_build, link\_project
4. **Database MCP Server**: Copilot can inspect schemas, generate migrations, debug queries.
   * SQL Server, MySQL, MongoDB
   * Tools: run\_query, get\_schema