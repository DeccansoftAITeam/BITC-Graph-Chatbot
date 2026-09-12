![](data:image/png;base64...)

**AI is the engine, but prompts are the steering wheel.**

If you can steer well, you can go anywhere.

**Question**: Write a function to validate email?

**Definition: The craft of designing effective instructions to guide AI models toward desired outputs.**

* It involves crafting inputs to guide AI outputs.
* It is vital for optimizing AI responses and usability.
* It emphasizes intent, context, and clarity beyond syntax.
* Ambiguous prompts can cause unpredictable results.
* Structured prompts with examples improve consistency.
* It addresses challenges like hallucinations, bias, and ethical use.

**The Paradigm Shift**: From Writing Code to Directing AI

For decades, developers have been the translators between human intent and machine execution. We took requirements, designed solutions, and wrote code that implemented those solutions line by line. AI fundamentally changes this relationship.

**💡 Key Insight:** Think of yourself as an architect who now has access to a very capable but literal-minded construction crew. Your job shifts from laying bricks to creating clear blueprint

### The Old Model vs. The New Model

|  |  |
| --- | --- |
| **Traditional Development** | **AI-Assisted Development** |
| **Requirement → Design → Code** | **Requirement → Prompt → Review → Refine** |
| You implement every detail | You specify intent; AI generates implementation |
| Time spent: 80% typing, 20% thinking | Time spent: 30% prompting, 70% reviewing/directing |
| Skill: Language syntax mastery | Skill: Clear specification + critical evaluation |

**Your Responsibilities as Senior Developer?**

### Prompts as Specifications:

As senior developers, you already write specifications, whether they are API contracts, technical design docs, or detailed tickets. A prompt is simply a specification for an AI system. The same principles apply: ambiguity leads to unexpected results, completeness prevents gaps, and precision ensures correctness.

Precise Prompt:

Write a C# function that validates email addresses. Requirements: (1) Return bool indicating validity, (2) Check for @ symbol and valid domain format, (3) Handle null/empty input by returning false, (4) Use regex for pattern matching, (5) Include XML documentation comments.

Why it works: The precise prompt specifies language, return type, validation rules, edge cases, implementation approach, and documentation expectations.

**Elements of Prompting**

**Role → Task → Audience → Context → Constraints → Output Format → Examples**

1. **Role Assignment:**

Tell the AI who it should act as. Helps set mental frame of the model (senior, junior, architect, reviewer, etc.)

Example roles: “senior Python developer”, “friendly customer support agent”, “business analyst for executives”.

### Effective Role Patterns

|  |
| --- |
| Generic: "Help me with this code"  Role-Based: "As a senior .NET architect, review this code"  ------  Generic: "Write a database query"  Role-Based: "As a DBA optimizing for SQL Server 2022, write a query"  ------  Generic: "Explain this error"  Role-Based: "As a debugging expert, analyze this stack trace and suggest fixes" |

1. **Audience**The target for whom you are generating the code. Shapes tone, complexity, and style.

Examples: “beginner developers”, “C-level executives”, “children aged 10–12”.

Audience is mostly combined with Role:

* "As a tech lead, explain microservices to a **junior developer** who knows monoliths"
* "As a security expert, review this authentication code and explain vulnerabilities to a **developer unfamiliar** with OWASP guidelines"
* "As a performance engineer, analyze this LINQ query and explain the optimization to **someone who understands SQL** but not Entity Framework internals"

1. **Task Clarity and Specification:**Every word in your prompt either adds signal or adds noise. Must be action-oriented and clear. Vague terms like "**good," "clean," "efficient," or "proper"** mean different things to different people and different things to AI models depending on context.
   1. **Specific Spectrum:**

Level 1 (Vague): "Write good code"

Level 2 (Better): "Write maintainable code"

Level 3 (Good): "Write code with clear variable names and single-responsibility functions"

Level 4 (Precise): "Write Python code following SOLID principles, with methods under 20 lines,

