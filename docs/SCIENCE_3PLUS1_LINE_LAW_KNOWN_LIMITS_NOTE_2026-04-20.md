# Science 3+1 Line Law: Known Limits Note

---

**This is a known-limits / scope-and-caveat overview note for the
3+1 line law surface. It does not establish any retained claim.**
For retained claims on the 3+1 line-law components, see the per-claim
notes referenced from the `## Audit scope` block below.

---

**Date:** 2026-04-20
**Status:** support / known-limits record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / known-limits record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no

## Audit scope (relabel 2026-05-10)

This file is a **known-limits / scope-and-caveat overview note** for
the 3+1 line-law surface on the clean science branch. It is **not** a
single retained theorem and **must not** be audited as one. The
audit ledger row for `science_3plus1_line_law_known_limits_note_2026-04-20`
classified this source as conditional/bounded_theorem with auditor's
repair target:

> add explicit audited dependency edges or a primary runner/proof
> bundle for each step of the closure chain and no-go.

The minimal-scope response in this PR is to **relabel** this document
as a known-limits overview rather than to add audited dependency
edges or a primary runner/proof bundle for each closure-chain step
here. Those steps belong in dedicated review-loop or per-step audit
passes. Until that work is done:

- This file makes **no** retained-claim assertions of its own.
- The "What Is Closed Exactly" canonical-Wilson-branch / `rho1` /
  Givens-grammar / least-distortion / reduced-packet narrative,
  multi-step closure chain, and "What Is Not Claimed" structural
  no-go (compression-interlacing) below are **historical known-
  limits memory only**.
- The retained-status surface for any Wilson/Perron branch,
  retained slice selector, Givens solve, reduced-packet closure,
  or full-packet no-go sub-claim is the audit ledger
  (`docs/audit/AUDIT_LEDGER.md`) plus the per-step theorem notes,
  **not** this known-limits record.
- Retained-grade does **NOT** propagate from this known-limits note
  to any closure step, scope caveat, or successor proof bundle.

For any retained claim about the 3+1 line law or its known limits,
audit the corresponding dedicated note and its runner as a separate
scoped claim — not this known-limits overview.

---

## Purpose

State the strongest theorem-native closure now supported on the clean science
branch, and state the remaining weaknesses precisely so review can evaluate the
result on its actual scope rather than on an overstated claim.

## What Is Closed Exactly

On the selected minimally-positive Wilson branch:

1. The Wilson/Perron completion branch is fixed canonically by the
   minimal-positive extension theorem on the factorized cone.

2. The retained `3d+1` complement-line problem is solved on a bounded positive
   line chart and reduces to an exact two-point orientation doublet.

3. The `rho1` least-distortion rule selects one canonical retained real `3d`
   slice from that solved doublet.

4. Inside that fixed selected slice, the ordered complex-Givens grammar
   `G12 · G13 · G23` contains exact solutions of the reduced projected-source
   packet equation

       (E1, E2, S12, S13).

5. Among those exact reduced-packet solutions, least Frobenius distortion to
   the identity basis selects one canonical internal dressing.

6. That selected dressing reproduces the observed live DM target exactly.

So the strongest exact closure now proved on this retained ambient is:

> canonical Wilson branch
> -> canonical retained real slice
> -> canonical internal reduced-packet dressing
> -> exact reduced projected-source packet
> -> exact live DM target

## What Is Not Claimed

The branch does **not** claim exact equality with the full sparse-face
`9`-channel projected-source packet on the retained `3d+1` ambient.

That stronger statement is ruled out by a structural no-go: the full sparse-face
target block violates compression interlacing against the selected retained
`4x4` Wilson block. So exact full-packet equality is not just unproved; it is
incompatible with this retained ambient.

## Remaining Weaknesses

### 1. The final two selectors are geometric-canonicity laws

The complement-line selector and the internal complex-Givens selector are both
least-distortion rules on exact solved sets.

This is mathematically clean and target-independent, but it is still a
geometric/canonical choice rule. A hard reviewer may still ask whether these
least-distortion rules are forced by deeper Wilson/Perron dynamics, or whether
they are the strongest canonical geometry presently available.

### 2. The solve theorems are numerical exact-solve theorems

The line solve and the complex-Givens solve are exact audited solution-set
theorems with nondegeneracy checks, but they are not symbolic elimination or
closed-form classification theorems.

So the branch supports:

- exact bounded-domain solve,
- isolated solution set,
- nondegeneracy,
- canonical selector on that solved set,

but not a closed-form symbolic description of the entire solution set.

### 3. Scope is reduced-packet exact closure, not full-packet exact closure

This is now an explicit strength/limit pair:

- strength: exact reduced projected-source packet closure is achieved,
- limit: exact full `9`-channel packet closure is impossible on this retained
  ambient.

Any review should judge the branch on that exact scoped claim.

### 4. The closure remains relative to the selected Wilson factorized carrier

The branch now proves the selected branch is canonical inside the factorized
cone, not across all imaginable upstream Wilson completions. So a deeper
challenge could still target the carrier class itself rather than the closure
chain inside it.

## Recommended Reviewer Posture

The clean branch should be read as proving the following:

1. the old review objections about ad hoc branch choice, hardcoded witness
   lines, and witness-only selector comparison have been repaired;
2. the strongest exact closure attainable on the retained `3d+1` ambient is now
   identified;
3. that strongest attainable closure already closes the selected retained-
   ambient Wilson route to the reduced projected-source packet and live target;
4. any remaining objection must therefore be one of:
   - challenge the least-distortion selector nativity,
   - demand symbolic rather than numerical solved-set classification,
   - challenge the factorized carrier itself,
   - challenge equivalence to the manuscript-facing microscopic selector law on
     `dW_e^H`,
   - or demand exact full-packet closure despite the structural no-go.

## Bottom Line

The branch is no longer vulnerable to the original review-note objections.
What remains are higher-bar objections about physical nativity, symbolic
classification, carrier choice, or equivalence to the manuscript-facing
microscopic selector law, not the original internal-consistency failures.
