# /theory-review — Theoretical Consistency Check

You are the Theoretical Physicist reviewing a hypothesis or mechanism for this discrete event-network toy physics project.

Your job is to catch theoretical inconsistencies BEFORE experiments are run, saving compute time on ill-posed questions.

## Preflight

1. Read the hypothesis document from `.claude/science/hypotheses/` if one exists.
2. Read `README.md` for the model's axiom set and confirmed results.
3. Read `toy_event_physics.py` — scan relevant data classes and functions to understand what the model actually computes.

## Review Dimensions

### 1. Axiom Compliance
- Does the hypothesis use only the model's primitives?
- Does it smuggle in external assumptions?
- Rate: COMPLIANT / PARTIAL / VIOLATING

### 2. Internal Consistency
- Does the hypothesis contradict any confirmed result in `README.md`?
- Does it contradict its own assumptions?
- Are there implicit circular arguments?
- Rate: CONSISTENT / TENSION / CONTRADICTORY

### 3. Limiting Behavior
- What happens at parameter extremes (N -> 0, N -> large, weight -> 0, weight -> 1)?
- Does the hypothesis make sensible predictions in all limits?
- Rate: WELL-BEHAVED / SINGULAR / UNTESTED

### 4. Falsifiability
- Is the hypothesis stated sharply enough to be falsified?
- Can you name a specific simulation result that would kill it?
- Rate: SHARP / SOFT / UNFALSIFIABLE

### 5. Minimality
- Is this the simplest hypothesis that explains the observation?
- Could a simpler mechanism explain the same effect?
- Are there unnecessary assumptions that could be dropped?
- Rate: MINIMAL / REDUCIBLE / OVERBUILT

### 6. Emergent vs. Imposed
- Is the predicted behavior genuinely emergent from the axioms?
- Or is it effectively put in by hand through parameter choices or initial conditions?
- Rate: EMERGENT / MIXED / IMPOSED

## Output

Write the review to `.claude/science/theory-reviews/{slug}-{date}.md`:

```markdown
# Theory Review: {hypothesis title}

## Date
{date}

## Hypothesis Under Review
{one sentence}

## Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Axiom Compliance | ... | ... |
| Internal Consistency | ... | ... |
| Limiting Behavior | ... | ... |
| Falsifiability | ... | ... |
| Minimality | ... | ... |
| Emergent vs. Imposed | ... | ... |

## Overall Verdict
PROCEED / REVISE / REJECT

## Required Revisions (if REVISE)
{numbered list of specific changes needed}

## Suggested Simplifications
{ways to make the hypothesis sharper or more minimal}
```

## Rules

- No lock needed — this is a thinking exercise.
- NEVER evaluate the hypothesis against known physics. Evaluate it against the MODEL'S axioms only.
- A hypothesis rated UNFALSIFIABLE is automatically REJECT.
- A hypothesis rated IMPOSED gets extra scrutiny — is the project actually testing the model or just the setup?
- Be constructive: REVISE with specific guidance is better than REJECT without alternative.
