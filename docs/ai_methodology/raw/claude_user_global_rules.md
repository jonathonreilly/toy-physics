# Claude User-Global Rules (full bodies)

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7`. These rule files
are loaded as user-global instructions on every Claude session on this
machine.

**Workspace:** `/Users/jonreilly/Projects/Physics`

**Source dir:** `/Users/jonreilly/.claude/rules/`

**Scope note:** Verbatim full-body dump of every user-global rule file. These
files appear in the per-conversation system prompt under "user's private
global instructions for all projects" and govern behavior across every
project Claude session opens. They are foundational methodology evidence —
the actual rules that shape every Claude response on this machine.

---

## autonomous-dev.md

**Path:** `/Users/jonreilly/.claude/rules/autonomous-dev.md`

**Bytes:** 7042, **Lines:** 202

```markdown
# Autonomous Development Workflow

> Full pipeline for turning a PRD into shipped code via Ralph autonomous agent loops.

## Overview

The autonomous dev workflow converts a product spec into working code through a structured pipeline. Each step feeds the next. The pipeline runs unattended once launched.

```
PRD/Spec → Architecture Doc → Phase/Story Breakdown → Ralph Loop (build + review) → Push/Merge → Next Phase
```

## Step 1: PRD / Engineering Spec

**Input:** A product requirements document or engineering spec.

**Requirements:**
- Clear feature descriptions with acceptance criteria
- Technical constraints and architecture decisions
- Data models / schema definitions
- API contracts (request/response shapes)
- UI/UX requirements (screens, flows, interactions)

**Output:** A spec file (e.g., `~/Desktop/ProjectName_Engineering_Spec_v2.md`)

## Step 2: Architecture Document

**Input:** The PRD/spec from Step 1.

**What to produce:**
- System architecture (what talks to what)
- Tech stack decisions with rationale
- Data model design (tables, relationships, enums)
- API design (endpoints, auth, error handling)
- Key design patterns and conventions
- Security considerations
- Performance requirements

**Output:** `docs/Architecture.md` or equivalent. Can be embedded in the spec.

## Step 3: Phase / Story Breakdown

**Input:** Architecture doc + spec.

**Process:**
1. Enter plan mode (`EnterPlanMode`)
2. Read the full spec thoroughly
3. Break work into phases (typically 5-6 phases, ~6-8 weeks each)
4. Each phase gets a theme and clear boundary (e.g., "Phase 1: Core Loop", "Phase 2: Rich Interactions")
5. Each phase contains 7-17 stories, ordered by dependency
6. Each story is sized for a single Ralph iteration (1-3 hours of Opus work)
7. Stories include: layer (Backend/iOS/Web/All), size (S/M/L), dependencies, what to build, done-when criteria
8. Get user approval via `ExitPlanMode`

**Story sizing guidelines:**
| Size | Scope | Estimated Time |
|------|-------|----------------|
| S | Single file, simple logic | 15-30 min |
| M | 2-5 files, moderate complexity | 30-90 min |
| L | 5+ files, complex logic, multiple layers | 1-3 hours |

**Output:** Plan file at `.claude/plans/<name>.md`

## Step 4: Ralph Loop Configuration

**Ralph loop** (`ralph.sh`) is the autonomous execution engine. Each iteration:
1. **BUILD pass** — Opus implements stories from the prompt
2. **REVIEW pass** — Opus reviews all changes, fixes bugs, polish, code quality
3. Check for completion promise → if found, run FINAL REVIEW, then exit

### ralph.sh Features
- `--promise "PHASE_N_COMPLETE"` — stop when this text appears in output
- `--session <name>` — tmux session name (if tmux available)
- Automatic `caffeinate -w <PID>` — prevents laptop sleep
- `unset CLAUDECODE` — allows nested Claude sessions
- Sonnet-only subagents via `--append-system-prompt`
- nohup fallback when tmux unavailable
- Logs to `.claude/ralph.log`

### Review Pass Checklist
The review prompt should check for ALL of these:
1. Bugs, logic errors, missing error handling, silent failures
2. Dead code, unused imports, commented-out code, debug statements
3. Naming consistency (camelCase/PascalCase), unclear names
4. Missing accessibility (VoiceOver, Dynamic Type, touch targets)
5. Hardcoded strings, magic numbers
6. Framework anti-patterns (SwiftUI, React, etc.)
7. Project convention compliance (MARK sections, Codable, etc.)
8. API contract correctness (auth checks, CORS, error responses)

