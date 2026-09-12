**Inline Completions vs Chat Window: When to Use Each**

|  |  |  |
| --- | --- | --- |
| **Aspect** | **Inline Completions** | **Copilot Chat** |
| Trigger | Automatic as you type | Manual (open panel, ask question) |
| Display | Gray ghost text in editor | Dedicated chat panel with markdown |
| Interaction | Accept (Tab), Reject (Esc), Cycle (Alt+]) | Multi-turn conversation, follow-ups |
| Response Time | 200-500ms (fast) | 1-5 seconds (slower, more thorough) |
| Output Scope | 1-20 lines of code | Code + explanations, unlimited length |
| Context Awareness | Current file + open tabs | Current file + selection + conversation history |
| Best For | Writing code quickly (execution mode) | Learning, debugging, exploration (thinking mode) |

|  |  |
| --- | --- |
| **Use Inline Completions When:** | **Use Copilot Chat When:** |
| * You know what you want to build * You're implementing a clear spec * Speed is critical * The task is straightforward * You need boilerplate or repetitive code * You want to stay in flow stat | * You're exploring options * You need to understand existing code * You're debugging an issue * You need explanations or learning * The task is complex or ambiguous * You want to iterate on solutions |
| **Examples:**   * Boilerplate code (getters, setters, constructors) * Repetitive patterns (CRUD operations, API routes) * Function implementations following established patterns * Quick fixes (error handling, null checks) * Autocomplete style completion | **Examples:**   * Complex algorithms requiring step-by-step reasoning * Architecture decisions * Multi-file refactoring * Debugging complex issues (/fix or /explain) * Learning new concepts * Authentication, encryption, payments (with extreme review) |

Think of Inline as your **"speed tool"** and Chat as your **"thinking tool"**.

A typical workflow might be:

1. **Chat**: "Explain how this authentication middleware works" (understanding)
2. **Inline**: Write a new route using that middleware (execution)
3. **Chat**: "Why is this route returning 401?" (debugging)
4. **Inline**: Fix the bug based on Chat's explanation (execution)

You're **switching between modes** as your needs change.

**Automatic Triggers for Inline Suggestions**

