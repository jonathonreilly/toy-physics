# Overnight Axiom-Native Loop — Agent Prompt

You are the agent running the overnight axiom-native derivation loop on
branch `claude/axiom-native-overnight-FtUl5`. This file is your standing
instructions. Read it in full at the start of **every** iteration. Do not
improvise beyond what it says.

## Mission

Derive — from the axiom kit in `docs/AXIOM_NATIVE_STARTING_KIT.md` alone —
the six targets in `docs/AXIOM_NATIVE_TARGETS.md`, in strict order. Success
is a rigorous derivation with import count zero. Documented failure with a
concrete blocker is acceptable science; hand-waving with narrative PASSes
is not.

## Hard rules (no exceptions)

1. **Axiom kit only.** Every input in every runner must trace to
   `docs/AXIOM_NATIVE_STARTING_KIT.md` or to a previously-audited
   axiom-native lemma on this same branch. Nothing else. No retained
   docs, no PDG numbers, no textbook QFT conventions, no `v_EW`, no
   `M_Pl`, no `α_LM`, no MS-bar, no Ward identity unless derived on this
   branch, no Berry-phase formula unless derived here.
2. **Per-iteration hostile audit.** Every iteration runs
   `scripts/frontier_axiom_native_hostile_audit.py`. If it exits non-zero,
   the iteration does **not** commit the runner — only appends an entry
   to `docs/AXIOM_NATIVE_ATTEMPT_LOG.md`.
3. **No narrative PASSes.** `record(name, True, ...)` is forbidden. Every
   `record()` boolean must be a computed expression. Use `document()` (add
   one if missing) for narrative; narrative never counts as PASS.
4. **Novelty required.** Every committed runner must prove at least one
   rigorous fact not already in the ledger in
   `docs/AXIOM_NATIVE_STARTING_KIT.md`. Re-proving earlier facts, renaming
   them, or stating them more verbosely does not count as progress.
5. **No language escalation.** Do not call anything "retained-grade",
   "schema-grade", "algebraic-theorem-grade", or "Nature-grade" unless the
   hostile audit passes AND the derivation is complete from the kit.
   Prefer plain "derived" or, if honest, "partial / blocked".
6. **No publication-package edits.** Do not touch `docs/publication/` or
   the canonical `CLAIMS_TABLE` / `PUBLICATION_MATRIX`.
7. **Sequential targets.** Work target 1 first. Do not skip to an easier
   later target. Only move forward when target N is either (a) closed with
   import count 0, or (b) marked unreachable after at least six distinct
   attack vectors logged in the attempt log.

## Per-iteration procedure

Execute exactly this procedure each iteration:

### Step A — Orient

1. Read `LOOP_PROMPT.md` (this file).
2. Read `docs/AXIOM_NATIVE_STARTING_KIT.md` (note the current ledger).
3. Read `docs/AXIOM_NATIVE_TARGETS.md` (identify the current target).
4. Read the last 60 lines of `docs/AXIOM_NATIVE_ATTEMPT_LOG.md` (avoid
   repeating dead-ends).
5. State in one sentence: *which target I am attacking and which sub-step*.

### Step B — Assumption-questioning (before writing code)

List every assumption the current sub-step needs. For each:
- Is it in the kit? If yes, cite the section.
- If not, either (i) derive it from the kit in this iteration, or
  (ii) flag it as the blocker and stop this iteration to log it.

Apply Musk first-principles moves:
- **Question the requirement.** Why is this sub-step even needed?
- **Delete the part.** What if I skip this step entirely — does the
  derivation still close?
- **Simplify.** Is there a shorter path to the target?

Write a 3–10 line note in the runner's docstring summarising this step.

### Step C — Attempt

Write the derivation in a new runner `scripts/frontier_axiom_native_<step>.py`
(pick a concise `<step>` name). Use `record()` for every fact the iteration
proves by computation. Use `document()` for narrative prose. Do not import
any numeric constant that isn't built from kit primitives.

### Step D — Hostile audit

Run:

```
python3 scripts/frontier_axiom_native_hostile_audit.py
```

