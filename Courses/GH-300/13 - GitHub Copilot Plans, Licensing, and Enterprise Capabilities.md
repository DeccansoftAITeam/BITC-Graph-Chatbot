**GitHub Copilot Plans, Licensing, and Enterprise Capabilities**. This domain shifts our focus from **how to use Copilot** to **how to adopt it strategically** across teams and organizations.

Here's the key question we're answering: **"Which Copilot plan is right for my team or organization, and how do I justify the investment?"**

By the end of this domain, you'll be able to:

* **Compare the three Copilot plans** — Individual, Business, and Enterprise — and understand the key differences in features, pricing, and capabilities.
* **Understand enterprise-specific features** like pull request summaries, knowledge bases, and organization-level policy controls.
* **Build a business case** for Copilot adoption with clear ROI metrics and productivity justifications.
* **Avoid common rollout pitfalls** that organizations face when deploying AI coding assistants at scale.
* **Make informed decisions** about licensing, seat management, and access controls.

This is practical and strategic. We're not just talking about features — we're talking about **decision-making frameworks**, **cost-benefit analysis**, and **organizational change management**.

**GitHub Copilot plans**

<https://github.com/features/copilot/plans>

GitHub Copilot offers **Five Plans** designed for different use cases:

**(FREE | Pro | Pro+ | Business | Enterprise)**

Common Features (with Edition-wise Support)

1. Premium requests per month - Monthly limit for advanced AI operations (chat, agent mode, code review, CLI) that consume more computational resources.
   (50 | 300 | 1500 | 300 | 10 00)
2. Purchase additional premium requests - Ability to buy extra premium requests at $0.04 per request when monthly limit is exceeded.
   (N | Y | Y | Y | Y)
3. Editors and IDEs - Support for code editors like VS Code, Visual Studio, JetBrains, Neovim, Eclipse, Xcode, Azure Data Studio.
   (Y | Y | Y | Y | Y)
4. CLI - Command-line interface tool to use Copilot directly from your terminal.
   (N | Y | Y | Y | Y)
5. GitHub (including github.com and GitHub Mobile) - Use Copilot directly within GitHub web and mobile experiences.
   (Y | Y | Y | Y | Y)
6. Agent mode use with GPT-5 mini - Interactive AI assistant mode using latest models;.
   (50/month | Unlimited | Unlimited | Unlimited | Unlimited)
7. Integrates with MCP servers (Agent mode) - Connect to Model Context Protocol servers (like Asana, Gmail, Salesforce) for external tool integration.
   (Y | Y | Y | Y | Y)
8. Custom instructions and agents (Agent mode) - Personalize AI behavior with custom instructions and create specialized agents.
   (Y | Y | Y | Y | Y)
9. App modernization for Java and .NET - Specialized assistance for upgrading/modernizing Java and .NET applications.
   (N | Y | Y | Y | Y)
10. Assign work to Copilot (creates PR) - Give Copilot a task and it automatically creates a pull request with the implementation.
    (N | Y | Y | Y | Y)
11. Pull request reviews in GitHub - AI-powered code review suggestions on pull requests in GitHub.
    (N | Y | Y | Y | Y)
12. File diff reviews in code editors - Review file changes directly within your IDE with AI suggestions.
    (N | Y | Y | Y | Y)
13. Custom instructions with instructions.md - Use instructions.md file to define project-specific coding guidelines for Copilot.
    (N | Y | Y | Y | Y)
14. Assign issues to Copilot (Coding agent) - Assign GitHub issues or work items to Copilot for automatic PR creation.
    (N | Y | Y | Y | Y)
15. Start/track issues from agents page - Manage and monitor Copilot-assigned work from a dedicated agents dashboard.
    (N | Y | Y | Y | Y)
16. Start/track issues from code editors - Create and track Copilot tasks directly within your IDE.
    (N | Y | Y | Y | Y)
17. Start/track issues from 3rd party tools - Integrate with project management tools like Jira, Azure DevOps for issue tracking.
    (N | Y | Y | Y | Y)
18. Integrates with MCP servers (Coding agent) - Connect coding agent to external services via MCP protocol.
    (N | Y | Y | Y | Y)
19. Custom instructions and agents (Coding agent) - Customize coding agent behavior with specific instructions and workflows.
    (N | Y | Y | Y | Y)
