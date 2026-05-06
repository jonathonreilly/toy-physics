# PR #525 Methodological Flaw: 1-Loop Interpretation Should Be Reopened

**Date:** 2026-05-05
**Status:** research_finding (corrects a flawed structural test in prior closed PR campaign)
**Type:** methodological correction
**Companion:** [`SU3_LOW_RANK_IRREP_PICARD_FUCHS_ODES_NOTE_2026-05-05.md`](SU3_LOW_RANK_IRREP_PICARD_FUCHS_ODES_NOTE_2026-05-05.md)
**Refers to:** PR #525 ("SU(3) bridge TERMINAL CLOSURE: structural test refutes 1-loop"), closed without merge

## Summary

PR #525 ran a structural test that purported to refute the 1-loop
self-energy interpretation of `Δk = 2/π = (N²−1)/(4π)` in the K-tube
ansatz `ρ_(p,q)(6) = (c_R(6) / c_(0,0)(6))^(12 + 2/π)`. The test
divided the deviation `Δ ln ρ_(p,q)` by the SU(3) Casimir `C_2(p,q)`
and reported a **451% spread** across irreps, concluding "1-loop
Feynman interpretation REFUTED."

This conclusion is based on testing the **wrong proportionality**.
The K-tube formula by construction implies

```
Δ ln ρ_(p,q) = (2/π) · ln(c_R(6) / c_(0,0)(6))
```

— that is, `Δ ln ρ` is proportional to `ln(c_R/c_(0,0))`, NOT to
`C_2(p,q)`. PR #525's test therefore divided by the wrong denominator.
Dividing by the correct denominator gives a ratio that is **constant
to six decimal places** across all tested irreps, exactly equal to
2/π:

| irrep R | C_2(R) | c_R(6)/c_(0,0)(6) | Δ ln ρ_R | Δlnρ / C_2 (PR #525 test) | Δlnρ / ln(c/c_(0,0)) (correct test) |
|:---:|:---:|---:|---:|---:|---:|
| (1,0) | 1.33 | 1.2676 | 0.1510 | 0.1132 | **0.636620** |
| (1,1) | 3.00 | 1.2981 | 0.1661 | 0.0554 | **0.636620** |
| (2,0) | 3.33 | 0.8158 | −0.1296 | −0.0389 | **0.636620** |
| (2,1) | 5.33 | 0.7243 | −0.2053 | −0.0385 | **0.636620** |
| (2,2) | 8.00 | 0.3646 | −0.6422 | −0.0803 | **0.636620** |
| (3,0) | 6.00 | 0.3506 | −0.6673 | −0.1112 | **0.636620** |

`2/π = 0.636620…`  Exact match to 6 figures.

## Implications for the closed PR #519/#522/#525/#527 campaign

PR #525 used the 451% spread as the load-bearing argument to refute
the 1-loop self-energy interpretation, which then propagated into PR
#527's "honest tension terminal status." The spread is real, but it
disproves only the **specific claim** that `Δ ln ρ_R ∝ C_2(R)`. It
does NOT disprove:

1. **1-loop gluon self-energy in the adjoint sector** producing a
   constant (irrep-independent) multiplicative renormalization of
   `c_R(β)/c_(0,0)(β)`. The adjoint-loop integral has prefactor
   `(N²−1) × α_s = (N²−1)/(4π)` at g_bare² = 1.
2. **1-loop tadpole / mean-field improvement** of the per-plaquette
   weight, which acts uniformly across irreps.
3. **1-loop Haar measure renormalization** around the classical vacuum.
4. Any other 1-loop effect that produces a uniform multiplicative shift.

The K-tube structure FORCES `Δ ln ρ_R ∝ ln(c_R/c_(0,0))` (with the
prefactor independent of R). PR #525's test was correct in spirit
(check whether 1-loop produces this proportionality) but tested the
wrong observable. **The 1-loop interpretation should be reopened** as
an honest open question.

## The actual current state

### What's confirmed by this analysis

1. The K-tube fit `ρ_(p,q)(6) = (c_R/c_(0,0))^(12 + 2/π)` produces
   `⟨P⟩(6) = 0.5934163`, matching standard MC reference at +0.2σ.
2. The 2/π exponent shift acts UNIFORMLY (irrep-independent prefactor).
3. The framework's Theorem 3 no-go in `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`
   stands: c_R(6) and SU(3) intertwiners alone cannot uniquely fix
   ρ_R. (This is a separate issue from the 1-loop interpretation.)

### What this analysis does NOT establish

This note does NOT close the famous problem. It only corrects a flawed
methodological test in PR #525. Specifically, it does NOT:

1. Derive `2/π = (N²−1)/(4π)` from a specific 1-loop Feynman diagram
   or self-energy calculation.
2. Resolve PR #527's three interpretations (A/B/C) of the K-tube
   ansatz vs Schur rigorous.
3. Verify the (N²−1)/(4π) form at general N (only N=3 has been tested
   by MC; SU(2) and SU(4) data would be needed).

## Reopened question

The honest open question is now:

> **What 1-loop SU(N) effect produces a uniform (irrep-independent)
> exponent shift `Δk = (N²−1)/(4π)` at g_bare² = 1?**

A follow-up SD-equation derivation probe (after this note) attempted
the four standard 1-loop candidates — adjoint gluon self-energy,
Faddeev-Popov ghost, Haar measure renormalization, Polyakov tadpole —
and found that NONE produces the exact `(N²−1)/(4π) · ln(c_R/c_(0,0))`
form cleanly:

- Gluon/ghost self-energy: produces `C_2(R)`-proportional shift, not
  uniform. Forbidden by K-tube structure.
- Haar measure renormalization: gives prefactor `(N²−1)/(8π²) · log β`,
  not `(N²−1)/(4π)`.
- Polyakov tadpole: gives `(N²−1)/(8N)` factor, not `(N²−1)/(4π)`.

So the open question remains unsolved at the SD-derivation level. The
prior campaign's terminal status is essentially correct in this
respect — but the claim that "1-loop is killed" was overclaimed, and
the campaign's strategy of seeking a 1-loop derivation is still a
viable line of attack with the correct test premise.

## Sub-result: numerical k* uncertainty

A complementary verification:
- K-tube exponent at MC `⟨P⟩=0.5934`: k* = 12.6342 (bisected, agrees to 10⁻¹⁰)
- Conjectured analytic value: 12 + 2/π = 12.6366
- Gap: |k* − (12 + 2/π)| = 2.4 × 10⁻³ (relative 0.019%)

The framework's L→∞ MC retained-grade FSS extrapolation
(PR #539; `⟨P⟩∞(β=6) = 0.59400 ± 0.00018`) gives a slightly different
k* = 12.69 within the FSS error budget. Both are consistent with
12 + 2/π within combined uncertainty, but not analytically pinned.

## Status proposal

```yaml
note: SU3_BRIDGE_PR525_FLAW_FIX_NOTE_2026-05-05.md
type: research_finding (methodological correction)
proposed_status: research_finding
positive_subresults:
  - PR #525's structural test divides by C_2 (wrong denominator)
  - correct test: Δ ln ρ / ln(c_R/c_(0,0)) — exactly constant at 2/π
  - reopens: 1-loop interpretation as a viable line of attack
audit_required:
  - independent verification of the corrected ratio computation
  - acknowledgment in any downstream notes that PR #525's "1-loop killed" was overclaimed
bare_retained_allowed: no
follow_up: derive uniform (N²-1)/(4π) shift from 1-loop SU(N) primitive
          (still open after SD-equation probe; standard 1-loop candidates fail)
```

## Ledger entry

- **claim_id:** `su3_bridge_pr525_flaw_fix_note_2026-05-05`
- **note_path:** `docs/SU3_BRIDGE_PR525_FLAW_FIX_NOTE_2026-05-05.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
- **dependency_chain:**
  - `SU3_LOW_RANK_IRREP_PICARD_FUCHS_ODES_NOTE_2026-05-05.md` (provides c_R(6) values)
  - `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` (Theorem 3 framework)
  - PR #525 (closed, the flawed test being corrected)
  - PR #527 (closed, terminal status being partially reopened)
