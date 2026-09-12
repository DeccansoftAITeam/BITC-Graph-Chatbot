**Overview**

* **Legacy code modernization with Copilot:**understand → test → modernize → verify.
* **Incremental Modernization Strategy:** Don't try to modernize entire codebase at once. Pick **one module at a time**, modernize it completely with tests, then move to the next. This "strangler fig" pattern gradually replaces legacy code while keeping the system functional.

**Refactoring Strategies with Copilot**

Refactoring with Copilot transforms risky, time-consuming work into **guided, systematic improvements.**

**Strategy 1:** *Code works but is hard to read or maintain*

**Workflow:**

1. **Understand:** /explain #selection to understand current behavior
2. **Simplify:** /simplify #selection without changing behavior
3. **Verify:** Run tests to confirm refactoring didn't break anything

**Strategy 2:** *You notice code duplication across files*

**Workflow:**

1. **Extract:** "Extract this repeated logic into a reusable function"
2. **Reuse:** Ask Copilot to find other places using same pattern
3. **Consolidate:** Replace duplicates with extracted function

**Strategy 3:** *Legacy code uses outdated patterns or syntax*

**Workflow:**

1. **Modernize:** "Convert this to async/await" or "Use modern ES6 syntax"
2. **Test:** Generate tests for both old and new versions, verify same behavior
3. **Deploy:** Replace old code with modernized version

**Common Refactoring Tasks**

1. **Simplifying Complex Conditionals -** Copilot converts nested conditionals to guard clauses or early returns

**Prompt:** /simplify #selection - this nested if/else is hard to follow

1. **Extracting Magic Numbers -** Replaces hardcoded values with descriptive constant names

**Prompt:** Extract magic numbers in #selection to named constants

1. **Breaking Down Large Functions -** Copilot identifies logical sections and suggests helper functions

**Prompt:** This function is too long (#selection). Break it into smaller, focused functions.

1. **Removing Code Duplication -** Analyzes multiple files, identifies common patterns, proposes shared functions

**Prompt:** Find duplicated logic in #file:user.js and #file:order.js, suggest shared utility

1. **Converting Callbacks to Promises/Async -** Modernizes async patterns, makes code more readable

**Prompt:** Convert callback-based code in #selection to async/await

**Using /optimize for Performance Refactoring**

**Performance-Focused Refactoring**: Copilot suggests algorithmic improvements, caching, or better data structures

**Prompt:** /optimize #selection - improve performance while maintaining behavior

**Common Optimizations Copilot Suggests**

* **Replace O(n²) with O(n):** Use hash maps for lookups instead of nested loops
* **Add memoization:** Cache expensive computation results
* **Batch operations:** Combine multiple API calls into one
* **Use lazy evaluation:** Don't compute values until needed
* **Optimize React renders:** Add React.memo, useMemo, useCallback

**Refactoring Safety Rules**

* **Always have tests before refactoring:** Tests are your safety net
* **Refactor one thing at a time:** Don't simplify AND optimize simultaneously
* **Verify behavior unchanged:** Run full test suite after each refactor
* **Use version control:** Commit before refactoring so you can revert
* **Understand before changing:** Never refactor code you don't understand

**Legacy Code Modernization & Pattern Extraction**

Legacy code modernization is one of Copilot's most valuable use cases. Learn systematic approaches to **understand, modernize, and extract patterns** from old codebases.

**Legacy Code Modernization Workflow**

1. **Understand Current State -** Copilot explains outdated patterns, dependencies, and potential issues

**Prompt:** /explain #selection - what does this legacy code do and what patterns does it use?

1. **Generate Tests for Current Behavior -** Tests ensure modernization doesn't break existing functionality

**Prompt:** /tests #**selection** to lock in current behavior before modernizing

1. **Modernize Incrementally –** Copilot updates syntax and patterns one section at a time

**Prompt:** **Modernize** #selection: convert to ES6+, use async/await, replace deprecated APIs

1. **Verify with Tests -**

Run tests from Step 2. If they pass, modernization preserved behavior. If they fail, debug and fix.

**Pattern Extraction from Legacy Code**

1. **Identifying Reusable Patterns -** Copilot scans code for duplication and suggests extraction opportunities

**Prompt:** Analyze #file:legacy.js and identify repeated patterns that should be extracted into utilities

1. **Creating Shared Utilities -** Copilot creates centralized utility with all validation patterns

**Prompt:** Extract the validation logic from #file:user.js, #file:order.js, #file:product.js into a shared validation utility module

1. **Establishing Team Patterns**

Once patterns are extracted, they become team standards:

* New code uses extracted utilities (consistency)
* Inline completions learn the pattern and suggest it automatically
* Team has single source of truth for common operations
* Easier onboarding for new developers (patterns are explicit)

**Common Legacy Code Modernizations:**

|  |  |  |
| --- | --- | --- |
| **Legacy Pattern** | **Modern Equivalent** | **Copilot Prompt** |
| var declarations | const/let | Convert var to const/let in #selection |
| Callbacks | Promises/async-await | Convert to async/await |
| function() | Arrow functions | Use arrow functions where appropriate |
| String concatenation | Template literals | Use template literals in #selection |
| Array.prototype.forEach | for...of loops | Replace forEach with for...of |
| Module.exports | ES6 modules | Convert to ES6 import/export |