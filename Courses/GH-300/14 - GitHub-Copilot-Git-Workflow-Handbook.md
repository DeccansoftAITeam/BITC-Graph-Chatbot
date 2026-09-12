**GitHub Copilot + Git Workflow**

Feature Development Handbook

*Real-World Example: Adding Category to Todo Application*

**AITeam Deccansoft**

AI-Augmented Development Training

# Introduction

This handbook provides a complete, production-ready Git workflow optimized for AI-augmented development with GitHub Copilot. It demonstrates best practices through a real-world example: adding a category feature to a Todo application.

The workflow balances development speed with code quality, leverages AI assistance appropriately, and maintains professional Git hygiene suitable for enterprise teams.

## Technology Stack

* Frontend: React
* Backend: Python FastAPI
* Development Environment: VS Code with GitHub Copilot
* Version Control: Git

## Feature Requirements

**Goal:** Add a category field (Work or Personal) to each todo item

**Implementation:** Backend model update + API changes + Frontend UI

Phase 1: Feature Planning & Setup

## Step 1.1: Understand the Requirement

Before touching code, document the requirement.

Open VS Code and create a new file: **docs/features/todo-categories.md**

**Copilot Prompt in file:**

# Feature: Todo Categories

## Requirement

Press Tab - Copilot will suggest completion. Review and adjust.

**Expected documentation:**

* What: Add category field
* Why: Better organization
* Scope: Predefined categories (Work, Personal)
* Impact: Backend model + API + Frontend UI

## Step 1.2: Check Current State

**Terminal commands:**

# Ensure you're on main branch and up to date

git status

git checkout main

git pull origin main

**Expected output:** "Already up to date" or shows incoming changes

## Step 1.3: Create Feature Branch

**Branch Naming Convention:** feature/<ticket-id>-<short-description>

For training: feature/add-todo-category

# Create and switch to feature branch

git checkout -b feature/add-todo-category

# Verify you're on the new branch

git branch

## Step 1.4: Set Upstream Tracking

# Push branch to remote and set tracking

git push -u origin feature/add-todo-category

**Why this matters:** Enables collaboration, backup, and CI/CD triggers

**Phase 2: Backend Development (Python FastAPI)**

## Step 2.1: Update Database Model

**File:** backend/models/todo.py (or wherever your Todo model is)

**Copilot Chat Prompt:** (Open Copilot Chat: Ctrl+Shift+I or Cmd+Shift+I)

I have a Todo model in this file. I need to add a category field that can only be "Work" or "Personal". What's the best way to implement this with validation?

**Copilot will suggest:** Using Enum or Literal type

**Your implementation (select code and use inline Copilot):**

**Place cursor after existing fields, type:**

# Add category field with Work or Personal options

**Press Tab - Copilot suggests:**

category: str = Field(default="Personal", pattern="^(Work|Personal)$")

**Better approach - prompt Copilot:**

from enum import Enum

class TodoCategory(Enum):

#

Copilot completes:

class TodoCategory(Enum):

WORK = "Work"

PERSONAL = "Personal"

Then in Todo model:

category: TodoCategory = Field(default=TodoCategory.PERSONAL)

## Step 2.2: Create Database Migration

**Terminal:**

# If using Alembic

alembic revision --autogenerate -m "Add category field to todos"

**Review the generated migration file**

**Copilot prompt in migration file:**

Select the upgrade function, ask Copilot Chat:

"Review this migration. Does it handle existing todos properly? Should I add a default value?"

## Make changes based on Copilot's suggestions

## Step 2.3: Run Migration Locally

# Apply migration

alembic upgrade head

# Verify

# Check your database or run Python shell

## Step 2.4: Commit Backend Model Changes

**Before committing, review changes:**

git status

git diff

**Stage files:**

git add backend/models/todo.py

git add alembic/versions/<migration-file>.py

**Write commit message with Copilot:**

git commit

VS Code opens commit editor. Copilot prompt in commit message:

Copilot suggests:

Add category field to Todo model

- Added TodoCategory enum with Work and Personal options

- Created Alembic migration for category field

- Set default category to Personal

**Convention:**

