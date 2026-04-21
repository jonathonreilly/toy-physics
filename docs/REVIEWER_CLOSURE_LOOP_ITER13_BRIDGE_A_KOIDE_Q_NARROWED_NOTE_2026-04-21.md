# Reviewer-Closure Loop Iter 13: Bridge A (Q = 2/3) Physical/Source-Law Mechanism — NARROWED

**Date:** 2026-04-21
**Branch:** `evening-4-21`
**Status:** **Narrowed, not closed at Nature-grade.** Iter 13 attempted three
fresh angles — geometric reformulation, direct Frobenius-on-selected-line
test, and retained-constant search for λ_* — all negative or non-deriving.
The residual is sharpest-stated: one of the 5 multi-principle functionals
identified by iter 2 must be elevated to retained-source-law status, or a
4×4 singlet-extension λ(m) non-constant route must be characterized.
**Runner:** `scripts/frontier_reviewer_closure_iter13_bridge_a_koide_q_physical_mechanism.py`
— 15/15 PASS.

---

## Target (user directive 2026-04-21)

> **Koide physical/source-law bridge for Q = 2/3.** Target: derive why the
> physical charged-lepton packet must extremize the block-total Frobenius
> functional, or derive an equivalent accepted source law forcing the same
> point. Why: the AM-GM/Frobenius math is already clean; what remains is
> the physical identification.

## Iter 13 attacks

### Part A — geometric reformulation

- Q = 2/3 ⟺ |u_parallel|² = |u_perp|² in √m space
- Equivalently: √m vector at 45° to the (1,1,1) diagonal
- Equivalently: equal singlet/doublet amplitude-squared projection
- This is a clean geometric picture but NOT a derivation — any closure of
  Bridge A simultaneously derives this geometric condition.

### Part B — block-total Frobenius on selected line

Testing the direct claim: "physical packet extremizes F(m) = Tr(H_sel(m)²)
on the selected-line parameter m."

**Symbolic result:** F(m) is quadratic in m. Its extremum m_F is a specific
closed-form expression in retained constants.

**Numerical:** m_F ≠ Koide m_* = -1.16044 (substantial difference).

**Conclusion:** the block-total Frobenius extremum on the selected-line
m parameter is NOT at the Koide point. So this particular source law is
RULED OUT.

### Part C — λ_* ≈ 0.5456 retained-constant search

Per retained `KOIDE_C3_SINGLET_EXTENSION_REDUCTION_THEOREM_NOTE_2026-04-20`,
the 4×4 singlet-extension with fixed coupling gives one scalar λ_* such that
the Koide point is stationary of V_λ(m). Numerical value: λ_* = 0.5456253117.

Tested 5 natural combinations of retained constants (γ, E_1, E_2, SELECTOR,
Q_Koide, δ_B):

| Candidate | Value | Dev from λ_* |
|---|---|---|
| `(2/3)·SELECTOR = 2√6/9` | 0.5443 | 1.3e-3 |
| `γ + Q/6 = 1/2 + 1/9` | 0.6111 | 6.5e-2 |
| `γ · (1 + 2/9) = (1/2)·(11/9)` | 0.6111 | 6.5e-2 |
| `(2γ + δ_B)/2 = (1 + 2/9)/2` | 0.6111 | 6.5e-2 |
| `γ · (1 + Q/3)` | 0.6111 | 6.5e-2 |

**Conclusion:** no clean retained-constant match for λ_*. Either:
- λ_* has no closed form in the current retained Atlas constants
- Or the retention is NOT via the fixed-coupling 4×4 Schur route

### Part D — honest narrowing

After iter 13, the narrowest honest statement of Bridge A is:

> **Residual open item:** elevate ONE of the 5 multi-principle information /
> variational functionals identified in iter 2 (all critical at p_+ = 1/2 =
> Koide) to **retained-source-law status** in the Atlas. Alternatively:
> derive the 4×4 singlet-extension λ(m) non-constant functional from Cl(3)/Z³
> structure.

## What iter 13 clarified vs what remains

### Clarified

1. **The 45° cone / equal-isotype-projection reformulation is exact.**
   Q = 2/3 is geometrically equivalent to "singlet = doublet amplitude
   squared projection." This is clean geometric content, not a derivation.

2. **Block-total Frobenius on the selected-line m parameter is ruled out**
   as the source law (its extremum is at a different m).

3. **λ_* = 0.5456 is not a simple retained-constant combination.** Either
   λ_* is transcendental in retained constants, or the 4×4 fixed-coupling
   route is not the correct one.

### Remaining

- The physical mechanism forcing the charged-lepton packet to the
  equal-isotype-projection point (Koide m_*) remains un-retained.
- 5 natural principles converge at Koide (iter 2) but none is currently
  a retained source law.
- 4×4 singlet-extension λ(m) non-constant route is the narrowest
  unexplored lane per the canonical review surface.

## Status of all Gate-1 Koide items after iter 13

| Item | Status | Iter |
|---|---|---|
| Bridge A (Q = 2/3 physical mechanism) | **Narrowed (primitive)** | 2, 13 |
| Bridge B observational (arg b = 2/9 at PDG) | 🎯 CLOSED | 3 |
| Bridge B strong-reading (framework derivation) | **🎯 REDUCED to Bridge A** | 12 |
| m_*/w/v selected-line witness | Downstream of Bridge A | — |
| v_0 overall scale | Outside-scope | — |

**All Gate-1 items now reduce to Bridge A alone. Closing Bridge A triggers
simultaneous closure of Bridge B strong-reading AND the m_*/w/v witness
via iter 12's L_odd construction.**

## Loop discipline / next steps

Iter 13 is a NARROWING result, not Nature-grade closure. Per /loop
discipline, the attack continues. The narrowest honest residuals:

1. **Examine the 5 iter-2 multi-principle functionals for retained-Atlas
   status.** If ANY is currently in the retained Atlas as a structural
   theorem (without needing new axioms), its elevation to
   charged-lepton-sector source law would close Bridge A.

2. **Derive the 4×4 singlet-extension λ(m) non-constant functional.**
   The fixed-coupling λ_* doesn't match clean retained constants, but
   a non-constant λ(m) function derived from a framework source law
   might.

3. **Search the retained Atlas for any theorem that forces the
   equal-isotype-projection condition directly.** This is the geometric
   equivalent of Q = 2/3; any retained theorem forcing this geometry
   closes Bridge A.

## Loop status

- Iters 1-7 (earlier session): audit, Bridge A narrowed, Bridge B observational closed,
  N1 narrowed (3 attempts), Bridge B strong narrowed.
- Iters 8-11 (earlier session): all 4 Gate-2 items closed at Nature-grade.
- Iter 12: Bridge B strong-reading REDUCED to Bridge A.
- Iter 13: Bridge A narrowed further (ruling out Frobenius-on-selected-line
  + λ_* retained-constant match + identifying 5-principle residual).

The loop continues on Bridge A.