20. Use Copilot from terminal - Access Copilot features through command-line interface for terminal-based workflows.
    (N | Y | Y | Y | Y)
21. Delegate tasks to coding agents (CLI) - Assign development tasks to AI agents from the command line.
    (N | Y | Y | Y | Y)
22. Make/commit code changes locally or on GitHub - Copilot can modify files and create commits on your local machine or directly on GitHub.
    (N | Y | Y | Y | Y)
23. Programmatic mode - Automated, script-friendly mode for CI/CD integration and batch operations.
    (N | Y | Y | Y | Y)
24. Interactions with GPT-4.1 and GPT-5 mini - Chat conversations using OpenAI's GPT-4.1 and GPT-5 mini models.
    (50/month | Unlimited | Unlimited | Unlimited | Unlimited)
25. Access to all available models - Use various AI models from Anthropic (Claude), Google (Gemini), OpenAI (GPT), and xAI (Grok).
    (Y | Y | Y | Y | Y)
26. Code completions - AI-generated code suggestions as you type; Free gets 2,000/month, paid plans unlimited.
    (2,000/month | Unlimited | Unlimited | Unlimited | Unlimited)
27. Copilot Spaces - Collaborative workspace for organizing and managing Copilot projects.
    (Y | Y | Y | Y | Y)
28. GitHub Spark (Preview) - Build and deploy intelligent applications (Pro+ exclusive feature).
    (N | N | Y | N | N)
29. Public code filter with code referencing - Detects and blocks suggestions matching public code (150+ chars).
    (Y | Y | Y | Y | Y)
30. Data excluded from training by default - Your code/prompts are not used to train AI models.
    (Y | Y | Y | Y | Y)
31. Enterprise-grade security - Advanced security and compliance controls.
    (N | N | N | Y | Y)
32. IP indemnity - Legal protection against IP infringement claims.
    (N | N | N | Y | Y)
33. User management in github.com - Centralized license and user access management.
    (N | N | N | Y | Y)
34. Usage metrics - Analytics dashboard for Copilot usage and adoption.
    (N | N | N | Y | Y)
35. SAML SSO authentication - Single Sign-On with enterprise identity providers.
    (N | N | N | N | Y)

**Business / Enterprise exclusive Features**

1. **Organization Management**

* **License management:** Assign/revoke seats centrally in github.com - Centralized admin controls for managing Copilot licenses and user access.
* **Usage analytics:** Analytics dashboard showing team's Copilot usage, adoption, and productivity metrics.
* **Policy controls**: Enable/disable features org-wide
* **Audit logs**: **:** Who used Copilot, when, where. This can be governance requirement.

1. **Privacy**

* **Data excluded from training by default** - Your code/prompts are not used to train AI models.
* **Data Protection Agreement (DPA):** GitHub offers a DPA that outlines the measures taken to protect your data and ensure compliance with data privacy regulations. These agreements provide transparency and assurance that your data is handled securely and responsibly.
* **Data retention:** Prompts/completions stored temporary for abuse prevention only
* **Telemetry control**: Admins can disable telemetry collection.
* **Public code filter with code referencing** - Detects and Blocks suggestions matching public code (150+ chars). **Settings → Copilot → Features → Suggestion matching public code → Blocked**

1. **AI-Generated Code Ownership**

* **You own the output –** Code generated by Copilot belongs to you
* **IP Indemnity:** If a Copilot suggestion is challenged as infringing third-party IP rights → GitHub defends you and covers legal costs provided "Block matching public code" setting is enabled

1. **Advanced Security and Compliance**:

* **SSO/SAML integration**: Enterprise authentication with **Azure AD, Okta, Google Workspace**, etc. Your developers log in with their corporate credentials, not personal GitHub accounts.
* **Enhanced audit logs**: Detailed compliance tracking for **SOC 2, ISO 27001, HIPAA, GDPR**. You can prove to auditors exactly who accessed Copilot, when, and what they did.

1. **Knowledge Bases**:

* **Index internal docs**: Copilot learns from your **Markdown documentation, wikis, and documentation repositories**. You point Copilot at your internal docs, and it indexes them.
* **Context-aware suggestions**: Once indexed, Copilot references your team's standards, architecture decisions, and coding patterns **automatically**.
* For example, if your docs say "Always use Redux for state management in React apps," Copilot will suggest Redux patterns instead of Context API or other alternatives.

1. **AI-Based Vulnerability Filtering**

