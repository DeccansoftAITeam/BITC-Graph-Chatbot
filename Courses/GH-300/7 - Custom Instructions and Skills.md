**Copilot Custom Instructions**

**What are custom instructions?**

* Markdown files that provide context to GitHub Copilot about your project
* Help Copilot generate more relevant code suggestions
* Can be repository-wide or path-specific
* Version-controlled and shared with team members

**Adding organization custom instructions**

You can add organization custom instructions via your organization settings.

1. GitHub.com, profile picture, then click  Organizations.
2. Next to the organization, click Settings.
3. In the left sidebar, click Copilot then click Custom instructions.
4. Under "**Preferences and instructions**", add natural language instructions to the text box.
5. Click Save changes.

NOTE: Organization custom instructions are currently only supported for Copilot Chat on GitHub.com, Copilot code review on GitHub.com and Copilot coding agent on GitHub.com.

**Repository-Wide Custom Instructions:**

.github/copilot-instructions.md in repository root or subdirectories

**When they apply:**

* Automatically loaded when working in that repository
* Apply to all files unless overridden by path-specific instructions
* Work in VS Code and other supported IDEs

**Path-Specific Custom Instructions:**

* Create .github/instructions
* Create one or more **NAME.instructions.md** files, where NAME indicates the purpose of the instructions.
  + frontend.instructions.md
  + backend.instructions.md
* At the start of the file, create a frontmatter block using GLOB syntax.

---

**applyTo: "frontend/\*\**"***

**OR**

**applyTo: "frontend/\*\*/*\*.js,frontend/\*\*/\**.jsx"**

***---***

**Note: Custom instructions are not visible in the Chat view or inline chat, but you can verify that they are being used by Copilot by looking at the References list of a response in the Chat view.**

**Enabling or disabling for Copilot Chat:**

1. Open the Setting editor by using the keyboard shortcut **Command+,** (Mac) / Ctrl+, (Linux/Windows).
2. Type **instruction file** in the search box.
3. Select or clear the checkbox under Code Generation: Use Instruction Files.

**Enabling or disabling for Copilot code review:**

1. GitHub.com 🡪 Repository Settings 🡪 Code & automation 🡪 click Copilot, then Code review.
2. Toggle the “Use custom instructions when reviewing pull requests” option on or off.

**Content guidelines:**

* Use markdown formatting
* Be specific and actionable
* Include coding standards, patterns, frameworks
* Specify tech stack and versions
* Define architectural patterns

**Limitations**

* Instructions are suggestions, not guarantees
* Complex rules may be ignored for simple suggestions
* Too many instructions can reduce suggestion quality
* Context window limits (~4000 tokens for instructions + code)

**Prompt to Generate the Recommended Content for the Custom Instructions File:**

Role: You are a Senior Software Developer with experience in coding Enterprise Apps using GitHub Copilot.
Task: Create a ready to use copilot.instructions.md file for Python and React Project.
Backend and Frontend are my project folders opened from same workspace.
Divide the instructions into sections.
Keep content of file under 2000 works. Can be less also.
Break the file into sections for clarity.

Before you proceed, feel free to ask questions you may have.

The instructions file at copilot-instructions.md is **automatically injected** into my context by VS Code's Copilot extension — it appears as an <attachment> tag directly in my system prompt. No explicit read\_file call is needed or made; it's already loaded before I respond to anything.

**Prompt Files**

Prompt files, also known as slash commands, let you simplify prompting for common tasks by encoding them as standalone Markdown files that you can invoke directly in chat.

**Use prompt files to:**

* Simplify prompting for common tasks, such as scaffolding a new component, running and fixing tests, or preparing a pull request
* Override default behavior of a custom agent, such as creating a minimal implementation plan or generating mockups for API calls

**Prompt files are Markdown files** with the **.prompt.md** extension. The optional YAML frontmatter header configures the prompt's behavior:

**Location = .github/prompts folder**

**You can reference the following variables in a prompt file:**

* Workspace variables - ${workspaceFolder},
* Selection variables - ${selection}, ${selectedText}
* File context variables - ${file}, ${fileDirname},
* Input variables - ${input:variableName} (pass values to the prompt from the chat input field)

**Tips for writing effective prompts**

* Clearly describe what the prompt should accomplish and what output format is expected.
* Provide examples of the expected input and output to guide the AI's responses.
* Use Markdown links to reference custom instructions rather than duplicating guidelines in each prompt.
* Take advantage of built-in variables like ${selection} and input variables to make prompts more flexible.
* Use the editor play button to test your prompts and refine them based on the results.

**Generate React Form Component (reactform.prompt.md):**

---

agent: 'agent'

model: GPT-5.2

tools: ['githubRepo', 'search/codebase']

description: 'Generate a new React form component'

argument-hint: 'mention form name and fields'

---

Your goal is to generate a new React form component based on the templates in #tool:githubRepo contoso/react-templates.

Ask for the form name and fields if not provided.

