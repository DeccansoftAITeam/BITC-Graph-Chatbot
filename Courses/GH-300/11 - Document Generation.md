Document Generation

The **/doc** command transforms documentation from a tedious, often-skipped task into an automated process.

**With /doc, documentation goes from "I'll do it later" to "done in 30 seconds".**

**Copilot generates docs in seconds, but you ensure they stay accurate and helpful.**

**/doc Command Variations**

1. **Basic Function Documentation -** Generates JSDoc comment with parameters, return types, and description

/doc #selection

1. **Documentation with Examples -** Adds @example tags with realistic code samples

/doc #selection and include usage examples

1. **Full File Documentation -** Documents every function in the file with consistent format

/doc for all functions in #file

1. **TypeScript Documentation -** Generates documentation that references TypeScript types and interfaces

/doc #selection with TypeScript type annotations

**Example: Generated JSDoc Documentation**

**Before: Undocumented Function**

function calculateDiscount(price, customerType, couponCode) {
  let discount = 0;
  if (customerType === 'premium') discount = 0.15;
  else if (customerType === 'regular') discount = 0.10;
  if (couponCode) discount += 0.05;
  return price \* (1 - Math.min(discount, 0.25));
}

**After: Copilot-Generated Documentation**

/\*\*
 \* Calculates the final price after applying customer tier and coupon discounts.
 \* Maximum total discount is capped at 25%.
 \*
 \* @param {number} price - The original price before discounts
 \* @param {string} customerType - Customer tier: 'premium' (15% off) or 'regular' (10% off)
 \* @param {string} [couponCode] - Optional coupon code for additional 5% discount
 \* @returns {number} Final price after applying discounts
 \*
 \* @example
 \* // Premium customer with coupon
 \* calculateDiscount(100, 'premium', 'SAVE5'); // Returns 80 (20% total discount)
 \*
 \* @example
 \* // Regular customer without coupon
 \* calculateDiscount(100, 'regular'); // Returns 90 (10% discount)
 \*/