### Prompt Structure
```
You are building [Project] — [one-line description]. Read the spec at [path] and the plan at [path].

Execute Phase N stories in order. Previous phases are DONE.

STORY N.1 — [Title]: [What to build]. Commit when done.
STORY N.2 — [Title]: [What to build]. Commit when done.
...

IMPORTANT RULES:
- Previous phases are built. Build ON TOP of them.
- Use conventional commits: feat(scope): description
- Understand what EXISTS before changing anything.
- When ALL stories are complete and committed, output: PHASE_N_COMPLETE
```

## Step 5: Watcher (Auto-Transition Between Phases)

**ralph-watcher.sh** monitors Ralph and auto-transitions between phases:
1. Wait for Ralph PID to exit
2. Check for completion promise in log
3. `git push` the branch
4. `gh pr create` + `gh pr merge --squash`
5. `git reset --hard origin/main` to sync
6. Build next phase prompt from plan file
7. Launch next Ralph loop via `ralph.sh`
8. **Spawn next watcher** (self-chaining through all phases)

### Self-Chaining
```bash
# Launch watcher for Phase 1 → 2 → 3 → 4 → 5
nohup bash .claude/ralph-watcher.sh 1 PHASE_1_COMPLETE 2 &
```

Each watcher spawns the next automatically. Chain stops at Phase 5 (or configured max).

## Step 6: Monitoring

**While running:**
```bash
tail -f .claude/ralph.log           # Ralph build/review output
tail -f .claude/ralph-watcher.log   # Phase transition events
cat .claude/ralph.pid               # Current Ralph PID
ps -p $(cat .claude/ralph.pid) -o pid,etime  # Uptime check
```

**Check GitHub:**
```bash
gh pr list                          # See merged PRs
git log --oneline origin/main -10   # See what landed
```

## When to Use This Workflow

**Use for:**
- Greenfield builds from a spec (new product, major rewrite)
- Large feature sets with clear phases (10+ stories)
- Overnight/unattended development sessions
- Any work where the spec is well-defined and phases are independent

**Don't use for:**
- Quick bug fixes (just fix it directly)
- Exploratory work (no clear spec yet)
- Work requiring frequent human judgment calls
- Anything touching production data or deployments

## Checklist: Launching an Autonomous Build

Before starting, verify:
- [ ] Spec/PRD is complete and saved to a known path
- [ ] Plan is written and approved (`.claude/plans/`)
- [ ] Working in a git worktree (not main branch)
- [ ] `.claude/` directory exists
- [ ] `ralph.sh` is executable and in project root
- [ ] `ralph-watcher.sh` is executable in `.claude/`
- [ ] GitHub repo is **private** (verify: `gh repo view --json isPrivate`)
- [ ] No hardcoded secrets in spec or prompts
- [ ] Laptop plugged in (caffeinate prevents sleep, not discharge)

Then launch:
```bash
# Start Phase 1 Ralph
./ralph.sh --promise "PHASE_1_COMPLETE" "Your prompt here..."

# Start self-chaining watcher
nohup bash .claude/ralph-watcher.sh 1 PHASE_1_COMPLETE 2 > /dev/null 2>&1 &
```

## Recovery

**Ralph stalled (hit 50 iterations without completing):**
```bash
# Check what was accomplished
git log --oneline -20
# Relaunch with adjusted prompt focusing on remaining stories
./ralph.sh --promise "PHASE_N_COMPLETE" "Continue Phase N. Stories X.1-X.5 are done. Complete X.6-X.10..."
```

**Watcher failed (merge conflict, PR issue):**
```bash
# Check watcher log
cat .claude/ralph-watcher.log
# Fix manually, then relaunch watcher for remaining phases
nohup bash .claude/ralph-watcher.sh N PHASE_N_COMPLETE $((N+1)) &
```

**Git lock file:**
```bash
rm -f .git/worktrees/<name>/index.lock
```
```

## coding-style.md

**Path:** `/Users/jonreilly/.claude/rules/coding-style.md`

**Bytes:** 7930, **Lines:** 346

```markdown
# Coding Style Rules

> Swift 6.2+ patterns for iOS development with SwiftUI and SwiftData.

## Core Principles

**Clarity over cleverness:**
- Code should be readable without comments
- Prefer explicit over implicit (when it aids understanding)
- Optimize for the reader, not the writer

