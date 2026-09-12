**Copilot CLI**

* Copilot CLI is a **command-line tool** that brings AI-powered assistance to your terminal.
* **Copilot CLI bridges the gap between natural language and command-line expertise**, making terminal workflows accessible to all skill levels.
* Junior developers can operate at the level of seniors because Copilot fills the knowledge gap. Seniors become more productive because they don't waste time remembering obscure flags and syntax.

**Installation and basic usage**:

gh extension install github/gh-copilot

Requires:

* PowerShell 7 (Install from <https://aka.ms/powershell>)
* [GitHub CLI (gh) installed](https://cli.github.com/) (<https://cli.github.com/>).

**Two Operating Modes:**

**1. Interactive Mode (Default)**

**copilot**

*# Opens persistent chat session*

*# Maintains context throughout*

**2. Programmatic Mode (Single command)**

**copilot -p "Create a React component for user login"**

***# With auto-approval***

**copilot -p "Fix all ESLint errors" --allow-all-tools**

***# Pipe from script***

**./my-script.sh | copilot**

**Slash Commands:**

/login # Authenticate with GitHub

/logout # Sign out

/context #Context usage

/exit # End session

/clear # Clear conversation history

/model # Switch AI models (Claude, GPT, Gemini)

/experimental # Enable experimental features

**Information & Debugging:**

/usage # Show premium requests used, context length

/share # Save session as Markdown or GitHub Gist

/feedback # Submit feedback to GitHub

/help # Show all commands

/lsp # Show Language Server Protocol config

**Workflow Commands**

/delegate <task> *# Send task to Copilot Coding Agent (creates PR)*

**Key features and use cases**:

1. **Command Execution:**

find all files modified in last 7 days

1. **Command Explanation**:

**explain** tar -xzvf archive.tar.gz

1. **Script Creation**:

Create a bash script that backs up my home directory to Azure Storage daily

1. **DevOps Workflows**:

Common tasks Copilot CLI excels at:

* **Docker commands** and Dockerfile generation
* **Kubernetes kubectl** operations
* **CI/CD pipeline** debugging
* **Git advanced operations** like rebasing, cherry-picking, and complex merges

**Examples:**

**# Launch in project directory**

cd my-new-project

copilot

**# Your prompts:**

You: Explain the layout of this project

You: What dependencies does this use?

You: Show me the main entry point and explain the flow

You: Find all TODO comments in the codebase

**Example: Fixing a Bug**

You: The login endpoint is returning 500 errors. Investigate and fix the issue.

**Copilot will:**

# 1. Check logs

# 2. Examine the endpoint code

# 3. Identify the problem (e.g., missing error handling)

# 4. Propose a fix

# 5. Apply changes (with your approval)

# 6. Run tests to verify

**Example: Development Workflow**

You: What process is using port 8080? Kill it and verify.

You: Install all dependencies listed in package.json

You: Run the test suite and fix any failing tests

You: Generate API documentation from the code

You: Create a migration to add email\_verified column to users table

**Example: Feature Implementation using Fleet mode.**

**Press Shift + Tab and switch to Plan mode.**

**Run the Prompt:**

You: Add rate limiting to all API endpoints.

Use express-rate-limit library.

Requirements:

- 100 requests per 15 minutes per IP

- Return 429 status when exceeded

- Include X-RateLimit headers

**Exit plan mode and manually run the following prompt**

**/fleet implement the plan**

**Note: Use the /tasks slash command to see a list of background tasks for the current session, including any subtasks handled by subagents.**

**You can press *Enter* to view details, k to kill a process, and r to remove completed or killed subtasks from the list**

**About Pricing:**

Each subagent can interact with the LLM independently of the main agent, so splitting work into smaller parallel tasks may result in more LLM interactions than if handled by the main agent. **Using /fleet may therefore consume more premium requests**.