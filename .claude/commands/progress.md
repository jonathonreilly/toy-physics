# /progress — Research Retrospective

You are the Research Manager reviewing recent progress on this discrete event-network toy physics project.

## Data Collection

1. Run `git log --oneline --since="1 week ago" -50` to see recent commits.
2. Scan `logs/` for files modified in the last 7 days:
   ```bash
   find logs/ -name "*.txt" -mtime -7 | sort -r | head -30
   ```
3. Read the latest 5 entries in `AUTOPILOT_WORKLOG.md`.
4. Scan `.claude/science/` for recent hypothesis, analysis, validation, and write-up documents.
5. Read `README.md` "Current Results" section for confirmed findings.

## Report Sections

### Summary (3 sentences max)
- What was the main thrust of work this period?
- What was the strongest new result?
- What is the current frontier?

### Hypotheses Tested

| Hypothesis | Status | Confidence | Source |
|------------|--------|------------|--------|
| ... | SUPPORTED/REFUTED/AMBIGUOUS | HIGH/MED/LOW | analysis doc |

### Key Findings
- Numbered list of quantitative results confirmed this period.
- For each: one sentence + source log file.

### Failed / Dead Ends
- What was tried and didn't work?
- Why? (Bug, artifact, wrong parameter regime, genuinely null result?)
- Is it worth revisiting or is it definitively closed?

### Frontier Map
- What has been explored?
- What remains unexplored?
- Where are the highest-value gaps?

### Automation Health
- How many autopilot runs completed?
- Any lock conflicts or failures?
- Any git sync issues?

### Recommended Next Steps
Prioritized by expected information gain:
1. {highest value experiment}
2. {second highest}
3. {third}

For each: one sentence on why it's high-value and estimated effort (interactive / autopilot / multi-day).

## Output

Write to `.claude/science/progress/{date}-retrospective.md`.

Create the directory if it does not exist.

## Rules

- No lock needed — read-only analysis.
- Be honest about dead ends. They are valuable information.
- Do not pad the report. If it was a slow week, say so.
- Quantify where possible: N experiments, N log files, N confirmed results.
- Distinguish between "confirmed with validation" and "observed but unvalidated."
