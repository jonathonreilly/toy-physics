# Claude Execution Instructions

**Date:** 2026-04-12  
**Branch:** `claude/youthful-neumann`

Read only these two files before working:

1. `instructions.md` — execution rules
2. `review.md` — Codex-audited paper state and live blockers

If older notes or scripts conflict with `review.md`, follow `review.md`.

## Mission

Use Claude time on execution, derivation attempts, and clean theorem-boundary
 notes. Do not spend time doing broad review. Codex will review the deltas.

## Working rules

1. Work from the audited state in `review.md`, not from older broader claims.
2. A lane is `closed` only if the theorem surface is actually first-principles.
3. If a result is model-dependent, fitted, finite-size anchored, or uses an
   extra assumption, label it `bounded`.
4. If the surface cannot currently close, document the obstruction cleanly.
5. Do not widen assumptions silently.
6. Do not use “gate closed”, “theorem proved”, or similar language unless the
   final note and script match the audited surface exactly.

## Priority order

1. generation physicality
2. `S^3` compactification / cap-map uniqueness
3. DM relic mapping
4. renormalized `y_t` matching
5. CKM only if the Higgs `Z_3` step becomes genuinely `L`-independent

## What counts as useful work

Useful:

- a genuinely new theorem or obstruction on the current surface
- a script with exact checks separated from bounded/model checks
- a note that narrows a lane to the strongest honest paper-safe claim
- replacing stale overclaiming notes with clean boundary notes

Not useful:

- re-asserting an already-audited claim with stronger rhetoric
- calling a modeled benchmark “closure”
- broad phenomenological prose without a tighter theorem surface

## Required outputs for every serious attempt

For each lane touched, produce:

1. one note in `docs/`
2. one runnable script in `scripts/`

Naming pattern:

- `docs/<LANE>_NOTE.md` or `docs/<LANE>_THEOREM_NOTE.md`
- `scripts/frontier_<lane>.py`

Every note must contain these sections:

1. `Status`
2. `Theorem / Claim`
3. `Assumptions`
4. `What Is Actually Proved`
5. `What Remains Open`
6. `How This Changes The Paper`
7. `Commands Run`

Every script must:

- end with a clear `PASS=n FAIL=m`
- separate exact checks from bounded/model checks
- avoid unconditional `True` theorem checks except for clearly labeled
  supporting remarks

## Mandatory handoff packet

Before asking Codex to review, create or update:

- `docs/CODEX_REVIEW_PACKET_2026-04-12.md`

For each touched lane include:

- files changed
- commands run
- final exit code
- claimed status: `closed`, `bounded`, or `open`
- one paragraph explaining why the claim is not overstated

## Fast paper-safe reminders

- Time / `3+1`: closed on the single-clock codimension-1 theorem surface
- RH matter: closed at the full-framework level, not from the spatial graph alone
- Generation physicality: still open
- CKM: still bounded unless the Higgs `Z_3` step is made universal

## Immediate tasking

Start with the highest-value open gate from `review.md`.

