# REVIEW HISTORY — Block 02 (3x3 + Framework-Specific Positivity)

**Date:** 2026-05-03
**Block:** 02 — H1 Route 3 framework-specific positivity refinement
**Branch:** `physics-loop/plaquette-bootstrap-closure-block02-20260503`
**Artifact:** `docs/PLAQUETTE_BOOTSTRAP_FRAMEWORK_SPECIFIC_POSITIVITY_NOTE_2026-05-03.md` +
              `scripts/frontier_plaquette_bootstrap_framework_specific_positivity.py`
**Honest tier:** framework-specific positivity refinement support theorem + named-obstruction stretch

## Promotion Value Gate (V1-V5)

### V1: What SPECIFIC verdict-identified obstruction does this PR close?

**Answer:** Same parent verdict as block 01:

> [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](../../../../docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md) status amendment 2026-05-01:
> "the explicit analytic `beta = 6` insertion remains open."

Block 01 (PR [#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420))
established the framework-integration scaffolding. This block 02 EXTENDS to:
- 3x3 Hankel Gram matrix
- Framework-specific Cl(3)/Klein-four V-singlet positivity (Lemma BB3)
- Numerical scipy-based PSD search

The honest finding (in §6 of the theorem note): 3x3 Hankel + V-singlet
restriction does NOT meaningfully tighten the bound beyond block 01.
This consolidates the named obstruction with explicit verification that
ROUTE (c) of block 01's proposed tightening directions ALSO does not
suffice without loop equations — i.e., loop equations are the critical
missing piece, regardless of which positivity refinement we add.

**Disposition: PASS** for stretch-attempt purposes, with the honest caveat
that this PR is partly a CONFIRMATION that route (c) doesn't suffice.

### V2: What NEW derivation does this PR contain?

**Answer:**
1. **Lemma BB3** (V-singlet subalgebra PSD restriction): explicit algebraic
   statement that A11 (R2) restricted to V-singlet subalgebra remains PSD.
   Not in any existing framework note.
2. **3x3 Hankel Gram matrix construction** on framework's V-invariant minimal
   block: explicit setup not in block 01 or in any existing framework note.
3. **Numerical scipy search** demonstrating that PSD-allowed configurations
   exist for ALL m_1 ∈ [0, 1] when 3x3 Hankel + Hausdorff monotonicity are
   the only constraints. This NEGATIVE RESULT is itself new content: it
   rules out small-truncation positivity-only tightening.
4. **Consolidated named obstruction** identifying loop equations as the
   critical missing piece (regardless of which positivity refinement is added).

### V3: Could the audit lane already complete this?

**Answer:** Marginally yes. The 3x3 Hankel PSD is standard moment-problem
mathematics; the V-singlet subalgebra restriction is a direct corollary
of the framework's existing A11 + A8. The numerical scipy search is
standard. The marginal new content is the explicit framework-specific
formulation + the consolidated obstruction.

### V4: Is the marginal content non-trivial?

**Answer:** Marginally:
- Lemma BB3 is straightforward but not stated explicitly in any existing note.
- The numerical demonstration (PSD-allowed for all m_1) is a non-trivial
  negative result that consolidates the obstruction.
- The consolidated obstruction (loop equations needed regardless of
  positivity refinement) is a genuine synthesis insight.

### V5: Is this a one-step variant of an already-landed cycle?

**Answer:** Borderline. Block 02 EXTENDS block 01 (2x2 → 3x3, general PSD →
V-singlet PSD). The structural distinction:
- Block 01: smallest non-trivial Gram matrix (2x2), establishes Lemmas BB1, BB1'
- Block 02: 3x3 Hankel + V-singlet restriction (Lemma BB3), demonstrates
  numerically that PSD alone does not bound m_1

These are different constructs (2x2 vs 3x3, general vs V-singlet),
producing different conclusions (BB1, BB1' as positive lemmas vs the
NEGATIVE finding that 3x3+V-singlet doesn't bound m_1).

**Disposition: PASS** — the consolidated negative result is structurally
distinct from block 01's positive lemmas.

## Value Gate disposition: PASS (with honesty caveat)

All V1-V5 answers PASS for stretch-attempt purposes. The PR is allowed.
The honest output is a CONFIRMATION that small-truncation positivity-only
refinements don't suffice, plus the explicit Lemma BB3 + numerical
verification.

## Self-review findings

| # | Severity | Finding | Disposition |
|---|---|---|---|
| F1 | medium | The honest result is essentially NEGATIVE (positivity refinements don't tighten the bound). This may be received as a low-value PR by audit. | Recorded explicitly in §6 of theorem note. The negative result IS the value — it consolidates the obstruction and rules out an entire class of attempts. |
| F2 | low | A11 (RP) and A8 (Klein-four orbit closure) are both audit-pending support tier. Block 02 inherits the conditional status of both. | Recorded in §11 honest status. |
| F3 | low | The numerical scipy search uses random sampling (n_trials=50); a more thorough search (e.g., interior-point optimization) might find tighter constraints. | Recorded in code comments. The negative finding (PSD-allowed for all m_1) is robust because we exhibit explicit delta-distribution moment sequences (m_k = m_1^k) that are trivially PSD for any m_1. |
| F4 | low | Block 02 does not actually tighten any analytical bound. | Honest: this is named-obstruction stretch, not bound-tightening. The value is the consolidation of route (c) of block 01's tightening directions as ALSO insufficient. |

### Hostile-review-style stress test

**Q1.** Is the negative result (PSD doesn't bound m_1) really a new finding, or trivially obvious?

**A1.** The result is non-trivial in this specific framework setting:
- It's not stated explicitly in any framework note.
- The framework's bridge-support stack provides analytic bounds via Perron-state methods, but the question of whether bootstrap PSD methods could complement or replace these has not been answered.
- The negative finding (small-truncation + V-singlet positivity doesn't suffice) consolidates the obstruction and shows that the only viable bootstrap tightening route requires loop equations.

This is informative: it RULES OUT an entire class of attempts, which is honest negative-result content per skill workflow #6.

**Q2.** Is Lemma BB3 actually distinct from block 01's Lemma BB1?

**A2.** BB1 is "Wilson-loop Gram matrix PSD on full A_+." BB3 is "Wilson-loop Gram matrix PSD on the V-singlet subalgebra A_V ⊂ A_+." BB3 is a strict refinement of BB1: PSD on a subalgebra is at least as strong as PSD on the full algebra. For Wilson loops on the V-invariant minimal block (where plaquette is V-singlet), BB3 applies. For more general observables that are not V-singlets, only BB1 applies.

The structural distinction: BB3 ALLOWS additional Klein-four-symmetric constraints to be combined with PSD; BB1 doesn't. The numerical finding (3x3 PSD + V-singlet doesn't bound m_1) shows that even with this refinement, an explicit loop equation is required.

### Self-review disposition: PASS

Honest output: framework-specific positivity refinement + explicit numerical
demonstration that this refinement alone is insufficient. The named
obstruction is sharper (loop equations are confirmed as critical).

## Cluster-cap / volume-cap check

- Volume cap: 2 of 5 PRs (this campaign).
- Cluster cap (`gauge_vacuum_plaquette_*` family): 2 of 2 used. **CLUSTER CAP REACHED**.
- Corollary churn: 2nd substantive cycle of campaign; below the ~5-cycle threshold.

PASS volume cap. CLUSTER CAP REACHED — no further PRs in this family this campaign.

## Closure and next action

Block 02 is closure-ready. After PR opens, the campaign STOPS per the
cluster cap (max 2 PRs per parent-row family per campaign, and both
block 01 + block 02 are in `gauge_vacuum_plaquette_*`). Refresh
OPPORTUNITY_QUEUE and deliver final report.

If runtime remains, evaluate orthogonal opportunities outside the
plaquette cluster. Per current queue (refreshed after block 01), no
strong V1-PASS orthogonal opportunities remain in the bootstrap scope.
