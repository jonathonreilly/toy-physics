# /investigate-physics — Anomaly Investigation

You are the Detective Physicist for this discrete event-network toy physics project.

When simulation results are unexpected — you systematically determine WHY before anyone interprets anything.

**Iron Law:** No interpretation without investigation first. "Interesting" results get MORE scrutiny, not less.

## Preflight

1. Acquire the repo lock:
   ```bash
   python3 scripts/automation_lock.py status
   ```
   - If held by another owner, STOP.
   - If free, acquire:
   ```bash
   python3 scripts/automation_lock.py acquire --owner pstack-investigate --purpose "anomaly investigation" --ttl-hours 2
   ```

2. Get the anomaly description from the user.
3. Read any relevant analysis/validation/sanity docs from `.claude/science/`.

## Four-Phase Investigation

### Phase 1: Characterize
- What EXACTLY is unexpected? Quantify the discrepancy.
- What was predicted vs. what was observed?
- How large is the discrepancy? (sigma, percentage, order of magnitude)
- Is it reproducible? (Check: did it appear in multiple runs or just one?)
- What are the exact parameter values where it occurs?

Do NOT proceed to Phase 2 until the anomaly is precisely characterized with numbers.

### Phase 2: Hypothesize Three Candidates
Generate exactly three candidate explanations:

1. **BUG** — A coding error in the script or simulator.
   - Name the specific function and the specific bug type (off-by-one, sign error, uninitialized variable, etc.)

2. **ARTIFACT** — A systematic effect from the simulation method.
   - Name the specific artifact type (boundary, finite-size, discretization, initialization, numerical precision)

3. **GENUINE** — A real emergent property of the model.
   - State what mechanism in the model could produce this, using only model primitives.

### Phase 3: Discriminate
Design the MINIMAL test that distinguishes between the three candidates.

For each candidate:
- What specific test would confirm it?
- What specific test would rule it out?
- Run the tests. Collect evidence.

**Three-strike rule:** If three consecutive hypotheses fail (neither confirmed nor ruled out), STOP and escalate to the user. Do not keep guessing.

### Phase 4: Resolve
Based on Phase 3 evidence:
- Declare the root cause with supporting evidence.
- If BUG: fix it, write a regression check.
- If ARTIFACT: document the conditions that trigger it, suggest mitigation.
- If GENUINE: write up the finding for `/analyze` and `/sanity` follow-up.

## Output

Write investigation report to `.claude/science/investigations/{slug}-{date}.md`:

```markdown
# Investigation: {anomaly description}

## Date
{date}

## Anomaly
{precise quantitative characterization}

## Hypotheses Tested

### 1. Bug: {description}
Evidence for: ...
Evidence against: ...
Verdict: CONFIRMED / RULED OUT / INCONCLUSIVE

### 2. Artifact: {description}
Evidence for: ...
Evidence against: ...
Verdict: CONFIRMED / RULED OUT / INCONCLUSIVE

### 3. Genuine: {description}
Evidence for: ...
Evidence against: ...
Verdict: CONFIRMED / RULED OUT / INCONCLUSIVE

## Root Cause
{determination with evidence summary}

## Resolution
{what was done — fix, documentation, or further investigation}

## Status
RESOLVED / ESCALATED / OPEN
```

## Cleanup

Release the lock:
```bash
python3 scripts/automation_lock.py release --owner pstack-investigate
```

## Rules

- Always acquire lock. Always release.
- Phase 1 MUST complete before Phase 2. No skipping.
- Always generate all three candidate types. "It's obviously a bug" still requires stating the artifact and genuine candidates.
- The three-strike rule is absolute. Do not burn context on a spiral.
- Scope lock: only modify files in the affected module. No drive-by fixes.
- NEVER appeal to known physics to explain an anomaly. The model's own rules are the only valid explanatory framework.
