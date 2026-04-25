# Claude User-Global Slash Commands (full bodies)

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7`.

**Workspace:** `/Users/jonreilly/Projects/Physics`

**Source dir:** `/Users/jonreilly/.claude/commands/`

**Scope note:** Verbatim full-body dump of every user-global slash command
on this machine. These commands are available across every Claude project
on this machine, in addition to the project-specific commands captured in
`claude_project_commands.md`.

---

## codemap.md

**Path:** `/Users/jonreilly/.claude/commands/codemap.md`

**Bytes:** 1063, **Lines:** 47

```markdown
# /codemap - Update Code Map

Create or update a codemap for quick codebase navigation.

## Instructions

1. **Analyze the codebase structure:**
   - Identify main directories and their purposes
   - Find entry points (main files, app delegates, etc.)
   - Map key modules and their responsibilities
   - Identify data flow patterns

2. **Document key files:**
   - Core models/types
   - Main services/managers
   - UI components (if applicable)
   - Configuration files
   - Test structure

3. **Create/update CODEMAP.md:**
   - Place in project root alongside CLAUDE.md
   - Use tree structure for directories
   - Add brief descriptions for each major component
   - Note dependencies between modules
   - Include "quick reference" section for common tasks

4. **Format:**
```markdown
# Codemap

## Quick Reference
- Entry point: [path]
- Models: [path]
- Services: [path]

## Structure
[tree representation]

## Key Components
[descriptions]

## Data Flow
[how data moves through the system]
```

Scope: $ARGUMENTS (or current project root if not specified)
```

## rc.md

**Path:** `/Users/jonreilly/.claude/commands/rc.md`

**Bytes:** 236, **Lines:** 10

```markdown
# /rc - Rigorous Coding

Shorthand to invoke the rigorous-coding skill for substantial code changes.

## Instructions

Invoke the `rigorous-coding` skill immediately. This is a shorthand command.

The user's request follows: $ARGUMENTS
```

## refactor-clean.md

**Path:** `/Users/jonreilly/.claude/commands/refactor-clean.md`

**Bytes:** 875, **Lines:** 30

```markdown
# /refactor-clean - Clean Up Dead Code

Remove dead code, unused files, and clean up the codebase.

## Instructions

1. **Identify dead code:**
   - Search for unused functions, types, and variables
   - Find orphaned files not imported anywhere
   - Locate commented-out code blocks
   - Find unused dependencies

2. **Identify cleanup targets:**
   - Loose .md files that aren't README or CLAUDE.md
   - Empty files or files with only comments
   - Duplicate code
   - Outdated TODO comments

3. **Present findings:**
   - List all items found with file paths
   - Categorize by type (dead code, unused files, etc.)
   - Estimate impact of removal

4. **Get approval before removing:**
   - Use verify-before-execute for bulk deletions
   - Remove items incrementally
   - Verify build still passes after each batch

Scope: $ARGUMENTS (or current project if not specified)
```

## review.md

**Path:** `/Users/jonreilly/.claude/commands/review.md`

**Bytes:** 887, **Lines:** 33

```markdown
# /review - Code Review

Perform a thorough code review of recent changes.

## Instructions

1. **Identify scope:**
   - If $ARGUMENTS specifies files/commits, review those
   - Otherwise, review uncommitted changes (git diff)

2. **Review checklist:**
   - [ ] Logic correctness
   - [ ] Edge case handling
   - [ ] Error handling (no silent failures)
   - [ ] Security (input validation, no injection vectors)
   - [ ] Performance (no obvious bottlenecks)
   - [ ] Code style consistency
   - [ ] Naming clarity
   - [ ] Test coverage

3. **For each issue found:**
   - Categorize: Bug, Security, Performance, Style, Suggestion
   - Provide specific file:line reference
   - Explain the problem
   - Suggest fix if straightforward

4. **Summary:**
   - Overall assessment (approve, request changes)
   - Critical issues that must be fixed
   - Optional improvements

Scope: $ARGUMENTS
```

## tdd.md

**Path:** `/Users/jonreilly/.claude/commands/tdd.md`

**Bytes:** 759, **Lines:** 33

```markdown
# /tdd - Test-Driven Development

Write tests first, then implement.

## Instructions

1. **Understand the requirement:**
   - Clarify what needs to be built/fixed
   - Identify edge cases and failure modes
   - Determine expected behavior

2. **Write failing tests first:**
   - Create test file if needed
   - Write tests that define expected behavior
   - Include happy path and edge cases
   - Run tests to confirm they fail

3. **Implement minimal code:**
   - Write just enough code to pass tests
   - No premature optimization
   - No extra features

4. **Refactor:**
   - Clean up implementation
   - Ensure tests still pass
   - Apply DRY where appropriate

5. **Verify:**
   - Run full test suite
   - Check for regressions

Requirement: $ARGUMENTS
```

## verify.md

**Path:** `/Users/jonreilly/.claude/commands/verify.md`

**Bytes:** 266, **Lines:** 10

```markdown
# /verify - Verify Before Execute

Shorthand to invoke verification before irreversible actions.

## Instructions

Invoke the `verify-before-execute` skill immediately. Present the verification block for the action described.

The user's request follows: $ARGUMENTS
```