Automatically **blocks suggestions** containing common security vulnerabilities. It analyzes suggestions in real-time. If a vulnerability is detected → suggestion is **blocked before being shown** to the developer.

* + - SQL injection patterns
    - Cross-site scripting (XSS) vulnerabilities
    - Hardcoded credentials and API keys
    - Path traversal vulnerabilities
    - Insecure deserialization

1. **Organization-level policy controls**:

* **Granular access control**: Enable or disable Copilot by team, repository, or user group. For example, you might enable it for frontend teams but disable it for infrastructure teams.
* **Feature toggles**: Control which Copilot features are available. You might enable inline completions but disable Chat for certain teams.
* **Model selection policies**: Specify which AI models teams can use. Maybe finance teams can only use GPT-4 for compliance reasons, while product teams can use any model.
* **Data residency**: Choose data storage regions for compliance. If you're in the EU and subject to GDPR, you can require data to stay in EU regions.
* **Custom retention policies**: Define how long prompts and telemetry are retained. Some industries require data deletion after 90 days.
* **Integration management**: Control third-party integrations and extensions to prevent shadow IT.

**Manage Content Exclusions**

* **Prevent specific files/directories/repositories** from being used by Copilot for suggestions and chat responses
* This is critical for **compliance** and **security**. If you have repos with PII or sensitive data, you can ensure Copilot never references them.
* Available for Organizations with a Copilot Business or Copilot Enterprise plan.
* Repository administrators, organization owners, and enterprise owners can manage content exclusion settings. People with the "Maintain" role for a repository can view, but not edit, content exclusion settings for that repository.

**Impact of Content Exclusions**

* **Code Completion**: Excluded files won't have code completion available, and their content won't inform suggestions in other files.
* **Chat Responses**: Excluded content won't be used in GitHub Copilot Chat responses, affecting the quality and relevance of suggestions.

**Configuring Content Exclusions**

1. **For Repositories**
   1. **GitHub.com 🡪 Select Repository 🡪 Settings** 🡪 code & automation 🡪 Copilot 🡪 Content exclusion 🡪 Paths to exclude in this repository 🡪 Enter path in glob pattern format

**# Ignore a specific file**

- "/src/some-dir/kernel.rs"

**# Ignore files called secrets.json anywhere in the repo**

- "secrets.json"

**# Ignore all files that start with 'secret'**

- "secret\*"

**# Ignore all \*.cfg files**

- "\*.cfg"

**# Ignore all files in or below /scripts**

- "/scripts/\*\*"

1. **For Organizations**
   1. You must be an **organization owner** to set these exclusions.
   2. GitHub.com 🡪 Profile Picture 🡪 Organizations 🡪 Settings tab under Organizations profile 🡪 Copilot (on left sidebar) 🡪 Copilot Settings 🡪 Content exclusion

**# Ignore all `.env` files from all file system roots (Git and non-Git).**

# "\*": ["\*\*/.env"]

"\*":

- "\*\*/.env"

**# In the `octo-repo` repository in this organization:**

octo-repo:

# Ignore the `/src/some-dir/kernel.rs` file.

- "/src/some-dir/kernel.rs"

**# In the `primer/react` repository on GitHub:**

https://github.com/primer/react.git:

# Ignore files called `secrets.json` anywhere in this repository.

- "secrets.json"

# Ignore files called `temp.rb` in or below the `/src` directory.

- "/src/\*\*/temp.rb"

**# In the `copilot` repository of any GitHub organization:**

git@github.com:\*/copilot:

# Ignore any files in or below the `/\_\_tests\_\_` directory.

- "/\_\_tests\_\_/\*\*"

# Ignore any files in the `/scripts` directory.

- "/scripts/\*"

**Debug Tip: Hover over Copilot status bar icon to see exclusion status: "Copilot disabled for this file by organization policy."**

**Note:** Organization-level exclusions act as defaults, overridden by repo-specific exclusions.

**Known Limitations with Context Exlusions:**

* **IDE-specific gaps**: Exclusions may not apply in **Copilot Chat with** **@github** participant (VS Code/Visual Studio)
* **Semantic information leakage**: Type definitions and function signatures may still be visible. You exclude **auth.ts**, but another file **imports AuthService** from it. Copilot may still suggest AuthService methods because the IDE provides type information.
* **Policy scope**: Only applies to organization members—external collaborators not affected