* **New line after comment:** Press Enter after comment → suggestion appears
* **Function signature:** Write function name + params → body suggested
* **Opening brace:** Type { → content suggested
* **Typing pause:** Stop typing for 200-300ms → suggestion triggers
* **After keyword:** Type if, for, return → completion follows
* **Incomplete statement:** const users = → value suggested

**Manual Trigger / Force Suggestions**

* **Windows/Linux:** Alt + \
* **macOS:** Option + \

**Shortcuts:**

|  |  |
| --- | --- |
| **Action** | **Shortcut** |
| **Accept Entire Suggestion** | Tab |
| **Accept Word-by-Word** | Ctrl + → (or Cmd + → macOS) |
| **Reject Suggestion** | Esc |
| **Next Alternative** | Alt + ] (or Option + ] macOS) |
| **Previous Alternative** | Alt + [ (or Option + [ macOS) |
| **Trigger Manually** | Alt + \ (or Option + \ macOS) |

**Recommendation:**

1. **Partial Acceptance Workflow:** Use Ctrl+→ (or Cmd+→) to accept word-by-word when the suggestion is 80% right but needs tweaking. Accept the good parts, stop at the bad parts, and type your own changes.
2. **Alternative Cycling Strategy:** Before accepting, press Alt+] 2-3 times to see alternatives. Sometimes suggestion #2 or #3 is better than #1. Don't settle for the first suggestion without exploring.
3. **Reject-Retype-Retrigger Pattern:** If all suggestions are wrong: Press Esc to reject → Retype your comment with more detail → Press Alt+\ to manually retrigger. Often the refined prompt yields a better suggestion.
4. **Common Anti-Patterns**
   1. Blindly Pressing Tab
   2. Fighting for complex Tasks
   3. Expecting suggestions in empty file
   4. Never using alternatives

**Copilot Chat**

* **Interface**: Dedicated chat panel in your IDE (sidebar or popup)
* **Interaction**: Type questions or requests in natural language
* **Context** **awareness**: Can reference open files, selected code, or entire workspace
* **Multi-turn** **conversations**: Maintains conversation history for follow-up questions
* **Response** **format**: Markdown-formatted text with code blocks, explanations, and reasoning
* **Code** **actions**: Can insert code at cursor, create new files, or explain existing code

**Copilot Chat Use cases:**

**Understanding & Learning**

* Explain unfamiliar code: "Explain what this function does"
* Learn new libraries: "How do I use React hooks?"
* Understand patterns: "What design pattern is this?"
* Clarify concepts: "Explain closures in JavaScript"

**Debugging & Troubleshooting**

* Find bugs: "Why is this returning undefined?"
* Fix errors: Use /fix command on error messages
* Performance issues: "How can I optimize this query?"
* Unexpected behavior: "This should return 5 but returns 4"

**Architecture & Design**

* Explore options: "Should I use Redux or Context API?"
* Design decisions: "Best way to structure this API?"
* Evaluate trade-offs: "Pros and cons of microservices?"
* Get recommendations: "What testing framework should I use?"

**Refactoring & Improvement**

* Code improvement: "How can I make this more readable?"
* Extract patterns: "Extract this into reusable functions"
* Modernize code: "Convert this to async/await"
* Add features: "Add error handling to this function"

**Documentation & Testing**

* Generate tests: Use /tests command
* Write docs: Use /doc command for JSDoc comments
* Create examples: "Generate usage examples for this API"
* README generation: "Create a README for this project"

**Slash Commands and Context Variables**

|  |  |  |
| --- | --- | --- |
| **Command** | **Description** | **Example** |
| **/clear** | Start a new chat session | /clear *(no prompt needed — resets the chat context)* |
| **/explain** | Explain how the code in your active editor works | /explain how does the middleware pipeline work in this file? |
| **/fix** | Propose a fix for problems in the selected code | /fix the null reference exception in the selected method |
| **/fixTestFailure** | Find and fix a failing test | /fixTestFailure why is the TodoController POST test failing? |
| **/help** | Quick reference and basics of using GitHub Copilot | /help *(no prompt needed — shows available commands and tips)* |
| **/new** | Create a new project | /new create a .NET Web API project with Entity Framework and SQL Server |
| **/tests** | Generate unit tests for the selected code | /tests generate xUnit tests for the selected TodoController actions |

**Chat Variables**Use chat variables to include specific context in your prompt. To use a chat variable, type # in the chat prompt box, followed by a chat variable.

|  |  |  |
| --- | --- | --- |
| **Variable** | **Description** | **Example** |
| **#block** | Includes the current block of code in the prompt | explain what this #block of code does |
| **#class** | Includes the current class in the prompt | review #class for any SOLID principle violations |
| **#comment** | Includes the current comment in the prompt | write code that implements the logic described in #comment |
| **#file** | Includes the current file's content in the prompt | summarize what #file does and suggest improvements |
| **#function** | Includes the current function or method in the prompt | /tests generate unit tests for #function |
| **#line** | Includes the current line of code in the prompt | explain what #line does and why it might throw an exception |
| **#path** | Includes the file path in the prompt | based on #path suggest the correct namespace for this file |
| **#project** | Includes the project context in the prompt | suggest a folder structure improvement based on #project |
| **#selection** | Includes the currently selected text in the prompt | /explain #selection and suggest a more readable version |
| **#sym** | Includes the current symbol in the prompt | find all usages and explain the purpose of #sym |

**Combine commands with context variables for powerful queries:**

**Example 1: Scoped Context with #selection**

/tests #selection

*/optimize #selection for better performance without changing behavior*

**Example 2: Multi-File References**

Compare **#file:oldAuth.js** with **#file:newAuth.js** and explain differences

Extract shared logic from **#file:auth.js and #file:validation.js** into a utilities module

**Example 3: Debug Error from Terminal**

*The test in* ***#selection*** *is failing with* ***#terminalSelection*** *error. What's the root cause and how do I fix it?*

***/fix #selection*** *- the error is* ***#terminalSelectio****n, likely related to* ***#file:config.js*** *settings*

**Example 4: Document Entire File**

**/doc** for all functions in **#file**

**/doc #selection** with usage examples that reference **#file:types.ts** interfaces

**Chat Participants**

Specialized agents that provide Copilot with specific context for your questions

* **@workspace –** knows about **all the code in your currently open workspace** — files, structure, dependencies, and relationships. It's the most frequently used chat participant for project-level questions.
  + ~~@workspace~~ what is the overall architecture of this project?
  + ~~@workspace~~ what design patterns are used in this codebase?
  + ~~@workspace~~ Create a README for this project
  + ~~@workspace~~ What external APIs do we use?
  + ~~@workspace~~ where is the database connection configured?
  + ~~@workspace~~ find all places where HttpClient is used
  + ~~@workspace~~ how is dependency injection configured in this project?
  + ~~@workspace~~ which parts of the codebase have no test coverage?
* **@terminal –** Ask how to do something in the terminal (Switch to Powershell - not supported in cmd mode)

(If not working, add "terminal.integrated.shellIntegration.enabled": true to settings.json in vscode user settings)

* + @terminal "How do I run tests in watch mode?"
  + @terminal find the largest file in the src directory
  + @terminal how do I recursively delete all node\_modules folders
  + @terminal show disk usage sorted by size
  + @terminal how do I build this .NET project from CLI
  + @terminal create a PowerShell script to restart IIS
  + **@terminal #terminalSelection** what does this output mean?
* **@vscode –** knows everything about the **VS Code editor itself** — its commands, settings, extensions, keybindings, and features. Use it when your question is about **how to use or configure VS Code**, not about your code.
  + @vscode how do I change the font size in the editor?
  + @vscode where is the settings.json file located?
  + @vscode how do I enable word wrap for markdown files only?
  + @vscode what is the shortcut to open the integrated terminal?
  + @vscode which extensions are recommended for C# development?
  + @vscode how do I set conditional breakpoints?
  + @vscode how do I find all references to a method across the project?
  + @vscode how do I view the git diff inline in the editor?
* **@github –** has access to **GitHub-specific skills** — it can search your repositories, issues, pull requests, commits, code, and even the web. Unlike @workspace (which knows your *local* code), @github knows your **remote GitHub repositories and activity**.
  + @github which repos in our org use .NET 8?
  + @github find all repos that have a Dockerfile
  + @github list all open bugs in the TodoWebAPI repository
  + @github list all open pull requests in this repository
  + @github what changed in the last 5 commits on the main branch?
  + @github what is the tech stack used in this repository?
* **@azure** – To get information about MS Azure and its Services.

**Next edit suggestions**

* Next edit suggestions (NES) is a GitHub Copilot feature that predicts both the location and content of your next code edit based on the recent changes you've been making.
* Unlike traditional ghost text suggestions that only appear at your cursor position, NES analyzes your editing history to anticipate what you'll want to change next—even if it's elsewhere in your file. When NES detects a suggested edit, an arrow appears in the editor gutter, and you can press Tab to navigate to the suggestion and Tab again to accept it.
* The feature is particularly useful for refactoring tasks, such as renaming variables or adding fields to data structures, where related changes need to be made in multiple locations throughout your code. NES can suggest changes to code, comments, tests, and can even help fix bugs or missing imports.​

![Copilot Next Edit Suggestions (preview)](data:image/png;base64...)

**Copilot pull request** **summaries**

GitHub Copilot Pull Request Summaries is an AI-powered feature that automatically generates comprehensive descriptions of code changes in pull requests.

It analyzes the diff and creates:

* A prose overview of what changed
* A bulleted list of specific changes with file references
* Reviewer focus areas

**Where You Can Generate Summaries**

1. **When creating a new pull request** - in the description field
2. **On existing pull requests** - by editing the opening comment
3. **As a comment** - in the PR conversation thread

**IDEs Supported**

* **In VS Code** - via GitHub Pull Requests extension
* **In Visual Studio** - when creating PRs (VS 2022 v17.10+)

**Steps:**

**Open Pull Request on GitHub.com**

* Click "Compare & pull request"
* Navigate to the text field where you want to add the pull request summary.
  + If you're creating a **new pull request**, use the "**Add a description**" field.
  + If you're adding a description to an **existing** pull request, **edit the opening comment**.
  + If you're adding a **summary as a comment**, navigate to the "**Add a comment**" section at the bottom of the pull request page.

![Screenshot of the form for creating a pull request. A Copilot icon is highlighted, and a box appears with the "Summary" command.](data:image/png;base64...)

**How It Works:**

1. **You trigger** the summary (click Copilot icon)
2. **Copilot analyzes** the code diffs from all changed files
3. **LLM generates** a structured summary using the Copilot API
4. **Two-part output:**
   * Prose paragraph explaining the changes
   * Bulleted list linking specific changes to files

**Copilot Code** **Review**

**Setup Repository Rules:**

Request Copilot code review for new pull requests automatically if the author has access to Copilot code review and their **premium requests quota** has not reached the limit:

1. Go to GitHub.com 🡪 Select your repository 🡪 **Repository Settings** → **Rules** → **Rulesets**
2. Create **New Ruleset**
3. Configure:
   1. Ruleset Name: CodeReviewAllBranches
   2. **Check** Automatically request Copilot code review

**What Happens:**

* Every **PR** automatically gets reviewed by Copilot
* No manual reviewer selection needed
* Consistent code quality checks
* Catches issues before human review

**Cost Consideration:**

* Included: 300-1000 reviews/month (licensed users)
* Premium Request: $0.04 per review (unlicensed users)

**Review in VS Code:**Select the Code 🡪 Right-click 🡪 Generate Code 🡪 Review

**Review All Uncommitted Changes**

**Scenario:** Before committing, review all your work

*Make multiple file changes*

**In VS Code:**

1. Open **Source Control** panel (Ctrl+Shift+G)
2. Click **"Review Changes"** button (sparkle icon above Message)
3. Or right-click on changes in Source Control → **"Review with Copilot"**

**Custom Review Instructions**

**Create .github/copilot-review-instructions.md:**

# Code Review Guidelines for Projects

## Security Requirements

- All database queries must use parameterized statements

- API keys must be in environment variables

- All user inputs must be validated and sanitized

- Authentication required on all non-public endpoints

## Code Quality Standards

- Functions should not exceed 50 lines

- Maximum cyclomatic complexity: 10

- All public methods must have JSDoc comments

- Consistent error handling with custom error classes

## Testing Requirements

- Every function must have unit tests

- Minimum 80% code coverage

- Integration tests for API endpoints

- E2E tests for critical user flows

## Specific Frameworks

- React: Use functional components with hooks

- Express: Use async/await, not callbacks

- Database: Use TypeORM, migrations required

- Logging: Use Winston, not console.log

## What NOT to flag

- Console.log in test files is acceptable

- Long functions in generated migration files

- TODO comments (we track them in Jira)

When reviewing, focus on:

1. Security vulnerabilities

2. Performance issues

3. Maintainability problems

4. Deviations from our standards above

**Make reviews project-specific:**

**Create .vscode/settings.json:**

{

"github.copilot.chat.reviewSelection.enabled": true,

"github.copilot.chat.reviewSelection.instructions": [

{

"file": ".github/copilot-review-instructions.md"

}

]

}

**Now Copilot reviews match YOUR standards!**