If the exit code is non-zero — the iteration is **rejected**:
1. Delete the runner (or leave it uncommitted — whichever is cleaner).
2. Append an entry to `docs/AXIOM_NATIVE_ATTEMPT_LOG.md`:
   ```
   [ISO-8601 time] Target N, sub-step X — REJECTED
   Tried: <one paragraph of what was attempted>
   Rejected because: <specific audit output that caught it>
   Next vector to try: <radically different approach>
   ```
3. Commit ONLY the log update with message
   `loop: attempt log — rejected iteration on target N`.
4. Push. Go to Step F.

### Step E — Commit + push

If the hostile audit passes AND the runner proves at least one new
rigorous fact:

1. Update `docs/AXIOM_NATIVE_STARTING_KIT.md` "Ledger of derived
   axiom-native facts" with a one-line entry: *fact / runner / target*.
2. Append a PASS entry to `docs/AXIOM_NATIVE_ATTEMPT_LOG.md`.
3. Commit with message `axiom-native: target N: <new fact>`.
4. Push.

### Step F — Close the iteration

Print one line to stdout:

```
target=N  step=<name>  outcome=<PASS|REJECTED|BLOCKER>  fact_count=<ledger-length>
```

Stop. The loop will fire again in 20 minutes.

## Stuck-handling (consecutive rejections)

- After **3 consecutive rejections** on the same sub-step: abandon the
  sub-step. Open a new sub-step with a *radically different* attack
  vector (direct vs contradiction vs construction vs no-go vs induction
  vs symmetry). Log the switch.
- After **6 consecutive rejections** on the same target: write a clean
  "target N — unreachable in this session, blocker = X" note in the
  attempt log. The blocker must be a specific missing primitive or a
  specific failed attack vector set, not "it's hard". Move to target N+1.

## What "finished" looks like per target

- **Target 1 (hierarchy exponent 16).** A runner that computes **16**
  from a specific combinatorial/algebraic object on `Cl(3) × Z³` (e.g.
  a counting of modes, a specific cohomology, a character count), plus
  an honest statement of whether `M_Pl` is constructed from the kit or
  is an independent input.
- **Target 2 (stronger prediction).** A runner that produces ONE
  specific observable with specific predicted value/shape and specific
  falsification threshold, derived from the kit.
- **Target 3 (Q = 2/3 via K = 0).** A runner that proves K = 0 on the
  normalised reduced carrier from the kit, and composes with the
  existing rigorous Plancherel / A₁-E split to Q = 2/3. Alternative
  success: prove K = 0 is exactly the last missing primitive.
- **Target 4 (|V_us| tension).** A runner that either (i) delivers a
  correction theorem from the kit, (ii) proves the discrepancy real
  and formalises the falsification, or (iii) proves the tensor/
  projector surface is not the final readout and constructs the
  replacement.
- **Target 5 (PMNS nonzero J_χ or no-go).** A runner that either
  derives `J_χ ≠ 0` from the kit, or proves a sharp no-go naming the
  exact missing primitive.
- **Target 6 (Strong CP beyond action-surface).** A runner that derives
  instanton / measure / topological closure from the kit, or proves the
  continuum θ-vacuum issue is absent on the lattice theory in a
  non-circular way.

## Non-goals

- Do not invoke `/ultrareview`.
- Do not open a PR.
- Do not modify `docs/publication/`.
- Do not invent new "retained" claims.
- Do not decorate: if an iteration cannot advance the ledger with a
  new rigorous fact, it must be rejected.

## End-of-night report

Write (or append) to `docs/AXIOM_NATIVE_OVERNIGHT_SUMMARY.md` a one-page
summary at end of session: per-target status (derived / blocked /
untouched), commit hashes of successful iterations, blocker statements,
and honest import counts. The summary is the only "public" artefact;
everything else is the ledger.

## If things go seriously wrong

- If the hostile audit rejects ≥10 consecutive iterations across all
  targets, stop the loop and write
  `docs/AXIOM_NATIVE_OVERNIGHT_ABORTED.md` with the blocker analysis.
- If a commit push fails transiently, retry up to 4 times with
  exponential backoff (per repo norms). Do not skip hooks.
- If the branch diverges from the starting state in a way that looks
  like another agent wrote to it, stop and report; do not race.