**YAGNI (You Aren't Gonna Need It):**
- Don't build features until needed
- No premature abstraction
- Three similar lines > one clever abstraction used once

**Keep it simple:**
- One thing per function
- One primary type per file
- Flat is better than nested

## Swift Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Types, Protocols | PascalCase | `UserProfile`, `Injectable` |
| Variables, Functions | camelCase | `userName`, `fetchUser()` |
| Constants | camelCase | `let maxRetries = 3` |
| Enum cases | camelCase | `.loading`, `.completed` |
| Boolean properties | `is`, `has`, `should` prefix | `isLoading`, `hasContent` |
| Factory methods | `make` prefix | `makeContainer()` |

**Naming quality:**
- Names should reveal intent
- Avoid abbreviations (except universally known: `url`, `id`)
- Use domain terminology consistently

## Swift 6.2 Concurrency

**Default to main actor isolation (Swift 6.2 "Approachable Concurrency"):**
```swift
// For most app code, main actor isolation is appropriate
@MainActor
class ScheduleManager {
    // All properties and methods isolated to main actor
    func updateSchedule() { }
}
```

**Mark parallel work explicitly:**
```swift
// Use @concurrent for work that should run off the main actor
@concurrent
func computeHash(for data: Data) -> String {
    // Heavy computation runs in parallel
}

// Or use nonisolated for pure functions
nonisolated func formatDate(_ date: Date) -> String {
    // No actor state accessed
}
```

**Structured concurrency:**
```swift
// Prefer TaskGroup for parallel work
await withTaskGroup(of: Result.self) { group in
    for item in items {
        group.addTask { await process(item) }
    }
    for await result in group { /* collect results */ }
}

// Use Task for fire-and-forget with proper lifecycle
@State private var task: Task<Void, Never>?

func startWork() {
    task = Task {
        defer { /* cleanup */ }
        try Task.checkCancellation()
        // ... work
    }
}

func cancel() {
    task?.cancel()
    task = nil
}
```

**Sendable compliance:**
```swift
// Value types are Sendable by default if all properties are
struct UserData: Sendable {
    let id: UUID
    let name: String
}

// Reference types need explicit Sendable + synchronization
final class Cache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Data] = [:]
}
```

## SwiftUI Patterns

**View composition:**
```swift
// Keep views small and focused
struct UserCard: View {
    let user: User

    var body: some View {
        VStack {
            UserAvatar(user: user)
            UserInfo(user: user)
        }
    }
}
```

**State management:**
```swift
// Use @State for local view state
@State private var isExpanded = false

// Use @Query for SwiftData
@Query private var users: [User]

// Pass data down, actions up
struct ChildView: View {
    let item: Item
    let onDelete: () -> Void
}
```

**Sheet presentation - use item binding:**
```swift
// GOOD - use item binding
@State private var selectedUser: User?

.sheet(item: $selectedUser) { user in
    UserDetailView(user: user)
}

// AVOID - isPresented with if-let inside causes issues
```

## SwiftData Patterns

**Model definitions:**
```swift
@Model
final class UserStackItem {
    // Always include version for migrations
    var dataVersion: Int = 1

    // Required properties
    var peptideId: String
    var createdAt: Date

    // Relationships on owner side only
    @Relationship(deleteRule: .cascade, inverse: \DosingPlan.stackItem)
    var dosingPlan: DosingPlan?

    // Cascade for owned data, nullify for historical
    @Relationship(deleteRule: .nullify, inverse: \Injection.stackItem)
    var injections: [Injection] = []
}
```

**Querying:**
```swift
// Use #Predicate for type-safe queries
let active = #Predicate<Vial> { $0.status == .active }

// Fetch with sorting
@Query(filter: #Predicate { $0.status == .active },
       sort: \.createdAt, order: .reverse)
private var activeVials: [Vial]
```

**Context operations:**
```swift
// Direct save - no wrapper needed
modelContext.insert(item)
try? modelContext.save()
```

## Error Handling

**Never silent failures:**
```swift
// BAD - error silently ignored
let data = try? JSONDecoder().decode(User.self, from: json)

// GOOD - handle or propagate
do {
    let data = try JSONDecoder().decode(User.self, from: json)
    return data
} catch {
    Log.error("Failed to decode user: \(error)", category: .data)
    throw DataError.decodingFailed(underlying: error)
}
```

**Typed errors when useful:**
```swift
enum SyncError: Error {
    case networkUnavailable
    case authenticationRequired
    case conflictDetected(local: Date, remote: Date)
    case unknown(underlying: Error)
}
```

**Result type for async without throws:**
```swift
func fetch() async -> Result<Data, FetchError> {
    // Return .success or .failure explicitly
}
```

## File Organization

**File structure:**
```
// 1. Imports (grouped)
import SwiftUI
import SwiftData

// 2. Type declaration
struct UserView: View {
    // MARK: - Properties
    @Environment(\.modelContext) private var context
    @Query private var users: [User]
    @State private var searchText = ""

    // MARK: - Body
    var body: some View { }

    // MARK: - Private Methods
    private func deleteUser(_ user: User) { }
}

// 3. Extensions (same file if small)
extension UserView {
    // MARK: - Subviews
    private var searchBar: some View { }
}
```

**When to split files:**
- File exceeds ~400 lines
- Distinct responsibility emerges
- Reusable component identified

## Optionals

**Prefer guard for early exit:**
```swift
func process(user: User?) {
    guard let user else { return }
    // user is now non-optional
}
```

**Use if-let for conditional logic:**
```swift
if let name = user?.name {
    display(name)
} else {
    displayPlaceholder()
}
```

**Avoid force unwrap except:**
- IBOutlets (must be connected)
- Programmer errors (use `fatalError` with message)
- Tests (where failure is expected to fail test)

## Immutability

**Prefer let over var:**
```swift
// Default to let
let config = Configuration()

// Use var only when mutation needed
var results: [Item] = []
for item in source {
    results.append(process(item))
}
```

**Prefer value types:**
```swift
// Structs for data
struct Coordinate: Hashable {
    let latitude: Double
    let longitude: Double
}

// Classes for identity, inheritance, or reference semantics
final class NetworkService { }
```

## Documentation

**When to document:**
- Public APIs
- Non-obvious algorithms
- Business logic rationale
- Workarounds for platform bugs

**When NOT to document:**
- Self-explanatory code
- Implementation details
- Code you didn't change (don't add docs during unrelated edits)