function calculateDiscount(price, customerType, couponCode) {
  // ... function body

**Documentation Quality Checklist**

**Always verify generated documentation for:**

* **Accuracy:** Does description match what code actually does?
* **Completeness:** Are all parameters documented? Edge cases mentioned?
* **Type correctness:** Are @param types accurate (number, string, Array, etc.)?
* **Return value:** Is @returns documented with correct type?
* **Examples validity:** Do @example code samples actually work?
* **Edge cases:** Are special conditions (null, empty, boundary) documented?
* **Throws:** If function can throw errors, are they documented with @throws?

**Documentation Workflow:** Generate documentation with **/doc** immediately after writing or updating a function. Don't wait until the end of development — document as you go. Copilot makes it so fast there's no excuse for undocumented code.

**README, API Docs & Inline Comments**

Beyond function documentation, Copilot can generate **README files**, **API documentation**, and **helpful inline comments** that explain complex logic.

**Generating README Files**

**README Generation Strategy**

Create a comprehensive README.md for this project (#file:index.js, #file:package.json).
Include: project description, installation, usage examples, API reference, contributing guidelines.

Copilot analyzes project files and generates structured README

**Standard README Sections Copilot Generates**

* **Project Title & Description:** What the project does and why it exists
* **Installation:** Step-by-step setup instructions with npm/yarn commands
* **Usage:** Basic examples showing how to use the project
* **API Reference:** Main functions/classes with parameters and returns
* **Configuration:** Environment variables and config options
* **Contributing:** How others can contribute (PR guidelines, code style)
* **License:** Project license (MIT, Apache, etc.)
* **Contact/Support:** How to get help or report issues

**API Documentation Generation**

**REST API Documentation:**

**Prompt:** Generate OpenAPI/Swagger documentation for the API endpoints in #file:routes/users.js

Copilot creates OpenAPI spec with paths, parameters, responses, examples

**Example: API Endpoint Documentation**

**Request:**

**Prompt:** Document this API endpoint: #selection

**Copilot generates:**

/\*\*
 \* @api {get} /api/users/:id Get User by ID
 \* @apiName GetUser
 \* @apiGroup Users
 \*
 \* @apiParam {String} id User's unique ID
 \*
 \* @apiSuccess {String} id User ID
 \* @apiSuccess {String} name User name
 \* @apiSuccess {String} email User email
 \*
 \* @apiError UserNotFound The user was not found
 \* @apiError InvalidID The ID format is invalid
 \*/

**What to Include in API Docs**

* Endpoint URL and HTTP method (GET, POST, PUT, DELETE)
* Request parameters (path, query, body) with types and descriptions
* Request body schema (for POST/PUT)
* Response format with status codes (200, 404, 500)
* Authentication requirements (bearer token, API key)
* Example requests and responses
* Error codes and their meanings

**Inline Comments for Complex Logic**

**When to Add Inline Comments**

* **Complex algorithms:** Sorting, searching, optimization logic
* **Business rules:** Calculations based on domain-specific logic
* **Non-obvious optimizations:** Performance tricks that aren't immediately clear
* **Workarounds:** Code that works around library bugs or limitations
* **Magic numbers:** Explain constants like 86400 (seconds in a day)

**Generating Inline Comments**

**Prompt:** Add inline comments to explain the logic in #selection

**Example:**

// Apply customer tier discount (premium: 15%, regular: 10%)
if (customerType === 'premium') discount = 0.15;
else if (customerType === 'regular') discount = 0.10;

// Add coupon discount, but cap total at 25% to maintain margins
if (couponCode) discount += 0.05;
return price \* (1 - Math.min(discount, 0.25));

**Maintaining Documentation Quality**

Generated documentation needs **review and maintenance**. Learn strategies to ensure Copilot-generated docs stay accurate, helpful, and up-to-date as code evolves.

**The Documentation Review Process**

**Step 1: Verify Accuracy:** Check that generated documentation matches code behavior

* Do parameter descriptions match what the code actually uses?
* Is the return type correct?
* Are edge cases mentioned in docs actually handled in code?
* Do example code snippets actually work if you run them?

**Step 2: Add Domain Context:** Enhance with business logic Copilot doesn't know

* Why does this function exist? What business need does it serve?
* Are there compliance or regulatory reasons for specific logic?
* What are the business rules behind magic numbers or thresholds?
* When should/shouldn't this function be used in production?

**Step 3: Improve Examples:** Make examples more realistic and helpful

* Replace generic "foo/bar" with realistic domain data
* Show both success and error cases
* Include common usage patterns from your codebase
* Add edge case examples that developers might not think of

**Step 4: Keep Docs in Sync:** Update docs when code changes

* When you modify a function, re-run /doc and merge changes
* Include documentation updates in PR checklist
* Use linters to flag undocumented public functions
* Review docs as part of code review process

**Documentation Maintenance Workflow**

**When Code Changes**

1. Modify the function code
2. Select the function including old docs
3. Use: /doc #selection and update to reflect recent changes
4. Copilot updates docs, preserving custom additions you made
5. Review merged documentation for accuracy

**Automated Documentation Checks**

Use tools to enforce documentation standards:

* **ESLint plugins:** Require JSDoc for exported functions
* **TypeDoc/JSDoc generators:** Build documentation site from comments
* **PR templates:** Checklist item: "Documentation updated?"
* **CI/CD checks:** Fail builds if public APIs lack documentation

**Documentation Quality Metrics**

|  |  |  |
| --- | --- | --- |
| **Metric** | **Target** | **How to Measure** |
| **Coverage** | 90%+ | % of public functions with JSDoc |
| **Completeness** | All params documented | Check @param tags for all parameters |
| **Examples** | 50%+ have @example | Count functions with usage examples |
| **Freshness** | Updated with code | Docs updated in same PR as code changes |

**Documentation Debt Warning**

Just like code debt, **documentation debt** accumulates when docs aren't maintained. Outdated documentation is worse than no documentation — it misleads developers. Make documentation updates part of your definition of "done" for every PR.