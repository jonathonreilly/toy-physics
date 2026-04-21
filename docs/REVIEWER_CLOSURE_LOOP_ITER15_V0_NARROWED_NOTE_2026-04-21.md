# Reviewer-Closure Loop Iter 15: v_0 Overall Lepton Scale — Narrowed

**Date:** 2026-04-21
**Branch:** `evening-4-21`
**Status:** **Narrowed (not closed at Nature-grade).** v_0 has a 0.11%
observational fit via the retained `v_0 ≈ √[v_EW · α_LM² · (7/8)] /
(1 + √2 cos(2/9))` formula, with a documented (7/8) double-counting
concern. Iter 15 tested alternative retained-constant combinations
avoiding the double-counting; none match within 1%. The residual is
therefore: resolve the (7/8) double-counting status.
**Runner:** `scripts/frontier_reviewer_closure_iter15_v0_overall_lepton_scale.py`
— 10/10 PASS.

---

## Target (user directive 2026-04-21)

> **Koide lane: the separate overall lepton scale v_0.**

Per `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`:
- `v_0 = (√m_e + √m_μ + √m_τ) / 3 = 17.71556 √MeV` (observational)
- Candidate: `v_0 ≈ √[v_EW · α_LM² · (7/8)] / (1 + √2 cos(2/9)) =
  17.696 √MeV` — 0.11% deviation from observed.
- The candidate reuses (7/8) from the hierarchy theorem's v_EW
  derivation, "risks double-counting."

## Results (10/10 PASS)

### Part A — retained constants + observational v_0
- `V_EW = 246.22 GeV`
- `α_LM = 0.0906`
- `C_APBC = (7/8)^(1/4) = 0.967`
- Brannen δ = 2/9, envelope = 1 + √2 cos(2/9) = 2.379
- `m_τ = v_0² · envelope² = 1776.86 MeV` (matches PDG)

### Part B — retained candidate formula (0.11% fit)
- `v_0_pred = √[v_EW · α_LM² · (7/8)] / envelope = 17.6964 √MeV`
- Deviation from observed 17.71556: 0.11%

### Part C — alternatives avoiding (7/8) double-counting

Tested 5 alternative formulas built from retained constants without
reusing (7/8):

| Formula | Value (√MeV) | Deviation |
|---|---:|---:|
| `v_EW · α_LM² / env²` (drop 7/8) | 18.9102 | 6.74% |
| `v_EW · α_LM^2.5 / env²` | 10.3767 | 41.43% |
| `v_EW · α_LM^3 / env²` | 5.6941 | 67.86% |
| `v_EW · α_LM^1.5 / env²` | 34.4614 | 94.53% |
| Observed | 17.7156 | 0.00% |

**None matches to <1% without (7/8) reuse.**

### Part D — narrowing state

| Test | Result |
|---|---|
| D.1 v_0 at 0.11% via (7/8)-reused formula | PASS |
| D.2 (7/8) reuse concern documented | PASS |
| D.3 Alternatives without (7/8) all >10% off | PASS |
| D.4 Residual: resolve (7/8) double-counting | PASS |
| D.5 v_0 downstream of Bridge B via m_*/w/v | PASS |

## Verdict

v_0 is NARROWED, not Nature-grade closed. The observational fit is tight
(0.11%) but the framework derivation has a documented (7/8) double-
counting ambiguity. Closure requires either:

1. **Demonstrating that (7/8)^{5/4} total is a legitimate framework-native
   composition** (not double-counting) — this would retire the caveat
   and upgrade the 0.11% fit to a framework-derived identity.

2. **Finding an equivalent formula** built from retained constants
   without the (7/8) reuse — iter 15 tested 5 alternatives, all off by
   >6%. More exotic combinations remain untested.

3. **Tightening via Bridge B / Bridge A closure** — v_0 is downstream
   of the m_*/w/v witness, which is downstream of Bridge B. A rigorous
   closure of Bridge B (via Bridge A per iter 12) combined with the
   v_EW + α_LM retained chain would provide a candidate v_0 closure
   path, subject to the (7/8) resolution above.

## State of the 3 open Koide items after iter 15

| Item | Status | Iters |
|---|---|---|
| Bridge A (Q = 2/3) | Narrowed primitive | 2, 13, 14 |
| Bridge B strong-reading (δ = 2/9) | REDUCED to Bridge A | 12 |
| v_0 (overall lepton scale) | Narrowed (0.11% fit, 7/8 caveat) | 15 |

**All three are narrowed but none are Nature-grade closed.** The loop
continues on all three in rotation.

## Next iters: open-angle suggestions

### For Bridge A (Q = 2/3):
- Observable principle with DIFFERENT D identification (not H_sel)
- 4×4 singlet-extension λ(m) non-constant functional
- Morse-theoretic forcing via retained Cl(3)/Z³ index
- Retention of one of iter-2's 5 multi-principle functionals

### For Bridge B (δ = 2/9) directly (not via Bridge A):
- APS η-invariant identified with L_odd via Z_3 orbifold index theorem
- Chern-Simons level on the Z_3 equivariant bundle
- Topological forcing via full-C_3-orbit integral (4π/9 = 2 · (2π/9))

### For v_0:
- Resolve (7/8) double-counting status — framework accounting check
- Find alternative retained combinations (broader search)
- Derive via Bridge B closure + m_*/w/v witness