```swift
/// Calculates the serum level at a given time based on pharmacokinetic model.
///
/// Uses a two-compartment model with first-order absorption.
/// - Parameter time: Hours since injection
/// - Returns: Estimated concentration in ng/mL
func serumLevel(at time: TimeInterval) -> Double { }
```

## Anti-Patterns to Avoid

**Don't:**
- Create ViewModels for simple views (use @Query + @State)
- Store user data in UserDefaults (use SwiftData)
- Use `isActive` flags (delete inactive items)
- Add emojis in code or comments
- Create abstractions for single-use code
- Add backwards-compatibility shims unless required

**Watch for:**
- Massive view bodies (extract subviews)
- Deep nesting (flatten with guard/early return)
- Stringly-typed code (use enums)
- Retain cycles in closures (use [weak self] for escaping closures)
```

## git-workflow.md

**Path:** `/Users/jonreilly/.claude/rules/git-workflow.md`

**Bytes:** 6296, **Lines:** 302

```markdown
# Git Workflow Rules

> Conventional commits, atomic changes, and safe practices.

## Conventional Commits

**Format:**
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types (required):**
| Type | When to Use | SemVer |
|------|-------------|--------|
| `feat` | New feature for users | MINOR |
| `fix` | Bug fix for users | PATCH |
| `docs` | Documentation only | - |
| `style` | Formatting, no code change | - |
| `refactor` | Code change, no feature/fix | - |
| `perf` | Performance improvement | PATCH |
| `test` | Adding/fixing tests | - |
| `build` | Build system, dependencies | - |
| `ci` | CI/CD configuration | - |
| `chore` | Maintenance, tooling | - |
| `revert` | Reverting a commit | - |

**Scope (optional but recommended):**
- Use component/feature name: `feat(auth):`, `fix(calendar):`
- Use file/module name for specific changes: `refactor(ScheduleManager):`
- Keep consistent within project

**Description:**
- Imperative mood: "add feature" not "added feature"
- Lowercase first letter
- No period at end
- Max 72 characters

**Examples:**
```
feat(dosing): add 5-day-on/2-day-off schedule type

fix(vials): correct concentration calculation for pre-mixed vials

refactor(TodayView): extract dose card into separate component

docs: update CLAUDE.md with new service documentation

BREAKING CHANGE: rename ScheduleType.fixed to ScheduleType.legacy
```

**Breaking Changes:**
```
feat(api)!: change response format for injection endpoints

BREAKING CHANGE: Response now returns array instead of object.
Migration: Update all callers to handle array response.
```

## Commit Best Practices

**Atomic commits:**
- One logical change per commit
- Should be revertable independently
- Tests should pass after each commit

**Commit message quality:**
- Describe WHAT and WHY, not HOW
- Reference issues: `fix(auth): resolve token refresh race condition (#123)`
- Future reader should understand without reading diff

