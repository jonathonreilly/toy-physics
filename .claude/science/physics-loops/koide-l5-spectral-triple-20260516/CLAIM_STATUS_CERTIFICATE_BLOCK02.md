# Claim Status Certificate — Cycle 2 / Block 02

**Loop:** koide-l5-spectral-triple-20260516
**Cycle:** 2
**Date:** 2026-05-16
**Block:** block02 — Block-Diagonality Obstruction (strengthening of Cycle 1)

## Artifact

- **Source note:** `docs/KOIDE_BLOCK_DIAGONAL_OBSTRUCTION_NOTE_2026-05-16.md`
- **Runner:** `scripts/frontier_koide_block_diagonal_obstruction.py`
- **Cached output:** `logs/runner-cache/frontier_koide_block_diagonal_obstruction.txt`
- **Verification:** 18 PASS / 0 FAIL, dominant_class A (18 class-A pattern hits)

## Status fields (after hostile review DEMOTE)

```yaml
actual_current_surface_status: exact-support
target_claim_type: exact_support
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  Hostile review verdict: DEMOTE (same as Cycle 1).

  Main theorem (block-diagonal H + {H, Γ_χ}=0 ⟹ H=0) is a strict
  generalization of Cycle 1 (Z_3-equivariant H + {H, Γ_χ}=0 ⟹ H=0).
  Set-theoretically larger by 3 real dimensions of H closed off.
  Proof is shorter (3-line block decomposition vs Cycle 1's Z_3 Fourier).

  But the V3 reconstruction concern that demoted Cycle 1 is SHARPER
  here: the proof uses only projector calculus, which an audit lane
  derives from L4 + standard math in one paragraph. The new dimensions
  closed off are physically vacuous (no candidate framework realization
  produces block-diagonal-but-not-Z_3-equivariant H).

  Cycle 2 is honest scholarship — proof correct, generalization real,
  comparison to Cycle 1 forthright — but adds limited marginal value
  beyond Cycle 1's exact_support content.

audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## V1-V5 Promotion Value Gate

**V1:** Closes the structural obstruction that connects R1, R2, and
the staggered-Dirac route under a single block-diagonality condition.
Strengthens Cycle 1 by showing the obstruction is more general than
Z_3-equivariance.

**V2:** New derivation: the 3-line block-diagonal proof. Strictly
shorter than Cycle 1's Fourier argument. But the underlying mechanism
is the same (Γ_χ has full-spectrum non-zero eigenvalues, anti-comm
forces each block to zero).

**V3:** Sharper failure than Cycle 1. The proof is a 3-line projector
calculus argument the audit lane derives from L4 §3 directly.
**V3 fails decisively** — reviewer says "an audit lane writes this in
~30 minutes given Cycle 1 + L4."

**V4:** Marginal content non-trivial in pure-math terms (3 extra dims
of H closed off) but physically vacuous (no candidate realization
distinguishes the extra dims).

**V5:** Borderline. Cycle 2 is a strict generalization of Cycle 1
along a coarser eigendecomposition. NOT a relabeling, but the
underlying structural insight is the same.

V3 failure-mode acknowledged via demotion to exact_support.

## Hostile review record

**Reviewer:** internal special-forces hostile reviewer (Cycle 2 review)
**Verdict:** DEMOTE
**Key warning:** "A Cycle 3 in this family would be churn by inspection."

See `REVIEW_HISTORY.md` for the full review record.

## Dependency classes

The runner verifies (purely algebraic, not just numerical):

- Part 1 (5 checks): P_s, P_D projectors; Γ_χ = P_s - P_D
- Part 2 (4 checks): block-diagonal H structure; [H, P_s] = [H, P_D] = 0;
  block-by-block anti-commutator components
- Part 3 (1 check): forcing h_s = 0 and H_D = 0 via the 4-equation system
- Part 4 (3 checks): algebra-equivariance corollary across 3 algebra cases
- Part 5 (2 checks): L4 family escape verification (Σh = 0 → non-block-diagonal)
- Part 6 (1 check): SO(3) premise fails — Γ_χ ∉ commutant(SO(3))

All 6 parts are class-A symbolic checks; no PDG values consumed.

## Campaign-level signal

The Cycle 2 hostile reviewer's verdict of "Cycle 3 churn by inspection"
in this parent-row family is the corollary-exhaustion stop signal.

Remaining ranked opportunities in OPPORTUNITY_QUEUE.md are all either:
- Pattern A variants (corollary churn, blocked by reviewer warning), OR
- Admits-imports routes (Connes-Moscovici, full spectral action) yielding
  bounded_theorem ceiling at best, requiring user direction.

Recommendation: stop the campaign with comprehensive HANDOFF. User
choice to extend with a different exit criterion (accepting bounded
ceilings, or pivoting to a different physics target).