* First line: Summary (50 chars max)
* Blank line
* Detailed description (what and why)

**Save and close editor, then verify:**

git log -1

## Step 2.5: Update API Endpoints

**File:** backend/routes/todos.py

**Copilot Chat prompt:**

I've added a category field to my Todo model (Work or Personal enum). Update the following endpoints to handle category: 1. GET /todos - add optional category filter 2. POST /todos - accept category in request 3. PUT /todos/{id} - allow category updates Show me the changes needed.

For GET endpoint, type:

@router.get("/todos")

async def get\_todos(

# add category filter parameter

Copilot suggests:

category: Optional[TodoCategory] = None, db: Session = Depends(get\_db) ):

## Step 2.6: Add Backend Validation

**Copilot Chat:**

What validations should I add for the category field in my Pydantic schemas?

Implement suggested validations in your schema files.

## Step 2.7: Test Backend Changes

**Create/Update test file:** backend/tests/test\_todos.py

**Copilot Chat:**

Generate test cases for the category functionality:

1. Create todo with Work category

2. Create todo with Personal category

3. Filter todos by category

4. Update todo category

5. Invalid category should fail

Copy suggested tests, review, and run:

# Run tests

pytest backend/tests/test\_todos.py -v

**All tests should pass ✓**

## Step 2.8: Commit Backend API Changes

git status

git add backend/routes/todos.py

git add backend/schemas/todo.py # if updated

git add backend/tests/test\_todos.py

**Commit:**

git commit -m "Add category filtering and validation to Todo API

- Updated GET /todos to support category filter

- Added category field to request/response schemas

- Implemented validation for Work/Personal values

- Added comprehensive test coverage for category feature"

**Phase 3: Frontend Development (React)**

## Step 3.1: Update TypeScript Types

**File:** frontend/src/types/todo.ts

**Copilot prompt (in file):**

// Update Todo interface to include category field (Work or Personal)