Requirements for the form:

\* Use form design system components: [design-system/Form.md](../docs/design-system/Form.md)

\* Use `react-hook-form` for form state management:

\* Always define TypeScript types for your form data

\* Prefer \*uncontrolled\* components using register

\* Use `defaultValues` to prevent unnecessary rerenders

\* Use `yup` for validation:

\* Create reusable validation schemas in separate files

\* Use TypeScript types to ensure type safety

\* Customize UX-friendly validation rules

**Perform Security Review (securityreview.prompt.md)**

---

agent: 'ask'

model: Claude Sonnet 4

description: 'Perform a REST API security review'

---

Perform a REST API security review and provide a TODO list of security issues to address.

\* Ensure all endpoints are protected by authentication and authorization

\* Validate all user inputs and sanitize data

\* Implement rate limiting and throttling

\* Implement logging and monitoring for security events

Return the TODO list in a Markdown format, grouped by priority and issue type.

For more community-contributed examples, see the [Awesome Copilot repository](https://github.com/github/awesome-copilot/tree/main).

**Using a Prompt File in Chat:**

In the Chat view, type / followed by the prompt name in the chat input field

You can add extra information in the chat input field. For example, /create-react-form formName=MyForm or /create-api for listing customers.

Agents Skills

* Agent Skills are folders of instructions, scripts, and resources that Copilot can load when relevant to improve its performance in specialized tasks.
* Agent Skills is an [open standard](https://github.com/agentskills/agentskills), used by a range of different agents.
* Shared Skills:
  + [anthropics/skills](https://github.com/anthropics/skills)
  + [github/awesome-copilot](https://github.com/github/awesome-copilot)

**Example skill categories:**

* Language & framework expertise
* Architecture rules
* Coding standards
* Security practices
* Testing strategy
* Cloud / infra assumptions
* Performance expectations

**To Create a Skill:**

1. Create a subdirectory for your skill. Each skill should have its own directory (for example, **.github/skills/my-skill-name**). Must be all lowercase
2. Create a **SKILL.md** file in the skill directory with the following structure:

---

**name**: my-skill-name

**description**: A clear description of what this skill does and when to use it

---

**# My Skill Name**

[Add your instructions here that Claude will follow when this skill is active]

**## Examples**

- Example usage 1

- Example usage 2

**## Guidelines**

- Guideline 1

- Guideline 2

1. Optionally, add scripts, examples, or other resources to your skill's directory.

For example, a skill for testing web applications might include:

* SKILL.md - Instructions for running tests
* test-template.js - A template test file
* examples/ - Example test scenario

**The skill body contains** the instructions, guidelines, and examples that Copilot should follow when using this skill. Write clear, specific instructions that describe:

* What the skill helps accomplish
* When to use the skill
* Step-by-step procedures to follow
* Examples of the expected input and output
* References to any included scripts or resources

You can reference files within the skill directory using relative paths. For example, to reference a script in your skill directory, use **[test script](./test-template.js)**

**Example: Web application testing skill**

---

**name: webapp-testing**

description: Guide for testing web applications using Playwright. Use this when asked to create or run browser-based tests.

---

# Web Application Testing with Playwright

This skill helps you create and run browser-based tests for web applications using Playwright.

## When to use this skill

Use this skill when you need to:

- Create new Playwright tests for web applications

- Debug failing browser tests

- Set up test infrastructure for a new project

## Creating tests

1. Review the **[test template](./test-template.js)** for the standard test structure

2. Identify the user flow to test

3. Create a new test file in the `tests/` directory

4. Use Playwright's locators to find elements (prefer role-based selectors)

5. Add assertions to verify expected behavior

## Running tests

To run tests locally:

npx playwright test

To debug tests:

npx playwright test --debug

## Best practices

- Use data-testid attributes for dynamic content

- Keep tests independent and atomic

- Use Page Object Model for complex pages

- Take screenshots on failure

**How Copilot uses Skills:**

1. **Skill discovery:** Copilot always knows which skills are available by reading their name and description from the YAML frontmatter. This metadata is lightweight and helps Copilot decide which skills are relevant to your request.
2. **Instructions loading:** When your request matches a skill's description, Copilot loads the SKILL.md file body into its context. Only then do the detailed instructions become available.
3. **Resource access:** Copilot can access additional files in the skill directory (scripts, examples, documentation) only as needed. These resources don't load until Copilot references them, keeping your context efficient.

**Skills vs Custom Instructions:**

|  |  |  |
| --- | --- | --- |
| Feature | Agent Skills | Custom Instructions |
| Purpose | Specialized capabilities/workflows | Coding standards/guidelines |
| Portability | Works across VS Code, CLI, coding agent | VS Code and GitHub.com only |
| Content | Instructions, scripts, examples, resources | Instructions only |
| Scope | Task-specific, on-demand loading | Always applied or via glob patterns |
| Standard | Open standard (agentskills.io) | VS Code-specific |