**Before committing:**
```bash
# Review what you're committing
git diff --staged

# Run tests
xcodebuild test -scheme Jabbit -destination 'platform=iOS Simulator,name=iPhone 17 Pro'

# Check for debug statements
git diff --staged | grep -E "(print\(|console\.log|debugPrint)"
```

## What Never to Commit

**Secrets and credentials:**
- `.env` files
- `credentials.json`, `secrets.yaml`
- API keys, tokens, passwords
- Private keys, certificates

**Build artifacts:**
- `DerivedData/`
- `.build/`
- `*.xcarchive`
- `Pods/` (if using CocoaPods with committed Podfile.lock)

**System files:**
- `.DS_Store`
- `*.swp`, `*~`
- `.idea/`, `.vscode/` (unless team agreed)
- `xcuserdata/`

**Debug code in production paths:**
- Hardcoded test data
- `#if DEBUG` blocks that should be removed
- Commented-out code blocks

## Branch Strategy

**Branch naming:**
```
feature/<description>   # New features
fix/<description>       # Bug fixes
refactor/<description>  # Code improvements
docs/<description>      # Documentation
release/<version>       # Release preparation
hotfix/<description>    # Urgent production fixes
```

**Examples:**
```
feature/add-cycling-schedule
fix/vial-concentration-calc
refactor/extract-dose-formatter
```

**Branch hygiene:**
- Keep branches focused (one feature/fix)
- Rebase on main before merging (when safe)
- Delete merged branches

## Pull Request Guidelines

**PR title:** Use conventional commit format
```
feat(dosing): add support for custom schedule days
```

**PR body template:**
```markdown
## Summary
- Brief description of changes
- Why this change is needed

## Changes
- List of specific changes made
- Files affected

## Test Plan
- [ ] Unit tests pass
- [ ] UI tested on device/simulator
- [ ] Edge cases considered

## Screenshots (if UI changes)
[Before/After screenshots]
```

**PR best practices:**
- Keep PRs focused and reviewable (<400 lines ideal)
- Reference related issues
- Self-review before requesting review
- Respond to feedback promptly

## Dangerous Operations

**NEVER do without explicit user request:**
```bash
# Force push to shared branches
git push --force origin main

# Rewrite published history
git rebase -i origin/main  # on shared branch

# Hard reset losing commits
git reset --hard HEAD~5

# Delete remote branches without checking
git push origin --delete feature-branch
```

**Safe alternatives:**
```bash
# Instead of force push, use force-with-lease
git push --force-with-lease origin feature-branch

# Instead of hard reset, use soft
git reset --soft HEAD~1

# Before deleting, verify branch is merged
git branch --merged main | grep feature-branch
```

## Recovery Commands

**Undo last commit (keep changes):**
```bash
git reset --soft HEAD~1
```

**Recover deleted branch:**
```bash
git reflog
git checkout -b recovered-branch <commit-hash>
```

**Undo a pushed commit:**
```bash
git revert <commit-hash>
git push
```

**Discard all local changes:**
```bash
git checkout -- .
# or
git restore .
```

## Commit Workflow

**Standard workflow:**
```bash
# 1. Check status
git status

# 2. Stage specific files
git add path/to/file.swift

# 3. Review staged changes
git diff --staged

# 4. Commit with message
git commit -m "feat(scope): description"

# 5. Push
git push origin feature-branch
```

**Interactive staging (for partial commits):**
```bash
git add -p  # Stage hunks interactively
```

## Merge vs Rebase

**Use merge when:**
- Merging feature branch to main
- Preserving branch history matters
- Multiple people worked on branch

**Use rebase when:**
- Updating feature branch with main changes
- Cleaning up local commits before PR
- Branch is personal/not shared

```bash
# Update feature branch with main
git checkout feature-branch
git rebase main

# If conflicts, resolve then:
git rebase --continue
```

## Git Hooks Integration

**Pre-commit checks (via hooks in Claude settings):**
- Verify no debug statements (print, console.log)
- Check for secrets patterns
- Run linter/formatter

**Pre-push checks:**
- Verify branch is not main (for direct pushes)
- Run tests
- Verify no WIP commits

## Stashing

**Save work in progress:**
```bash
git stash push -m "WIP: description"
```

**List stashes:**
```bash
git stash list
```

**Apply and keep:**
```bash
git stash apply stash@{0}
```

**Apply and remove:**
```bash
git stash pop
```
```

## performance.md

**Path:** `/Users/jonreilly/.claude/rules/performance.md`

**Bytes:** 8014, **Lines:** 357

```markdown
# Performance Rules

> Context window management for Claude + iOS app performance patterns.

## Claude Code Performance

### Model Selection

