# REVIEW HISTORY — Block 01 (Bootstrap framework integration)

**Date:** 2026-05-03
**Block:** 01 — H1 Route 3 framework integration: bootstrap via reflection positivity + smallest 2x2 Gram matrix
**Branch:** `physics-loop/plaquette-bootstrap-closure-block01-20260503`
**Artifact:** `docs/PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md` +
              `scripts/frontier_plaquette_bootstrap_framework_integration.py`
**Honest tier:** framework-integration support theorem + named-obstruction stretch

## Promotion Value Gate (V1-V5)

### V1: What SPECIFIC verdict-identified obstruction does this PR close?

**Answer:** [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](../../../../docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
status amendment 2026-05-01:

> "the explicit analytic `beta = 6` insertion remains open."

This PR addresses the obstruction by establishing the modern lattice
bootstrap (Anderson-Kruczenski 2017; Kazakov-Zheng 2022, 2024;
JHEP 12(2025) 033 SU(3)) as a viable attack route on the framework's
retained surface. Lemma BB1 establishes that the framework's
existing reflection-positivity theorem (A11,
[`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md))
is sufficient as the load-bearing positivity input for Wilson-loop
Gram matrix PSD — i.e., the bootstrap can be done inside the
framework without external positivity assumptions.

The PR does not close `⟨P⟩(β=6)`, but it sharpens the named
obstruction by:
1. Identifying the smallest non-trivial 2x2 Gram matrix as
   equivalent to connected correlator non-negativity (BB1').
2. Computing the mixed-cumulant audit estimate (~0.35-0.48), which
   is far below MC 0.5934 due to strong-coupling expansion's
   non-convergence at β=6.
3. Identifying three explicit tightening routes: (a) Migdal-Makeenko
   on framework surface, (b) industrial SDP, (c) framework-specific
   positivity (block 02).

**Disposition: PASS** for stretch-attempt purposes. V1 directly
addresses the named verdict obstruction with a new attack route
(bootstrap via RP).

### V2: What NEW derivation does this PR contain?

**Answer:** Yes:
1. **Lemma BB1** (Wilson-loop Gram matrix PSD from A11): direct
   restriction of A11's R2 (PSD bilinear form on `A_+`) to the
   Wilson-loop subalgebra. New framework-internal mapping; not in any
   existing framework note.
2. **Lemma BB1'** (connected reflected-plaquette correlator
   non-negativity): RP applied to mean-subtracted observables gives
   an explicit algebraic statement equivalent to BB1 for the 2x2 case.
3. **Mixed-cumulant + bootstrap framing**: combines the framework's
   exact mixed-cumulant audit (`P_full(β) = P_1plaq(β) + β^5/472392 +
   O(β^6)`) with the bootstrap structure to give an explicit
   analytical estimate at β=6.

The lemmas are not in any existing framework note. The framework-
integration mapping (bootstrap ⟷ RP theorem ⟷ Gram matrix PSD) is
new structural content.

### V3: Could the audit lane already complete this?

**Answer:** Partially. The audit lane has A11 (RP) and the bridge-support
stack with mixed-cumulant audit. Combining these via the bootstrap
framing is a structural insight that the audit lane has not made
explicitly. The framework-integration mapping is the marginal new
content.

### V4: Is the marginal content non-trivial?

**Answer:** Yes:
- Lemmas BB1 and BB1' are explicit framework-internal statements not
  in existing notes.
- The framework-integration mapping (RP ⟶ Wilson loop bootstrap) is
  a non-trivial structural insight.
- The named obstruction's three tightening routes (Migdal-Makeenko,
  industrial SDP, framework-specific positivity) provide explicit
  next-cycle direction.

### V5: Is this a one-step variant of an already-landed cycle?

**Answer:** NO. Block 01 of this campaign is structurally distinct from:
- Prior campaign block 03 / PR [#410](https://github.com/jonathonreilly/cl3-lattice-framework/pull/410) (mean-field saddle approach)
- Prior bridge-support stack work (Perron solves, source-sector
  factorization) which uses analytic upper-bound construction
- The framework's existing RP runner (verifies RP via reconstruction,
  not bootstrap)

The bootstrap-via-RP approach is a genuinely different attack route.

## Value Gate disposition: PASS

All V1-V5 answers are positive. PR is allowed.

## Self-review findings

| # | Severity | Finding | Disposition |
|---|---|---|---|
| F1 | low | The block 01 result (~0.35-0.48 from strong-coupling LO + mixed-cumulant) is far below MC 0.5934. The strong-coupling expansion is not convergent at β=6. | Recorded explicitly in §5 of theorem note. The bound is honestly weak because of strong-coupling non-convergence; the framework-integration value is in establishing the bootstrap mapping, not in the numerical bound itself. |
| F2 | medium | A11 (RP theorem) is `support` tier, audit-pending. Block 01 inherits this conditional status. | Recorded in §10 honest status. Audit ratification of A11 is a prerequisite for retaining BB1 / BB1'. |
| F3 | medium | BB2 (lattice Migdal-Makeenko as standard QFT) is admitted, not derived on framework surface. | Recorded in Section 1 (Setup) and named-obstruction §6. Future cycle: derive Migdal-Makeenko on framework's V-invariant minimal block. |
| F4 | low | The 2x2 Gram matrix PSD reduces to BB1' which is just RP. The "bootstrap" content is not yet applied at higher truncation. | Acceptable for block 01 (smallest non-trivial). Block 02 attempts 3x3 + framework-specific positivity. |
| F5 | low | The mixed-cumulant correction `β^5/472392 ≈ 0.0165` is small at β=6; the dominant uncertainty is in `P_1plaq(β)` which we use only at LO. | Recorded explicitly. Higher-order strong-coupling expansion (SU(3) characters) would give P_1plaq ≈ 0.43-0.48, still below MC. The strong-coupling expansion is fundamentally not convergent at β=6. |

### Hostile-review-style stress test

**Q1.** Does the framework's RP theorem (A11) actually apply to Wilson-loop subalgebra, or only to the broader algebra `A_+` of all polynomials in fields?

**A1.** A11 (R2) explicitly states "the algebra A_+ of polynomial observables localised in Λ_+." Wilson loops (products of link variables around closed loops) are polynomials in field operators — specifically in the link matrices U_l. So Wilson loops are a subalgebra of A_+, and the PSD restriction holds. ✓

**Q2.** Is the "mixed-cumulant audit" relation really exact, or is it itself perturbative?

**A2.** Looking at PLAQUETTE_SELF_CONSISTENCY_NOTE: the relation `P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O(beta^6)` is described as the "first nonlinear coefficient of the full-vacuum reduction law" — exact AT THIS order. Higher orders (β^6 and beyond) are not included; they may shift the result. So the relation is exact-up-to-O(β^6), not exact. The runner output honestly reports this.

**Q3.** Why is the bound ~0.35-0.48 so far below MC 0.5934? Is the framework-integration honestly capturing the bootstrap power?

**A3.** The published industrial bootstrap (Kazakov-Zheng 2022) achieves bracket 0.59-0.61 at L_max=16 with ~100k loop equations. Our small-truncation (L_max=2) framework-integration cannot match this precision. The strong-coupling estimate (~0.35-0.48) is the LO + first-nonlocal correction, NOT the bootstrap bracket itself — the 2x2 PSD constraint by itself only gives Var(P) ≥ 0 (no bound on ⟨P⟩). The runner honestly reports both numbers separately and identifies the gap as the bootstrap-tightening obstruction.

### Self-review disposition: PASS

The framework-integration is honest support theorem; the analytical estimate is honestly identified as weak / non-convergent at β=6; the named obstruction is sharply stated.

## Cluster-cap / volume-cap check

- Volume cap: 1 of 5 PRs (this campaign).
- Cluster cap (`gauge_vacuum_plaquette_*` family): 1 of 2 used.
- Corollary churn: first cycle of this campaign; not applicable yet.

PASS all caps.

## Closure and next action

Block 01 is closure-ready as framework-integration support theorem +
named-obstruction stretch. Next action: write CLAIM_STATUS_CERTIFICATE
already done, commit, push, open PR.

After block 01 PR opens, pivot to block 02 (3x3 + framework-specific
positivity refinement).