export interface Todo {

Copilot suggests adding:

category: 'Work' | 'Personal';

**Better with type safety:**

export type TodoCategory = 'Work' | 'Personal';

export interface Todo

{

id: string;

title: string;

completed: boolean;

category: TodoCategory;

// ... other fields

}

## Step 3.2: Update Todo Form Component

**File:** frontend/src/components/TodoForm.tsx

**Copilot Chat:**

I need to add a category dropdown to my TodoForm component. The options are "Work" and "Personal". Show me how to add this field with proper state management.

In the component, type:

// Add category state

const [category, setCategory] =

Copilot completes state initialization. For the JSX, type:

{/\* Category selector \*/}

<select

Copilot suggests the complete select element:

## <select

## value={category}

## onChange={(e) => setCategory(e.target.value as TodoCategory)}

## className="..."

## >

## <option value="Work">Work</option>

## <option value="Personal">Personal</option>

## </select>

## Step 3.3: Update Todo Display Component

**File:** frontend/src/components/TodoItem.tsx

**Copilot prompt (inline):**

{/\* Display category badge \*/} <span className=

Copilot suggests category badge styling:

<span className={`badge ${todo.category === 'Work' ? 'badge-primary' : 'badge-secondary'}`}> {todo.category}

</span>

## Step 3.4: Update API Service

**File:** frontend/src/services/todoService.ts

**Copilot Chat:**

Update my todoService to:

1. **Include** category when creating todos

2. **Support** filtering todos by category

3. **Update** category field in PUT requests

## Step 3.5: Add Category Filter UI

**File:** frontend/src/components/TodoList.tsx

**Copilot Chat:**

Add a filter dropdown above the todo list to filter by category (All, Work, Personal)

## Implementation:

## // Category filter

## const [filterCategory, setFilterCategory] =

## Copilot suggests state and UI implementation.

## Step 3.6: Test Frontend Changes

## Manual testing checklist (create file: docs/testing/category-feature.md):

## Copilot prompt in file:

## # Testing Checklist: Category Feature

## ## Functionality to Test:

## Copilot suggests test scenarios:

**Manual testing checklist:**

* Create todo with Work category
* Create todo with Personal category
* Filter by Work shows only work todos
* Filter by Personal shows only personal todos
* Filter by All shows all todos
* Update todo category
* Category badge displays correctly
* Category persists after page refresh

**Perform manual testing in browser**

## Step 3.7: Commit Frontend Changes

**Review changes:**

git status git diff

**First commit - Types and services:**

git add frontend/src/types/todo.ts

git add frontend/src/services/todoService.ts

git commit -m "Add category type and API service updates

- Added TodoCategory type definition

- Updated todoService to handle category field

- Added category filtering to getTodos API call"

**Second commit - UI components:**

git add frontend/src/components/TodoForm.tsx

git add frontend/src/components/TodoItem.tsx

git add frontend/src/components/CategoryBadge.tsx

git add frontend/src/components/TodoList.tsx

git commit -m "Add category UI components and filtering

- Added category dropdown to TodoForm

- Created CategoryBadge component for visual display

- Implemented category filter in TodoList

- Updated TodoItem to display category badge"

# Phase 4: Integration & Local Testing

## Step 4.1: Run Full Application

**Terminal 1 (Backend):**

cd backend

source venv/bin/activate # or venv\Scripts\activate on Windows

uvicorn main:app --reload

**Terminal 2 (Frontend):**

cd frontend

npm start

## Step 4.2: End-to-End Testing

Go through testing checklist from Phase 3.6.

Open browser DevTools (F12) → Network tab to verify API calls.

## Step 4.3: Fix Issues (if any)

**Example: Category not saving**

**Copilot Chat:**

When I create a todo, the category isn't being saved. Here's my TodoForm submit handler:

[paste code]

What's wrong?

Copilot identifies the issue. Fix, test, and commit:

git add <fixed-files> git commit -m "Fix category not persisting on todo creation

- Added category field to form submission payload

- Updated default value initialization"

# Phase 5: Code Review Preparation

## Step 5.1: Self-Review Checklist

**Use Copilot for self-review:**

**Copilot Chat:**

Review my recent changes for the category feature. Check for:

1. Code quality issues

2. Missing error handling

3. Security concerns

4. Performance issues

5. Accessibility problems

Here are the files changed:

[Open files in editor or use @workspace]

**Address Copilot's suggestions**

## Step 5.2: Review All Commits

# View all commits in this branch git log main..feature/add-todo-category --oneline

**Expected output:**

a1b2c3d Add category UI components and filtering

e4f5g6h Add category type and API service updates

i7j8k9l Add category filtering and validation to Todo API

m0n1o2p Add category field to Todo model

**Check commit messages are clear and descriptive**

## Step 5.3: Squash if Needed (Optional)

If you have many small "fix" commits:

# Interactive rebase git rebase -i main

**In the editor that opens:**

pick m0n1o2p Add category field to Todo model

pick i7j8k9l Add category filtering and validation to Todo API

pick e4f5g6h Add category type and API service updates

pick a1b2c3d Add category UI components and filtering

squash f1x2y3z Fix typo in CategoryBadge

squash a2b3c4d Fix category filter state

Change **'pick'** to **'squash'** for commits you want to combine.

**Save and close** - Git will prompt for new commit message.

## Step 5.4: Update Documentation

**File:** README.md or docs/features/README.md

**Copilot prompt:**

## Recent Updates

### Todo Categories Feature

Copilot suggests documentation. Commit documentation:

git add README.md docs/ git commit -m "Update documentation for category feature"

## Step 5.5: Push All Changes

# Push feature branch to remote

git push origin feature/add-todo-category

# If you rebased/squashed:

git push origin feature/add-todo-category --force-with-lease

**Note:** **--force-with-lease** is safer than **--force** - it checks no one else pushed changes.

# Phase 6: Pull Request & Review

## Step 6.1: Create Pull Request

**Using GitHub CLI:**

gh pr create --title "Add category feature to todos" --body "## Description

This PR adds category functionality to todos, allowing users to categorize todos as Work or Personal.

## Changes

- Backend: Added category field to Todo model and API

- Frontend: Added category selection and filtering UI

- Tests: Added comprehensive test coverage

## Testing

- [x] Backend tests pass

- [x] Frontend builds successfully

- [x] Manual testing completed

- [x] Category filtering works correctly

## Screenshots

[Add screenshots]

**Or on GitHub.com:**

1. Navigate to repository
2. Click "Pull requests" → "New pull request"
3. Select base: main and compare: feature/add-todo-category
4. Fill in title and description

## Step 6.2: PR Description with Copilot

In GitHub PR editor, use Copilot Chat:

Generate a comprehensive PR description for my category feature. Include:

- Summary of changes

- Technical implementation details

- Testing approach

- Breaking changes (if any)

Copy and paste Copilot's suggestion, review and adjust.

## Step 6.3: Self-Review in GitHub

**On GitHub PR page:**

1. Go to "Files changed" tab
2. Review each file diff
3. Add inline comments where needed

**Use Copilot for explanatory comments:**

Click on a line → "Add comment" → Type:

Why did we

Copilot suggests explanation.

## Step 6.4: Request Reviews

**On PR page:**

Add reviewers (team members)

Add labels (e.g., "enhancement", "frontend", "backend")

Link to issue/ticket if exists

## Step 6.5: Address Review Feedback

**Reviewer comment example:**

"Should we validate category on the frontend before sending to API?"

**Your response:**

Good point! Let me add that.

**Make changes:**

**File: frontend/src/components/TodoForm.tsx`**

**Copilot Chat:**

Add client-side validation to ensure category is either "Work" or "Personal" before form submission

Implement Copilot Suggestion

**Commit and push**

git add frontend/src/components/TodoForm.tsx

git commit -m "Add frontend validation for category field

- Validate category before API submission

- Show error message for invalid category

- Addresses review feedback"

git push origin feature/add-todo-category

**PR automatically updates** with new commits.

**Respond to reviewer:**

| Added validation in commit abc123. Please review again.

## Step 6.6: Get Approval

**Once approved:**

* PR shows "✓ Approved" status
* All CI/CD checks pass (if configured)
* Ready to merge

# Phase 7: Merge & Deployment

## Step 7.1: Final Pre-Merge Checks

**Terminal (on feature branch):**

# Ensure branch is up to date with main

git fetch origin

git merge origin/main

# Resolve conflicts if any

## If conflicts exist:

## VS Code shows conflict markers:

## <<<<<<< HEAD

## category: TodoCategory = Field(default=TodoCategory.PERSONAL)

## =======

## category: str = "Personal"

## >>>>>>> origin/main

## Copilot Chat:

## I have a merge conflict in this file. The feature branch has TodoCategory enum, but main has string. Which approach should I keep and why?

## Resolve conflict, test again, and commit:

## git add <resolved-files>

## git commit -m "Resolve merge conflicts with main"

## git push origin feature/add-todo-category

## Step 7.2: Choose Merge Strategy

**Three options on GitHub PR:**

**1. Create a merge commit** - Preserves all commits

- Use when: Branch has meaningful commit history

**2. Squash and merge** - Combines all commits into one

- Use when: Many small commits, want clean main history

**- Best for this example** (feature is one logical unit)

**3. Rebase and merge** - Replays commits on main

- Use when: Want linear history, commits are clean

## For training, recommend: Squash and merge

## Step 7.3: Perform Merge

**On GitHub PR page:**

1. Click "Squash and merge" button
2. Edit commit message if needed

**Copilot can help with final commit message:**

Add todo category feature (#123)

- Backend: Added TodoCategory enum and database migration

- API: Implemented category filtering and validation

- Frontend: Added category selection dropdown and filter UI

- Tests: Comprehensive test coverage for category functionality

Users can now categorize todos as Work or Personal

1. Click "Confirm squash and merge"
2. Delete branch (GitHub prompts): Click "Delete branch"

## Step 7.4: Local Cleanup

# Switch to main

git checkout main

# Pull merged changes

git pull origin main

# Delete local feature branch

git branch -d feature/add-todo-category

# If branch wasn't fully merged (rare):

# git branch -D feature/add-todo-category

# Verify

git branch

**Expected:** Only main branch locally (or other active branches).

## Step 7.5: Verify Deployment

**If auto-deployment configured:**

* Check deployment pipeline status
* Verify feature in production/staging

**Manual testing in deployed environment:**

* Create todo with category
* Filter by category
* Verify database contains category data

# Phase 8: Cleanup & Documentation

## Step 8.1: Update Project Documentation

**File:** CHANGELOG.md

**Copilot prompt:**

## [Version X.X.X] - 2024-XX-XX

### Added

Copilot suggests:

- Todo category feature: Users can now categorize todos as Work or Personal

- Category filtering in todo list

- Category badge visualization

**Commit:**

git add CHANGELOG.md

git commit -m "Update changelog for category feature"

git push origin main

## Step 8.2: Archive/Close Related Items

* Close GitHub issue (if exists)
* Update project board (if using)
* Mark task complete in tracking system

# Best Practices Summary

## Branch Management

* Create feature branch from updated main
* Use descriptive branch names: feature/, bugfix/, hotfix/
* Set upstream tracking immediately
* Delete merged branches

## Commit Practices

* Small, logical commits (one concern per commit)
* Descriptive commit messages (what + why)
* Commit after tests pass
* Review diffs before committing

## Copilot Integration

* Use Copilot Chat for planning and review
* Verify all Copilot suggestions
* Use Copilot for boilerplate, not critical logic
* Test AI-generated code thoroughly

## Code Review

* Self-review before requesting review
* Respond to all review comments
* Update PR with new commits (don't force-push during review)
* Thank reviewers

## Merge Strategy

* Keep main branch stable
* Test before merging
* Use squash for feature branches
* Clean up after merge

# Common Copilot Prompts Reference

## Planning Phase

"Outline the steps to implement [feature] in [tech stack]"

"What database changes are needed for [feature]?"

"Generate a testing checklist for [feature]"

## Development Phase

"Add [field] to [model] with [constraints]"

"Create API endpoint for [action] with [requirements]"

"Generate tests for [functionality]"

"Update [component] to display [data]"

## Review Phase

"Review this code for security issues"

"Check for performance problems in [code]"

"Suggest improvements for [function]"

"Is there better error handling for [scenario]?"

## Documentation Phase

"Generate API documentation for [endpoint]"

"Create user guide for [feature]"

"Write commit message for [changes]"

# Troubleshooting Common Issues

## Issue: Merge Conflicts

**Solution:**

git fetch origin git merge origin/main

# Resolve conflicts in VS Code

# Ask Copilot: "Help me resolve this merge conflict"

git add .

git commit

## Issue: Accidentally Committed to Main

**Solution:**

# Create feature branch from current state

git checkout -b feature/my-changes

# Reset main to remote state

git checkout main

git reset --hard origin/main

# Continue work on feature branch

## Issue: Need to Undo Last Commit

**Solution:**

# Keep changes, undo commit

git reset --soft HEAD~1

# Discard changes and commit

git reset --hard HEAD~1

## Issue: Pushed Wrong Code

**Solution:**

# If no one else pulled yet

git revert <commit-hash>

git push origin <branch>

# Git Commands Quick Reference

|  |  |
| --- | --- |
| **Command** | **Description** |
| **Status & Info** |  |
| git status | Check current state |
| git log --oneline | View commit history |
| git diff | See unstaged changes |
| git diff --staged | See staged changes |
| **Branch Management** |  |
| git branch | List branches |
| git checkout -b <name> | Create and switch to branch |
| git branch -d <name> | Delete local branch |
| **Committing** |  |
| git add <file> | Stage specific file |
| git add . | Stage all changes |
| git commit -m "msg" | Commit with message |
| **Syncing** |  |
| git fetch origin | Download remote changes |
| git pull origin main | Fetch and merge |
| git push origin <branch> | Push to remote |

# Conclusion

This handbook represents a production-ready workflow that balances development speed with code quality, leverages AI assistance appropriately, and maintains professional Git hygiene suitable for enterprise teams.

By following these phases systematically, developers can:

* Maintain clean, traceable version history
* Leverage GitHub Copilot effectively throughout the development cycle
* Ensure code quality through systematic review processes
* Collaborate efficiently with team members
* Deliver features with confidence

Use this as a template for all feature development in your AI-augmented development training curriculum.

**Happy Coding with GitHub Copilot!**