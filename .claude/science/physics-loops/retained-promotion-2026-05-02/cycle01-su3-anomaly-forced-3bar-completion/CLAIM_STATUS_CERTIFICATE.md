# Cycle 01 (Retained-Promotion) Claim Status Certificate — SU(3) Anomaly-Forced 3̄ Singlet Completion (closing derivation)

**Block:** physics-loop/su3-anomaly-forced-3bar-completion-derivation-2026-05-02
**Note:** docs/SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_su3_anomaly_forced_3bar_completion.py (PASS=15/0)
**Target row:** su3_cubic_anomaly_cancellation_theorem_note_2026-04-24 (claim_type=positive_theorem, audit_status=audited_conditional, td=134, lbs=B)

## Block type

**Closing derivation** (output type (a) per the new retained-promotion
campaign prompt). New theorem note + runner that **derives the
verdict-identified obstruction** from retained framework primitives,
rather than working around it.

## Promotion Value Gate (V1–V5) — answered in writing per SKILL.md workflow step 7

### V1: SPECIFIC verdict-identified obstruction this PR closes

Quoted from parent row's `verdict_rationale`:

> the cancellation relies on the retained presence and SU(3)
> representations of u_R^c and d_R^c, but those right-handed
> anti-triplets are not established by the provided retained one-hop
> dependencies. The note's reproduction runner passes 33 checks, but
> it checks the hand-entered content table rather than deriving the
> missing matter-content authority. ... Repair target: add or retain a
> one-hop audited theorem deriving the one-generation color-charged
> completion, including u_R^c, d_R^c as left-handed 3bar fields.

**This PR's closing-derivation theorem derives the SU(3) representation
content (3̄) of u_R^c, d_R^c from retained Q_L : (3, 2) + SU(3)^3
anomaly cancellation + minimal-field-count completion, replacing the
hand-coded matter-content table.**

### V2: NEW derivation contained

The parent's runner takes a hand-entered table of fields with their SU(3)
representations and verifies that the cubic anomaly trace `+2 - 1 - 1 = 0`
sums to zero. This is conditional algebra, not a derivation.

This PR's derivation:
1. Catalogues SU(3) cubic-anomaly coefficients for irreps `{1, 3, 3̄, 6,
   6̄, 8, 10, 10̄, 15, 15̄, 27}` (standard reference, role-labelled).
2. Computes `Q_L : (3, 2)` contribution = `2 · A(3) = +2`.
3. Shows no 1-field completion exists (no irrep has `A = -2`).
4. Exhaustively enumerates 2-field completions and shows `{3̄: 2}` is
   the unique minimal solution.
5. Extends to `{6, 6̄, 8, ...}` and confirms `{3̄: 2}` remains uniquely
   minimal — exotic completions don't help.
6. Identifies the 2 LH 3̄ fields as `u_R^c, d_R^c`.

The derivation closes the parent's hand-coded matter-content gap.

### V3: Audit lane couldn't already do this from existing retained primitives + standard math machinery

The math machinery is standard (Diophantine enumeration over irrep anomaly
coefficients), but the framework-side decisions are not:

- **Restriction to LH-Weyl SU(2)-singlet fermions in irreducible SU(3)
  reps** (P3): this restricts the search space to admissible matter
  content within the framework's lattice-fermion + matter-closure
  conventions.
- **Minimal field-count criterion**: this is a framework-level minimality
  principle (separate from anomaly cancellation alone, which has
  infinitely many solutions).

Without these framework-side inputs, the audit lane couldn't conclude
"the SU(3) rep is forced to be 3̄"; it could only say "anomaly
cancellation is consistent with `2 × 3̄` among many other completions".
The framework's matter-content discipline (P3 + minimality) is what
makes this a derivation rather than just a verification.

### V4: Marginal content non-trivial

Yes:
- Standard SU(3) cubic-anomaly coefficient table cited from external
  literature (Slansky 1981 / Cvitanović) — admitted-context external
  reference, role-labelled.
- Diophantine enumeration over compositions: not a textbook identity;
  requires the explicit candidate-rep set + minimal-count constraint.
- Uniqueness of the 2-field minimal solution: requires both Set A
  enumeration and Set B extension to confirm no exotic alternatives.
- Identification step ties the math to SM bookkeeping.

This is genuine derivation content the parent row didn't have.

### V5: Not a one-step variant of an already-landed cycle

No prior cycle (13–52 in the prior campaign or any cycle in this
campaign) attempted matter-content derivation from anomaly cancellation.
Closest related: cycle 42 (B-L anomaly Pattern C, source-tightening only,
on a different anomaly-trace family). Distinct: this PR is a closing
derivation deriving SU(3) rep content from anomaly trace, not a B-L
trace verification.

## Outcome classification (per new prompt)

**(a) Closing derivation.** This PR provides a new theorem note + runner
that **derives the verdict-identified obstruction** from retained
framework primitives. The derivation does not rely on hand-coded matter
content; it forces `{3̄: 2}` from `Q_L : (3, 2)` + anomaly cancellation +
minimal-field-count completion.

The outcome IS retained-positive movement on the parent row's
load-bearing step, conditional on audit-lane ratification of:
- the framework's restriction to LH-Weyl singlets in irreducible reps
  (P3, conventional within lattice-fermion frameworks);
- the minimal-field-count criterion (P3, framework-level minimality).

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Slansky / Cvitanović
  cubic-anomaly coefficient table is standard external mathematical
  reference, role-labelled).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this derivation:
- Parent row `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24`
  load-bearing class-B step closes (matter-content authority is now
  derivable, not hand-coded).
- Downstream rows depending on the SU(3) anomaly cancellation can cite
  this derivation as the audit-retained source for `u_R^c, d_R^c`
  reps (3̄), independent of the conditional `one_generation_matter_closure`
  row's hand-coded content.
- The verdict's specific obstruction is addressed.

## What this proposes

A candidate retained-grade closing derivation of the parent's class-B
load-bearing step. **Audit lane to ratify; no retained-status promotion
asserted in this PR.**

## Honesty disclosures

- The framework-side restriction to `{1, 3, 3̄}` (or extension to
  higher-dim irreps) and the minimal-field-count criterion are
  framework-level conventions, not pure mathematics. The derivation is
  conditional on these conventions being framework-retained.
- The hypercharges `Y(u_R^c), Y(d_R^c)` are NOT derived here; they
  belong to a separate authority row.
- The SU(2)_L singlet labelling distinguishing `u_R^c` from `d_R^c` is
  also separate; the SU(3) rep content alone is the closing derivation
  here.
- The runner does not modify any audit-ledger file. The parent row's
  audit_status remains `audited_conditional` until the audit lane
  reviews this derivation.