| Task Type | Recommended Model | Why |
|-----------|------------------|-----|
| Simple fixes, formatting | Haiku | Fast, cheap, sufficient |
| Standard development | Sonnet | Good balance |
| Complex architecture, difficult bugs | Opus | Deep reasoning needed |
| Planning mode, code review | Opus | Nuanced decisions |

**Switch models when:**
- Simple task taking too long → try Haiku
- Complex task getting confused → escalate to Opus
- Cost-conscious exploration → use Haiku

### Context Window Management

**Your 200k window can shrink to ~70k with too many tools enabled.**

**Best practices:**
- Keep under 10 MCPs enabled per project
- Keep under 80 tools active total
- Disable unused MCPs in project config
- Use `/compact` when approaching limits

**What consumes context:**
- Large file reads (entire files)
- Tool definitions (each MCP adds overhead)
- Conversation history
- Code outputs in responses

**Reduce context usage:**
```
# Instead of reading entire file
Read file.swift  # ~500 lines

# Read specific section
Read file.swift lines 100-150
```

**Use targeted exploration:**
```
# Instead of broad search
Glob **/*.swift  # Returns 200 files

# Be specific
Glob Views/Today/*.swift  # Returns 10 files
```

### Parallel Workflows

**Fork conversations for independent tasks:**
```
/fork  # Creates parallel conversation
```

**Use git worktrees for parallel Claudes:**
```bash
git worktree add ../feature-branch feature-branch
# Run separate Claude instances in each worktree
```

**tmux for long-running commands:**
```bash
tmux new -s dev
# Claude runs commands here
# Detach: Ctrl+B, D
# Reattach: tmux attach -t dev
```

## iOS App Performance

### Main Thread Protection

**Never block main thread with:**
- File I/O
- Network requests
- Heavy computation
- Database queries (even SwiftData)

**Use async/await:**
```swift
// BAD - blocks main thread
let data = try Data(contentsOf: url)

// GOOD - async
let data = try await URLSession.shared.data(from: url).0
```

**Offload heavy work:**
```swift
@MainActor
class ViewModel {
    func processData() async {
        // Heavy computation off main actor
        let result = await Task.detached(priority: .userInitiated) {
            return self.heavyComputation()
        }.value

        // Update UI on main actor
        self.results = result
    }
}
```

### SwiftUI Performance

**Avoid unnecessary redraws:**
```swift
// BAD - entire view redraws on any change
struct ParentView: View {
    @State private var items: [Item] = []
    @State private var searchText = ""

    var body: some View {
        // Both items AND searchText changes redraw everything
        List(items) { item in
            ExpensiveRow(item: item)
        }
        TextField("Search", text: $searchText)
    }
}

// GOOD - isolate state
struct ParentView: View {
    var body: some View {
        VStack {
            ItemList()  // Only redraws when items change
            SearchBar() // Only redraws when searchText changes
        }
    }
}
```

**Use `@Observable` efficiently:**
```swift
@Observable
class ViewModel {
    var items: [Item] = []      // Only views using items update
    var isLoading = false        // Only views using isLoading update
}
```

**Lazy loading for lists:**
```swift
// Use LazyVStack/LazyHStack for long lists
LazyVStack {
    ForEach(items) { item in
        ItemRow(item: item)
    }
}
```

### Memory Management

**Prevent retain cycles:**
```swift
// In closures that escape
someAsyncOperation { [weak self] result in
    guard let self else { return }
    self.handleResult(result)
}

// In delegates
weak var delegate: SomeDelegate?
```

**Watch for SwiftData leaks:**
```swift
// Models hold strong references to relationships
// Use @Relationship carefully with delete rules
@Relationship(deleteRule: .nullify)  // Breaks reference on delete
var parent: Parent?
```

**Profile with Instruments:**
- Allocations: Track memory growth
- Leaks: Find retain cycles
- Time Profiler: Find slow code paths

### SwiftData Performance

**Batch operations:**
```swift
// BAD - individual saves
for item in items {
    context.insert(item)
    try context.save()  // N saves
}

// GOOD - single save
for item in items {
    context.insert(item)
}
try context.save()  // 1 save
```

**Efficient queries:**
```swift
// BAD - fetch all, filter in memory
@Query var allItems: [Item]
var filtered: [Item] { allItems.filter { $0.isActive } }

// GOOD - filter at query level
@Query(filter: #Predicate { $0.isActive })
var activeItems: [Item]
```