descriptive snake-case names, and XML documentation for public members"

* 1. **Quantify When Possible:**

|  |  |
| --- | --- |
| **Vague** | **Specific** |
| "Make it fast" | "Optimize for O(n) time complexity" |
| "Add error handling" | "Wrap in try-catch, log to ILogger, return Result<T>" |
| "Write tests" | "Write xUnit tests with 3 happy path and 2 edge cases" |
| "Keep it simple" | "Use no external dependencies, max 50 lines" |

1. **Context Setting:**

Context is the invisible contract between you and the AI. Without it, the model makes assumptions. Context makes responses situationally correct.

**Example:** The function will be used in a user registration system and will receive a single string input.

* What is the surrounding code doing?
* What problem are we solving?
* What libraries/patterns does the project use?

1. **Constraints**

* Rules that limit or guide the output.
* Non-functional requirements (performance, security, maintainability)
* Edge cases to handle
* Types of Constraints:
  + Language / tools
  + Length
  + Tone
  + Must include / must avoid
* Example:
  + Use Python 3.12 only
  + Use built-in libraries instead of looking for 3rd party libraries
  + Keep the solution simple and readable.

1. **Output Format**

* Specify how you want the output structured.
* Ensures consistency and easy evaluation.
* Example:
  + Return: (1) the function, (2) a short explanation, (3) sample test cases.
  + *Format the code with clear comments explaining each step, and provide the output as a clean code block*

1. **Examples (Optional but Powerful)**

* Show a sample code. Useful for learning pattern, Naming Convention etc…
* If possible, include both positive and negative examples.

**Example:**

|  |
| --- |
| **Role:**  You are a **Senior Python Software Engineer** with experience in writing production-ready code  **Task:** Design and implement a function that validates whether a given string is a valid email address.  **Audience:** The function is intended for junior developers who will read and reuse this code in a real-world backend application.  **Context / Input:**  Email validation is required for a user registration system. The function will receive a single string input representing an email address.  **Constraints:**   * Language: **Python** * Use **regex-based validation** * Function must:   + Return True for valid email addresses   + Return False for invalid ones * Avoid:   + Overly complex regex   + External libraries * Include:   + Clear function name   + Inline comments * Keep the solution **simple, readable, and production-appropriate**   **Output Format:**  Provide:   * 1. The Python function   2. A brief explanation (2–3 lines)   3. Example usage with at least **3 test cases**   **Examples:** Valid examples:   1. user@example.com 2. john.doe123@gmail.com   Invalid examples:   * user@com * @gmail.com * usergmail.com |

# Comprehensive Hands-On Lab

|  |
| --- |
| **🔬 Lab: The Transformation Challenge**  **Objective:** Transform a vague requirement into a production-quality prompt through iterative refinement.  **Tasks:**   1. Start with this vague requirement: "We need user authentication for our app" 2. Identify all the ambiguities (list at least 8) 3. Add environment context (choose your preferred stack) 4. Add security requirements (password rules, lockout, etc.) 5. Add architecture constraints (layers, patterns, DI) 6. Add output format requirements (what files, what structure) 7. Submit final prompt and evaluate output against production standards   **Expected Outcome:** Your final prompt should be 100-200 words and produce code that could pass a code review. |

### Solution: Here's how a well-crafted prompt might look:

