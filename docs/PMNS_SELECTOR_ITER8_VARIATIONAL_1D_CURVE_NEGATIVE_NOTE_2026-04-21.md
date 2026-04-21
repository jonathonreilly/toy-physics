# PMNS Selector Iter 8: Variational on 1-D Curve — Negative

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** Honest negative. No natural retained functional tested has
an extremum on the 1-D curve `{δ·q_+ = 2/3, det(H) = E2}` coinciding
with `m_*`. Variational-on-the-reduced-curve class is ruled out as a
source for the third retained cut.
**Runner:** `scripts/frontier_pmns_selector_iter8_variational_on_1D_curve.py` —
0 PASS, 2 FAIL.

---

## Attack

After iter 5-6 established two retained identities (`δ·q_+ = 2/3`,
`det(H) = E2`) reducing the 3-D chart to a 1-D curve, and iter 7
confirmed no third simple-value scalar identity at the closure point,
iter 8 tested a different class: variational principles. Question —
does any natural retained functional `F(m)` have its extremum
`dF/dm = 0` at the physical `m_*`?

## Functionals tested

14 natural candidate functionals, parameterized by m along the 1-D
curve:

| # | Functional | m of extremum | \|Δm\| | dF/dm at m_* |
|---|---|---:|---:|---:|
| F1 | Tr(H²)/Tr(H)² | N/A | ∞ | -34.68 |
| F2 | λ_max/\|λ_min\| | 0.756 | 0.099 | +0.30 |
| F3 | Jarlskog | N/A | ∞ | -0.071 |
| **F4** | **sin(δ_CP)** | **0.713** | **0.056** | **-0.53** |
| F5 | Koide Q on λ | N/A | ∞ | +0.083 |
| F6 | \|K_12\| | 0.526 | 0.131 | +0.88 |
| F7 | arg(K_12) | N/A | ∞ | +3.45 |
| F8 | s13² | N/A | ∞ | +0.052 |
| F9 | s12² | N/A | ∞ | +0.50 |
| F10 | s23² | N/A | ∞ | -0.22 |
| F11 | Tr(H³)/Tr(H²)^{3/2} | 0.781 | 0.124 | +0.17 |
| F12 | (λ_max+λ_min)/λ_mid | N/A | ∞ | -4.94 |
| F13 | Re(K_12) | N/A | ∞ | +1.00 |
| F14 | Im(K_12) | N/A | ∞ | -0.78 |

Best candidate (F4 sin(δ_CP)) has its extremum 0.056 away from m_*,
far from the 1e-3 threshold. All other functionals either have no
extremum on the tested interval OR extrema at distances > 0.1 from
m_*.

## What this rules out

The retained selector's third cut is NOT a variational extremum of
any of the natural candidate functionals tested. This rules out the
broad class of "quadratic/cubic spectral invariants of H" and the
"Z_3-doublet-phase variational" sub-classes.

## What remains

**Updated attack backlog exhaustion status after iter 8:**

| Attack class | Status |
|---|---|
| A1 direct AM-GM doublet | Ruled out iter 1 |
| A2 W[J] scalar Casimir | Ruled out iter 2 |
| A3 Koide on eigenvalues | Implicitly tested iter 4, ruled out |
| A4 Brannen-phase gate | Weak hint, ruled out exact iter 3 |
| **A5** A-BCC axiomatic derivation | **Not yet attempted** ← prime candidate |
| A6 operator commutation | Ruled out iter 4 |
| **A7** Wilson-line cyclic bundle | **Not yet attempted** |
| A8 A-BCC × I2/P cross-sector | Overlaps A5 |
| **A9** chamber-boundary variational | **Not yet attempted** |
| **A10** symplectic | **Not yet attempted** |
| Iter-8 variational on curve | Ruled out this iter |

Four untried classes remain: A5, A7, A9, A10.

## The standing support package (iters 5-6)

Even without the third retained cut, iters 5-6 established a
**2-retained + 1-observational** closure that is:

- Framework-native on the retained-identity part (two specific,
  testable, retained equations).
- Observationally admissible (all three PMNS angles in NuFit 3σ NO,
  two in 1σ).
- Falsifiable (predicts `s23² = 0.545`, `s12² = 0.303` given
  `s13² = 0.0218`).

Whether this counts as "gate closure" depends on the framework's
strict interpretation of "retained-forced". A full 3-retained closure
would eliminate the s13² observational input; iters 9+ pursue this
via the untried attack classes.

## Iter 9 plan

Primary: **A5 — A-BCC axiomatic derivation**. This is the prime
candidate because:

1. It's what the user's original framing named explicitly: "DM
   A-BCC / PMNS angle-triple gate".
2. `A-BCC` is currently observationally grounded (via T2K CP-phase
   exclusion of the `C_neg` basin), not derived from `Cl(3)`.
3. If A-BCC is axiom-derived, it may come with additional structure
   that constrains the point further beyond the signature choice —
   possibly pinning s13² or a related scalar.

Concrete A5 plan:
- State the A-BCC condition as `signature(H_base) = signature(H_base + J_*)
  = (2, 0, 1)` in briefing conv (1 negative, 2 positive in numpy conv).
- Attempt derivation: show that `Cl(3)` on `Z³` + retained `W[J]`
  observable principle forces the sign of `det(H_base + J)` at the
  physical chamber point.
- If the derivation produces an identity stronger than just the sign
  (e.g., a specific value of `det` or a specific constraint on `K`),
  that's the third cut candidate.