**Fetch only what you need:**
```swift
// Use FetchDescriptor for complex queries
var descriptor = FetchDescriptor<Item>(
    predicate: #Predicate { $0.status == .active },
    sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
)
descriptor.fetchLimit = 20  // Don't fetch everything
```

### Algorithmic Efficiency

**Watch for O(n²) patterns:**
```swift
// BAD - O(n²)
for item in items {
    if otherItems.contains(where: { $0.id == item.id }) {
        // ...
    }
}

// GOOD - O(n)
let otherItemIds = Set(otherItems.map(\.id))
for item in items {
    if otherItemIds.contains(item.id) {
        // ...
    }
}
```

**Avoid redundant computation:**
```swift
// BAD - computed in every cell
ForEach(items) { item in
    Text(expensiveFormat(item.date))  // Called for every visible cell
}

// GOOD - cache result
struct ItemRow: View {
    let item: Item
    let formattedDate: String  // Computed once

    init(item: Item) {
        self.item = item
        self.formattedDate = expensiveFormat(item.date)
    }
}
```

### Network Performance

**Use URLSession efficiently:**
```swift
// Reuse URLSession
let session = URLSession.shared  // Don't create new sessions

// Use appropriate cache policy
var request = URLRequest(url: url)
request.cachePolicy = .returnCacheDataElseLoad
```

**Background downloads:**
```swift
// For large downloads, use background session
let config = URLSessionConfiguration.background(
    withIdentifier: "com.app.download"
)
let session = URLSession(configuration: config, delegate: self, delegateQueue: nil)
```

### Image Performance

**Downscale images:**
```swift
// Don't load full-resolution for thumbnails
let options = [
    kCGImageSourceThumbnailMaxPixelSize: 200,
    kCGImageSourceCreateThumbnailFromImageAlways: true
] as CFDictionary

if let source = CGImageSourceCreateWithURL(url as CFURL, nil),
   let thumbnail = CGImageSourceCreateThumbnailAtIndex(source, 0, options) {
    return UIImage(cgImage: thumbnail)
}
```

**Use AsyncImage with phases:**
```swift
AsyncImage(url: imageURL) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image.resizable().aspectRatio(contentMode: .fit)
    case .failure:
        Image(systemName: "photo")
    @unknown default:
        EmptyView()
    }
}
```

### Profiling Checklist

Before shipping:
- [ ] Profile with Time Profiler (no main thread blocks)
- [ ] Check Allocations (memory not growing unbounded)
- [ ] Run Leaks instrument (no retain cycles)
- [ ] Test on oldest supported device
- [ ] Verify scroll performance (60fps in lists)
- [ ] Check launch time (<400ms to first frame)

### Quick Wins

**Lazy properties:**
```swift
lazy var expensiveObject = createExpensiveObject()
```

**Computed properties vs stored:**
```swift
// If accessed frequently and expensive, cache it
private var _cachedValue: Value?
var computedValue: Value {
    if let cached = _cachedValue { return cached }
    let value = expensiveComputation()
    _cachedValue = value
    return value
}
```

**Avoid string interpolation in loops:**
```swift
// BAD
for i in 0..<1000 {
    log("Processing item \(i)")  // String allocation each time
}

// GOOD - log less frequently or use static strings
for i in 0..<1000 {
    if i % 100 == 0 { log("Processing batch \(i/100)") }
}
```
```

## security.md

**Path:** `/Users/jonreilly/.claude/rules/security.md`

**Bytes:** 6271, **Lines:** 208

```markdown
# Security Rules

> These rules apply to ALL code I write or modify. Security is non-negotiable.

## Secrets and Credentials

**Never in code:**
- API keys, tokens, passwords, or secrets
- Hardcoded encryption keys (generate at runtime, store in Keychain)
- Connection strings with credentials
- Private keys or certificates

**Detection triggers** - warn immediately if I see:
- Strings matching `sk-`, `pk_`, `api_key`, `secret`, `password`, `token` patterns
- Base64-encoded blobs that could be keys
- `.env` files being staged for commit
- `credentials.json`, `secrets.yaml`, or similar files

**Where secrets belong:**
- iOS: Keychain Services (NEVER UserDefaults)
- Environment variables for build-time config
- Secure remote config for runtime secrets

## Keychain Best Practices (iOS)

**Access control - use the most restrictive option:**
```swift
// PREFERRED: Only accessible when device unlocked, this device only
kSecAttrAccessibleWhenUnlockedThisDeviceOnly

// For background refresh needs:
kSecAttrAccessibleAfterFirstUnlock

// Requires passcode to be set:
kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly
```