|  |
| --- |
| **Role:** You are a senior Python security architect.  **Task:** Design the authentication flow for user login.  **Requirements**   1. **LoginCommand**    * Accepts email and password    * Input validation using a Python validation approach (e.g., Pydantic / custom validators) 2. **Token Strategy**    * JWT access token with **15-minute expiry**    * Refresh token with **7-day expiry** 3. **Account Lockout**    * Lock account after **5 failed login attempts**    * Lockout duration: **30 minutes** 4. **Audit Logging**    * Log every authentication attempt (success or failure)    * Capture:      + Timestamp      + User identifier (if available)      + Client IP address 5. **Result Pattern**    * Use a Result[T]-style return object instead of raising exceptions    * Explicit success/failure states with error codes/messages   **Context:** You are building a Python-based Web API following Clean Architecture principles, organized into the following layers:   * **API:** HTTP controllers / routers (e.g., FastAPI or Flask blueprints) * **Application** Use-case handlers (Commands / Queries pattern) / Validation logic & Application-level DTOs) * **Domain** (Entities, Value Objects, Business rules (no framework dependencies)) * **Infrastructure** (ORM (e.g., SQLAlchemy),   Users are stored in SQL Server using a Python ORM. Authentication is handled using JWT access tokens and refresh tokens.  **Output Format**   * login\_command.py * login\_command\_handler.py * login\_command\_validator.py * authentication\_result.py (record / dataclass)   All public classes and methods should include docstrings.  **Constraints**   * No external authentication frameworks (e.g., OAuth providers) * Only standard Python crypto / JWT libraries * Password rules:   + Minimum 8 characters   + At least one uppercase letter   + One lowercase letter   + One number   + One special character * Token generation must be thread-safe |

**Prompt Patterns and Techniques**

1. Zero-Shot vs Few-Shot Prompting
2. Chain of Thought (CoT) Reasoning
3. Prompting for Architectural Decisions
4. *Self-Consistency and Verification Prompts*
5. Decomposition and Orchestration
6. Iterative Refinement
7. **Zero-Shot vs Few-Shot Prompting**

* **Zero-shot** means asking the AI to perform a task without providing examples. Use for common tasks/patterns. You rely entirely on the model's training to understand what you want.
* **Few-shot** means providing one or more examples that demonstrate the pattern you expect. The model extracts the pattern from your examples and applies it.

**When to Use Each:**

* Standard, well-known tasks, eg: validation of email address **- Zero Shot**
* Custom naming conventions - **Few Shot**
* Unusual output formats - **Few Shot**
* Company-specific code style – **Few Shot**

You can use this technique for Domain Specific API Code, Custom Exceptions, Test Cases, Documentation etc…

**Partial Prompt Example:**

**Task:** **Create method to update customer address**

**Example 1:**

# Input: Create a method to get user by ID

# Output:

async def get\_user\_by\_id(self, user\_id: int) -> Result[UserDTO]:

user = await self.repository.find\_by\_id(user\_id)

if user is None:

return Result.not\_found(f"User {user\_id} not found")

return Result.success(UserDTO.from\_entity(user))

**Example 2:**

# Input: Create a method to delete a product

# Output:

async def delete\_product(self, product\_id: int) -> Result[bool]:

product = await self.repository.find\_by\_id(product\_id)

if product is None:

return Result.not\_found(f"Product {product\_id} not found")

await self.repository.delete(product)

return Result.success(True)

**Lab: Few-Shot**

1. Find a function in your codebase that has a consistent input/output pattern

2. Write TWO examples showing that pattern

3. Ask Copilot to generate the next instance

4. Did it match your conventions?

5. If not, why? What was missing from the examples?

1. **Chain of Thought (CoT) Reasoning**

Chain of Thought prompting asks the model to show its reasoning step-by-step before providing an answer. This dramatically improves accuracy for complex problems.

* Complex business logic
* Debugging
* Performance optimization
* Architecture decisions
* Algorithm design if step by step logic is required.

**Example1:**
Prompt: I need to find the longest substring without repeating characters. Think through the approach step by step before writing code.

**Example2: Debugging Complex Logic**

Without CoT:

**Prompt: Why does this code return wrong results?**

def **calculate\_total**(order: Order) -> float:

subtotal = sum(item.price \* item.quantity for item in order.items)

discount = 0.1 if order.is\_premium\_member else 0

tax = subtotal \* 0.08

return subtotal - discount + tax

The AI might jump to one issue and miss others.

**With CoT:**

Prompt: Analyze this code step by step. Trace through the calculation for a premium member with a $100 subtotal. Show each intermediate value. Then identify bugs.

Output will be detailed and would include reasoning:

1. **Prompting for Architectural Decisions**

Step-back prompting asks the model to first consider the broader context, principles, or constraints before diving into specifics. This prevents narrow solutions that miss the bigger picture.

**Pattern**: "Before solving X, first consider Y, then apply that understanding to X."

***When to Use Step-Back* :**

* Choosing between technologies or approaches
* Designing system architecture
* Refactoring legacy code
* Performance optimization decisions
* Security implementation choices

***Example: Database Choice***

**Without Step-Back:** Gets a generic comparison that may not fit your needs.

Prompt: Should I use PostgreSQL or MongoDB for my application?

**With Step-Back:**

**Prompt**: Before recommending a database, first analyze these factors:

* 1. Our data characteristics: - Product catalog: 50,000 products, complex nested attributes (varies by category)
     + Orders: 10,000/day, strict consistency required, complex joins for reporting
     + User sessions: 100,000 concurrent, simple key-value, 24hr expiration
     + Analytics events: 5M/day, append-only, queried by date ranges
  2. Our team's expertise: Strong PostgreSQL background, limited NoSQL experience
  3. Our constraints: Azure cloud, must integrate with existing Django application

Based on this analysis, recommend a database strategy.

**Example2: Refactoring Strategy**

**Prompt:**

Before suggesting how to refactor this monolithic Django service, first consider:

1. Current pain points:

- Deployments take 45 minutes and require full regression

- Team of 12 developers frequently has merge conflicts

- Cannot scale the order processing independently from catalog browsing

2. Constraints:

- Cannot pause feature development for more than 2 weeks

- Limited experience with Kubernetes

- Current monitoring is basic (just health checks)

3. Risk tolerance:

- Production handles $2M/day in transactions

- Last major outage cost $50K/hour

Given these factors, recommend a refactoring strategy with phases.

This produces a pragmatic, phased approach rather than an idealistic "rewrite everything as microservices" answer.

**LAB:** Scenario: Your team needs to implement real-time notifications.

Task: Craft a step-back prompt that includes:

1. Your current tech stack and team expertise

2. Scale requirements (users, messages/second)

3. Reliability requirements (can messages be lost?)

4. Budget constraints

5. Existing infrastructure to leverage

Then ask for a recommendation with trade-offs explained.

1. ***Self-Consistency and Verification Prompts***

Self-consistency asks the model to verify its own output, catch errors, and improve quality through explicit self-checking.

Key patterns:

* Generate then verify
* Multiple approaches comparison
* Devil's advocate review
* Test case validation

**Pattern 1: Generate Then Verify**

Write a function to check if a string is a valid palindrome (ignoring spaces and case).

After writing the code, verify it by:

1. Trace through with "A man a plan a canal Panama"

2. Trace through with "race car"

3. Trace through with "hello"

4. Check edge cases: empty string, single character, special characters

If any test fails, fix the code and show the corrected version.

**Pattern 2: Multiple Approaches**

I need to implement rate limiting for a FastAPI endpoint.

Provide three different approaches:

1. Simple in-memory solution

2. Distributed solution with Redis

3. Using a third-party library (slowapi or similar)

For each approach, list pros, cons, and when to use it.

Then recommend which approach fits best for: a startup with 10K requests/hour,

3 API servers behind a load balancer, Redis already in use for caching.

**Pattern 3: Devil's Advocate**

Here's my proposed database schema for a multi-tenant SaaS:

[schema details]

First, explain the strengths of this design.

Then act as a critical reviewer: What are the potential problems?

Consider: query performance, data isolation, scaling challenges, backup complexity.

Finally, suggest specific improvements for each issue identified.

**Pattern 4: Catch bugs in generated code.**

Write a function to merge two sorted lists into one sorted list.

Requirements:

- Input: Two sorted integer lists

- Output: Single sorted list containing all elements

- Must be O(n+m) time complexity

After writing, verify by:

1. Trace through: [1,3,5] and [2,4,6]

2. Trace through: [1,2,3] and [7,8,9] (no interleaving)

3. Trace through: [] and [1,2,3] (empty list)

4. Trace through: [1] and [1] (duplicates)

5. Verify time complexity claim

If any issues found, provide corrected version.

**🔬 Lab: Refactoring with Multiple Patterns**

**Scenario:** Legacy code that needs modernization.

**The Code:**

class ReportGenerator:

def generate(self, report\_type: str, data: Any, include\_header: bool,

include\_footer: bool, format: str, compress: bool) -> str:

result = ""

if include\_header:

if format == "html":

result += "<html><head><title>Report</title></head><body>"

elif format == "csv":

result += "REPORT HEADER\n"

elif format == "json":

result += '{"header": true,'

if report\_type == "sales":

sales\_data = data *# List[Sale]*

for sale in sales\_data:

if format == "html":

result += f"<tr><td>{sale.product}</td><td>{sale.amount}</td></tr>"

elif format == "csv":

result += f"{sale.product},{sale.amount}\n"

elif format == "json":

result += f'{{"product":"{sale.product}","amount":{sale.amount}}},'

elif report\_type == "inventory":

*# Similar nested ifs...*

pass

*# ... more nested conditions for footer, compression, etc.*

return result

**Your Task - Apply these patterns in sequence:**

**Step 1: Chain of Thought Analysis**

Analyze this code step by step:

1. List all the responsibilities this single method has

2. Identify the code smells (name each one)

3. Map which SOLID principles are violated

4. Trace through a call with report\_type="sales", format="html" to show complexity

**Step 2: Step-Back for Strategy**

Before refactoring, consider:

1. The patterns that typically solve these problems (Strategy, Factory, Builder)

2. Our constraint: Must maintain backward compatibility with existing callers

3. Our goal: Enable adding new report types and formats without modifying existing code

Recommend a refactoring strategy with phases.

**Step 3: Few-Shot for Implementation**

Here's how we implement the Strategy pattern in our codebase:

Example - Payment Processing:

from abc import ABC, abstractmethod

from typing import Protocol

class PaymentProcessor(Protocol):

def process(self, request: PaymentRequest) -> PaymentResult: ...

class CreditCardProcessor:

def process(self, request: PaymentRequest) -> PaymentResult:

...

class PayPalProcessor:

def process(self, request: PaymentRequest) -> PaymentResult:

...

class PaymentService:

def \_\_init\_\_(self, processors: dict[PaymentType, PaymentProcessor]):

self.\_processors = processors

def process(self, request: PaymentRequest) -> PaymentResult:

processor = self.\_processors[request.payment\_type]

return processor.process(request)

Now apply this same pattern to the ReportGenerator for report types.

**Step 4: Self-Verification**

Review your refactored code:

1. Verify all original functionality is preserved

2. Show how to add a new report type (prove Open-Closed principle)

3. Show how to add a new format (prove extensibility)

4. Identify any remaining code smells

**🔬 Lab: Debugging with CoT and Verification**

**Scenario**: A function that "mostly works" but has subtle bugs.

**The Code:**

from typing import Generic, TypeVar

T = TypeVar('T')

class **PaginationHelper**(Generic[T]):

def \_\_init\_\_(self, collection: list[T], items\_per\_page: int):

self.\_collection = collection

self.\_items\_per\_page = items\_per\_page

@property

def **item\_count**(self) -> int:

return len(self.\_collection)

@property

def **page\_count**(self) -> int:

return len(self.\_collection) // self.\_items\_per\_page

def page\_item\_count(self, page\_index: int) -> int:

if page\_index < 0 or page\_index > self.page\_count:

return -1

if page\_index == self.page\_count - 1:

return len(self.\_collection) % self.\_items\_per\_page

return self.\_items\_per\_page

def **page\_index**(self, item\_index: int) -> int:

if item\_index < 0 or item\_index > len(self.\_collection) - 1:

return -1

return item\_index // self.\_items\_per\_page

**Your Task: Use Chain of Thought to debug this pagination helper.**

**Test scenario:** Collection of 11 items, 5 items per page.

Trace through each property and method:

1. page\_count property

- Expected: 3 pages (items 0-4, 5-9, 10)

- Actual calculation: 11 // 5 = ?

- Is this correct?

2. page\_item\_count(0) - first page

- Expected: 5

- Trace through the conditions...

3. page\_item\_count(2) - last page

- Expected: 1 (only item index 10)

- Trace through the conditions...

4. page\_item\_count(3) - invalid page

- Expected: -1

- Trace through...

5. page\_index(10) - last item

- Expected: 2 (third page)

- Trace through...

**For each bug found, explain the root cause and provide the fix.**

**Then verify your fixes with the same test cases.**

*🔬* ***Lab: API Design with Templates***

**Scenario: Design a complete API for a new feature.**

**Context: You're building a task management API with FastAPI.**

**Users can:**

- Create tasks with title, description, due date, priority

- Assign tasks to team members

- Add comments to tasks

- Change task status (todo → in\_progress → review → done)

- Filter and search tasks

**Your Task:**

Create prompts using the API design template for these endpoints:

1. **Create Task Endpoint** Use the template with specific constraints:

* Must validate due date is in the future
* Priority: 1-4 (1=critical, 4=low)
* Title: 5-200 characters
* Returns created task with ID and timestamps

1. **List Tasks with Filtering** Consider:

* Pagination (cursor-based vs offset)
* Multiple filter options (status, assignee, priority, date range)
* Sorting options
* Include/exclude completed tasks

1. **Status Transition Endpoint** Step-back consideration:

* Should any status transition be allowed, or only valid progressions?
* What happens to "done" tasks that need to be reopened?
* Who can change status?

**For each endpoint, your prompt should produce:**

1. FastAPI route with Pydantic models
2. Request/response examples
3. Error scenarios
4. Validation rules
5. **Decomposition and Orchestration**

**Breaking Complex Tasks into Prompt Chains**

When a task is too complex for a single prompt, decomposition splits it into manageable steps where each prompt's output feeds the next. This mirrors how experienced developers break down large features into smaller, testable units.

**Why decomposition works:**

* Each step has a focused objective (single responsibility)
* Intermediate outputs can be validated before proceeding
* Errors are isolated and easier to fix
* Complex reasoning is built incrementally

**Examples of When to Use Multiple Prompts:**

* Build a complete CRUD module
* Refactor legacy system
* Design and implement API
* Migrate database schema

#### **Example: Building a Feature with Prompt Chains**

**Task:** Implement a user registration system with email verification.

**Single prompt approach (problematic):**

Build a complete user registration system with email verification,

password hashing, database models, API endpoints, and email templates.

Note: This produces shallow implementations across all areas, often with inconsistencies.

**Decomposed approach:**

**Prompt 1: Design Phase**

Design the data models for a user registration system with email verification.

Requirements:

- User can register with email and password

- Email verification required before login

- Verification tokens expire after 24 hours

- Track failed login attempts for rate limiting

Output:

1. Entity relationship diagram (text-based)

2. SQLAlchemy models with all fields and relationships

3. Pydantic schemas for API requests/responses

Do not implement business logic yet - just the data layer.

**Prompt 2: Core Business Logic**

Using the models from the previous step implement the UserService class with these methods:

1. register\_user(email, password) -> Result[User]

2. verify\_email(token) -> Result[bool]

3. resend\_verification(email) -> Result[bool]

Requirements:

- Password hashing with bcrypt

- Generate secure random tokens

- Check for existing users

- Handle token expiration

Use our Result pattern for error handling. Do not implement the API layer yet.

**Prompt 3: API Layer**

Using the service from previous step implement create FastAPI endpoints:

1. POST /auth/register

2. POST /auth/verify-email

3. POST /auth/resend-verification

Include:

- Request validation with Pydantic

- Proper HTTP status codes

- Error response formatting

- OpenAPI documentation strings

Do not implement email sending yet.

**Prompt 4: Email Integration**

Using the endpoints and service from previous steps:

Implement the email notification layer:

1. EmailService class with send\_verification\_email method

2. Email template for verification (HTML and plain text)

3. Integration with the registration flow

4. Retry logic for failed sends

Use our async patterns with aiosmtplib (async SMTP client for use with asyncio).

**Prompt 5: Testing**

Using the complete implementation:

[Paste all code]

Generate comprehensive tests:

1. Unit tests for UserService (mock database and email)

2. Integration tests for API endpoints

3. Edge cases: duplicate email, expired token, invalid token

Use pytest with fixtures. Include both happy path and error scenarios.

|  |
| --- |
| **🔬 Lab: Decomposition Planning**  **Objective:** Practice breaking down complex tasks into prompt chains.  **Scenario:** You need to build an order processing system with:   * Shopping cart management * Inventory validation * Payment processing * Order confirmation emails * Order history   **Tasks:**   1. **Plan the decomposition:** Write out 5-7 prompts you would use, with:    * Clear objective for each prompt    * Expected output from each    * What context carries forward to the next 2. **Identify dependencies:** Draw a simple diagram showing which prompts depend on outputs from others 3. **Execute the first two prompts:**    * Submit your Prompt 1 (data models)    * Take the output and use it in Prompt 2 (core service)    * Note any adjustments needed in handoff   **Starter structure:**  Prompt 1: Data Models  - Objective: Define Cart, CartItem, Order, OrderItem entities  - Output: SQLAlchemy models + Pydantic schemas  - Carries forward: Model definitions  Prompt 2: Cart Service  - Objective: Implement add/remove/update cart operations  - Input needed: Models from Prompt 1  - Output: CartService class  - Carries forward: Service interface  Prompt 3: ... |

1. **Iterative Refinement:**

Instead of accepting the first output, use follow-up prompts to systematically improve quality. This mimics the code review and iteration process.

**Pattern: Generate → Critique → Improve**

**Step 1: Generate**

Write a Python function to parse and validate configuration from a YAML file.

Support nested keys, environment variable substitution, and type coercion.

**Step 2: Critique**

Review this configuration parser for:

1. Error handling completeness

2. Security issues (path traversal, arbitrary code execution)

3. Performance with large files

4. Edge cases not handled

5. Testability

List specific issues with line references.

**Step 3: Improve**

Refactor this code to address these issues:

Provide the improved version with comments explaining each fix.

**Example: Iterative API Design**

**Step1: Initial Generation Prompt:**

Design a REST API endpoint for bulk user import from CSV.

**Step2: Critique Prompt:**

Analyze this bulk import endpoint for production readiness:

Consider:

1. What happens with 100,000 rows?

2. What if row 50,000 fails validation?

3. How does the client know which rows failed?

4. What about duplicate detection?

5. Memory usage patterns?

6. Timeout handling?

Provide specific issues and severity ratings.

**Step3: Improvement Prompt:**

Refactor the bulk import to address these issues:

Fix all Issues mentioned

Requirements for new design:

- Stream processing (don't load entire file)

- Batch commits (every 100 rows)

- Detailed error reporting per row

- Return job ID for async processing if > 1000 rows

- Duplicate detection by email field

- Progress tracking capability

Meta-prompting uses AI to create optimized prompts for specific tasks. This is powerful for creating reusable templates and improving prompt quality.

**Common Pitfalls to Avoid**

* **Don't** accept boilerplate without understanding it
* **Don't** let Copilot make architectural decisions
* **Don't** skip security review because "AI generated it"
* **Don't** lose your problem-solving muscle - understand before accepting
* **Don't** ignore your instincts if something feels wrong