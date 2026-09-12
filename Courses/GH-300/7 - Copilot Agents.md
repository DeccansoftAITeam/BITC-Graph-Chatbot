**Overview**

* Agents perform complete coding tasks end-to-end. They understand your project, make changes across multiple files, run commands, and adapt based on the results.
* You give an agent a high-level task, and it breaks the task down into steps, executes those steps with tools, and self-corrects when it hits errors.
* For example, imagine you have a failing test. Instead of suggesting a fix, an agent can:
  1. Read the error message and identify the root cause across multiple files
  2. Update the relevant code
  3. Run the tests again to verify the fix works
  4. Commit the changes
* You can run multiple agent sessions in parallel, each focused on a different task.

**Use tools with Agents**

Tools extend agents in Visual Studio Code with specialized functionality for accomplishing specific tasks like searching code, running commands, fetching web content, or invoking APIs.

**Types of Tools:**

* + **Built-in tools:** These are automatically available in chat. These tools cover common development tasks and are optimized for working within your workspace.
  + **Model Context Protocol (MCP) tools**: Enables AI models to use external tools and services through a unified interface.
  + **Extension tools:** VS Code extensions can contribute tools that integrate deeply with the editor. Automatically available with extensions when you install them.

To Configure: Select the **Configure Tools** button in the chat input field.

**Use tools in Prompt:**

* The agent autonomously chooses and invokes relevant tools as needed to accomplish the task.
* You can also explicitly reference tools in your prompts by typing # followed by the tool name

Examples:

* "Summarize the content from **#fetch** https://code.visualstudio.com/updates"
* "How does routing work in Next.js? **#githubRepo** vercel/next.js"
* "Explain the authentication flow **#codebase**"

**Note: Some tools require your approval before they can run.**

**Agent Types**

1. **Local Agents:**

* Local agents run directly within VS Code on your machine. Use local agents for interactive tasks that require immediate feedback, such as brainstorming, planning, or exploratory work.
* Local agent sessions use:

1. **Agent** for complex coding tasks
2. **Plan** for creating structured implementation plans,
3. **Ask** for answering questions about your codebase.
4. **Custom Agents** for specialized workflows
5. **Background Agents:**
   * Background agents, like Copilot CLI, are CLI-based agents that run non-interactively in the background on your local machine.
   * They use Git worktrees to work isolated from your main workspace, preventing conflicts with your active work.
   * You can send follow-up prompts to the background agent to make adjustments or improvements to the feature.
6. **Cloud Agents:**

* Cloud agents, like Copilot coding agent, run on remote infrastructure and integrate with GitHub repositories and pull requests for team collaboration and code reviews.

**Examples:**

|  |  |
| --- | --- |
| **I want to...** | **Use** |
| Brainstorm, explore, or iterate on an idea interactively | Local agent |
| Get answers about my codebase | Local agent (Ask) |
| Create a structured implementation plan | Local agent (Plan) |
| Fix an issue that needs editor context (test failures, linting errors, debug output) | Local agent |
| Use specific VS Code extension tools or MCP servers | Local agent |
| Implement a well-defined task while I keep working | Background agent or Cloud agent |
| Explore multiple variants or proof of concepts | Background agent or Cloud agent |
| Create a PR for team review and collaboration | Cloud agent |
| Assign a GitHub issue to an agent | Cloud agent |
| Use a specific AI provider (Anthropic, OpenAI) | Third-party agent |

**Copilot Coding Agent**

This is an autonomous AI developer that works in the background on GitHub's infrastructure:

**How to use it:**

1. **Assign work to the agent:**
   * **From GitHub Issues:** Assign any issue directly to @copilot as the assignee
   * **From VS Code:** During a chat session, use the "Delegate to coding agent" action or type #copilotCodingAgent
   * **From TODO comments:** Click the light bulb icon on TODO comments and select "Delegate to coding agent"
   * **From multiple platforms:** GitHub Mobile, GitHub CLI, Slack, Teams, Linear, Azure Boards
2. **How it works:**
   * Creates a pull request immediately (with initial empty commit)
   * Works in an isolated GitHub Actions environment
   * Pushes incremental commits as it develops the solution
   * Requests your review when complete
   * You can iterate by commenting on the PR

**Best for:** Tasks you can delegate and review later - fixing bugs, adding features, refactoring, documentation, handling backlog items

Example: "Add unit tests for this module" or "Fix this security alert"

**Key Differences with Agent Mode in VS Code**

|  |  |  |
| --- | --- | --- |
| **Feature** | **Coding Agent (GitHub)** | **Agent Mode (VS Code)** |
| **Execution** | Cloud (GitHub Actions) | Local (your workspace) |
| **Interaction** | Asynchronous | Synchronous |
| **Integration** | Pull requests & issues | Editor & chat |
| **Best Use** | Background tasks | Interactive coding |

The GitHub team themselves uses both - coding agent for smaller, well-defined tasks in their 200+ repositories, and agent mode for interactive development and prototyping.

**Example Walkthrough: Basic Task Delegation**

1. Goto GitHub.com and Select your Repository
2. Create a GitHub Issue
   1. Provide the Title: Provide documentation for the python files.
   2. Description: Use JSDoc standards and provides comprehensive information about each component's purpose, parameters, and behavior, making the codebase more maintainable and easier for developers to understand.
3. Assign the Issue to GitCopilot
   1. Click on "Assignees" → Select "Copilot"
   2. - Or comment: `@copilot please implement this`

What happens

* Agent creates a PR immediately (with empty initial commit)
* Works in isolated GitHub Actions environment
* Pushes incremental commits as it develops
* Requests your review when complete 4.

1. Review the PR:
   1. Check the documentation generated
   2. Comment if changes needed: “@copilot please add information about parameters types”
2. Review and Complete the Pull Request.

**Exercise 2: Delegating from VS Code Chat:**

1. In Chat Window, Click button Next to + 🡪 Select **Cloud** (Delegate to coding agent)
2. **Prompt**: I need to refactor our database queries to use connection pooling. Currently we're opening a new connection for each query which is inefficient. Create a connection pool and update all queries to use it.

**What happens:**

* 1. Entire chat context transfers to Coding Agent
  2. PR created with detailed description
  3. Agent works autonomously in background
  4. You continue working on other tasks

1. Comple the Pull Request after review.

**Example 2: Multi-Issue Assignment
Scenario: End of sprint cleanup - assign multiple small tasks**

1. **Issues to create and assign to Copilot:**

#1: Add JSDoc comments to all public methods in src/utils/

#2: Update dependencies with minor version updates

#3: Fix all ESLint warnings in src/components/

#4: Add missing unit tests for DateFormatter class

#5: Replace console.log with proper logging using winston

1. **Assign all 5 to Copilot at once**

* Agent works on them in parallel
* Creates separate PR for each
* You review in order of completion

**Hand off a session to another agent**

You can hand off an existing task from one agent to another agent to take advantage of their unique strengths. For example, create a plan with a local agent, hand off to a background agent for proof of concepts, and then continue with a cloud agent to submit a pull request for team review.

**Example:**

1. **Local Agent:** (Plan and then Implement)
   1. Create a simple todo app with HTML, CSS, and JavaScript. Include an input field to add todos, a list to display them, and a delete button for each item.
   2. Mark todos as completed with a strikethrough effect.
2. **Background Agent (Plan mode)**
   1. Create a plan to add a dark/light theme toggle to the app. The toggle should switch between themes and persist the user's preference.
3. **Cloud Agent:**
   1. Publish the Project to GitHub
   2. Redesign the todo app layout to improve user experience. Update colors, spacing, typography, and add animations to give it a modern look.