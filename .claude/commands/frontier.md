# /frontier — Frontier Map & Gap Analysis

You are the Research Strategist mapping explored vs. unexplored territory for this discrete event-network toy physics project.

## Data Collection

1. Scan ALL log files in `logs/`:
   ```bash
   ls -la logs/*.txt | wc -l
   ls -la logs/*.txt | tail -20
   ```
2. Scan ALL scripts in `scripts/`:
   ```bash
   ls scripts/*.py | wc -l
   ```
3. Read `README.md` for confirmed results and current frontier description.
4. Read latest `AUTOPILOT_WORKLOG.md` entries (top 10).
5. Read any existing frontier documents in `.claude/science/frontier/`.

## Analysis

### 1. Mechanism Family Census
- Group scripts by mechanism family (pocket_wrap, taper, threshold, wider, etc.)
- For each family: how many scripts, how many log files, what parameter ranges covered.
- Present as a table:

| Family | Scripts | Logs | Parameter Range | Status |
|--------|---------|------|-----------------|--------|
| pocket_wrap | N | N | ... | ACTIVE/EXHAUSTED/PARTIAL |

### 2. Parameter Space Map
- What parameters have been swept?
- What ranges have been covered?
- Where are there GAPS (parameter regions with zero or few data points)?
- Present gaps ranked by expected information value.

### 3. Observable Coverage
- What observables have been measured?
- Which observables have been measured across MULTIPLE families?
- Which observables exist in code but have NOT been measured yet?

### 4. Confirmed vs. Unvalidated
- Results that have been through `/validate`: list them.
- Results that are "observed but not validated": list them.
- Results that were refuted: list them.

### 5. Dead Ends
- Parameter regions or mechanism families that have been exhausted.
- Mark clearly: "do not re-explore unless new theory motivates it."

### 6. Highest-Value Gaps
Rank the top 5 unexplored or under-explored areas by:
- Expected information gain (high if it could confirm or refute a pending hypothesis)
- Feasibility (can it be tested with existing scripts or does it need new code?)
- Estimated effort (interactive / autopilot / multi-day)

## Output

Write to `.claude/science/frontier/{date}-frontier-map.md`:

```markdown
# Frontier Map: {date}

## Coverage Summary
- Total scripts: N
- Total log files: N
- Mechanism families: N
- Confirmed results: N
- Unvalidated observations: N
- Dead ends: N

## Family Census
{table}

## Parameter Space Gaps
{ranked list}

## Observable Coverage
{table}

## Top 5 Highest-Value Gaps
1. {gap} — {why it matters} — {effort level}
2. ...

## Dead Ends (do not revisit)
- {family/region} — {why it's exhausted}
```

## Rules

- No lock needed — read-only analysis.
- Do not fabricate data. If a family has no logs, say "0 logs."
- Distinguish between "unexplored" (never tested) and "exhausted" (tested, nothing there).
- The ranking of gaps by information value is the most important output. Spend the most thought here.
- This skill pairs naturally with `/progress` — run them together for a full research status.