**NEVER use:**
- `kSecAttrAccessibleAlways` - data accessible even when locked
- `kSecAttrAccessibleAlwaysThisDeviceOnly` - same problem

**What goes in Keychain:**
- Authentication tokens (OAuth, JWT, refresh tokens)
- Encryption keys
- Passwords and PINs
- Sensitive user identifiers

**What does NOT go in Keychain:**
- Large data (use encrypted files with Data Protection)
- Non-sensitive preferences (use UserDefaults)
- Cached data (use file system with appropriate protection)

## Data Protection (iOS)

**File protection classes:**
```swift
// Most restrictive - files only accessible when unlocked
.completeProtection

// Available after first unlock (for background access)
.completeUnlessOpen

// Default - available after first unlock
.completeUntilFirstUserAuthentication
```

**Apply to sensitive files:**
```swift
try data.write(to: url, options: .completeFileProtection)
```

## Secure Enclave

**Use for:**
- Biometric-protected keys
- Cryptographic operations where keys should never leave hardware
- High-security signing operations

```swift
// Create key in Secure Enclave
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
    [.privateKeyUsage, .biometryCurrentSet],
    nil
)
```

## Input Validation

**Validate ALL external input:**
- User input from text fields
- API responses (don't trust server data implicitly)
- Deep links and URL schemes
- File contents from external sources
- Clipboard data

**Never interpolate user input into:**
- SQL queries (use parameterized queries)
- Shell commands (use argument arrays)
- JavaScript (for WebViews)
- Predicates (use format strings with arguments)

```swift
// BAD - SQL injection risk
"SELECT * FROM users WHERE name = '\(userInput)'"

// GOOD - parameterized
let predicate = #Predicate<User> { $0.name == searchTerm }
```

## Network Security

**App Transport Security (ATS):**
- Keep ATS enabled (default)
- Never add blanket exceptions (`NSAllowsArbitraryLoads`)
- If exception needed, use domain-specific exceptions with justification

**Certificate pinning for sensitive APIs:**
```swift
// Implement URLSessionDelegate for pinning
func urlSession(_ session: URLSession,
                didReceive challenge: URLAuthenticationChallenge,
                completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
    // Validate server certificate against pinned certificate
}
```

## OWASP Mobile Top 10 Awareness

| Risk | Mitigation |
|------|------------|
| Improper Platform Usage | Use platform security features correctly (Keychain, Data Protection) |
| Insecure Data Storage | Encrypt sensitive data, use Keychain, enable file protection |
| Insecure Communication | Use TLS 1.3, certificate pinning, ATS |
| Insecure Authentication | Biometrics via LocalAuthentication, secure token storage |
| Insufficient Cryptography | Use CryptoKit, never roll your own crypto |
| Insecure Authorization | Verify permissions server-side, don't trust client |
| Client Code Quality | Input validation, no hardcoded secrets, code signing |
| Code Tampering | Jailbreak detection where appropriate, integrity checks |
| Reverse Engineering | Code obfuscation for sensitive logic (if warranted) |
| Extraneous Functionality | Remove debug endpoints, test accounts, verbose logging |

## Logging Security

**Never log:**
- Passwords or tokens
- Full credit card numbers
- Personal health information
- Biometric data
- Private keys
- Full user input (could contain sensitive data)

**Safe to log:**
- User IDs (not emails unless necessary)
- Timestamps
- Error types (not full error messages with user data)
- Anonymized metrics

## SwiftData/CloudKit Security

**CloudKit considerations:**
- Private database for user data (default)
- Never store unencrypted sensitive data even in private DB
- Be aware CloudKit data can be accessed via iCloud.com
- Consider client-side encryption for highly sensitive fields

**SwiftData:**
- Model properties are stored in SQLite - not encrypted by default
- Enable Data Protection on the container's store file
- Sensitive computed properties should not persist the sensitive value

## Biometric Authentication

**Implement correctly:**
```swift
let context = LAContext()
context.evaluatePolicy(
    .deviceOwnerAuthenticationWithBiometrics,
    localizedReason: "Access your data"
) { success, error in
    // Verify success before granting access
}
```

**Combine with Keychain:**
```swift
// Bind Keychain item to biometric authentication
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    .biometryCurrentSet,  // Invalidates if biometrics change
    nil
)
```

## Code Review Security Checklist

Before approving any code I write:
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on external data
- [ ] Keychain used for sensitive storage (not UserDefaults)
- [ ] Appropriate Data Protection class for files
- [ ] No sensitive data in logs
- [ ] Network calls use HTTPS
- [ ] Error messages don't leak sensitive info
- [ ] No debug/test code in production paths
```

