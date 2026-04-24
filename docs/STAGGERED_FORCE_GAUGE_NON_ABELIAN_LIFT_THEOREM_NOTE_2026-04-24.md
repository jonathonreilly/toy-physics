# N+4 Non-Abelian Lift of the Force-vs-Gauge Separation Theorem

**Date:** 2026-04-24
**Status:** theorem-grade completion of the N+1 → N+4 arc. Lifts the
force-vs-gauge separation from scalar `phi` to SU(N) gauge
connection `U: E → SU(N)`.
**Runner:** `scripts/frontier_staggered_force_gauge_non_abelian_lift_theorem.py`
**Result:** `13/13 PASS`, wallclock `0.03 s`.
**Predecessor notes:**
- [`STAGGERED_FORCE_GAUGE_SEPARATION_THEOREM_NOTE_2026-04-24.md`](STAGGERED_FORCE_GAUGE_SEPARATION_THEOREM_NOTE_2026-04-24.md) — loop 15 single-cycle scalar theorem.
- [`STAGGERED_FORCE_GAUGE_MULTI_CYCLE_HOMOLOGY_THEOREM_NOTE_2026-04-24.md`](STAGGERED_FORCE_GAUGE_MULTI_CYCLE_HOMOLOGY_THEOREM_NOTE_2026-04-24.md) — N+2 multi-cycle homology extension.
- [`GRAPH_NATIVE_OBSERVABLE_FORM_CLASSIFICATION_AUDIT_NOTE_2026-04-24.md`](GRAPH_NATIVE_OBSERVABLE_FORM_CLASSIFICATION_AUDIT_NOTE_2026-04-24.md) — N+3 package-wide observable audit.

## 1. Question

The loop-15 scalar theorem (T.1–T.5) and the N+2 multi-cycle
homology extension (M.1–M.5) are built on the exterior calculus
identity `d ∘ d = 0` for 0-forms, which makes the cycle integral
`sum_{e ∈ C} (phi_j - phi_i)` identically zero. This is **gauge-
trivial**: the scalar case's "gauge row" carries nontrivial per-
edge span but zero cycle holonomy.

N+4 asks: does the separation theorem extend to the non-abelian
setting, where cycle integrals become Wilson loops — gauge-
invariant, reparameterization-invariant, **nontrivial** objects?

## 2. Non-abelian setup

- Graph `G = (V, E)`.
- SU(N) link variables `{U_e : e ∈ E}`, one matrix per directed edge.
- Convention: `U_e : fiber_i → fiber_j` for `e = (i → j)`, so
  `U_e @ v_i = v_j`.
- Wilson loop on cycle `C = (v_0, v_1, ..., v_k = v_0)`:
  `W(C) = Tr(U_{v_{k-1} → v_k} @ ... @ U_{v_1 → v_2} @ U_{v_0 → v_1})`
  (right-to-left matrix product in traversal order).
- Gauge transformation: `g : V → SU(N)`. Links transform as
  `U_e → g(j) U_e g(i)^{-1}`.

## 3. Theorem

### L.1 Gauge invariance

Under the local transformation `U_e → g(j) U_e g(i)^{-1}`, the
Wilson loop is invariant: `W(C) → W(C)`. This follows from the
telescoping of g factors around a CLOSED cycle:

```
W = Tr(U_{v_{k-1} → v_0} @ U_{v_{k-2} → v_{k-1}} @ ... @ U_{v_0 → v_1})

W' = Tr( g(v_0) U_{v_{k-1} → v_0} g(v_{k-1})^{-1}
       @ g(v_{k-1}) U_{v_{k-2} → v_{k-1}} g(v_{k-2})^{-1}
       @ ...
       @ g(v_1) U_{v_0 → v_1} g(v_0)^{-1} )

  = Tr( g(v_0) [prod] g(v_0)^{-1} )
  = Tr(prod)
  = W
```

Verified numerically on a random SU(2) 4-cycle with random gauge
transformation: `|W_after - W_before| = 0` to machine precision.

### L.2 Reparameterization invariance

Starting the cycle traversal at a different vertex gives the same
trace, by the cyclic-trace identity `Tr(ABC) = Tr(BCA)`. Verified on
all 4 starting vertices of the 4-cycle.

**Consequence**: the "edge selection" ambiguity of the scalar case
(loop-15 T.5: source-proximal non-bridge rule needed to detect
per-edge span) **DISSOLVES** in the non-abelian case. `W(C)` is
a single gauge-invariant number per cycle, independent of which
edge we label as the starting point.

### L.3 Reversal gives complex conjugate

Traversing the cycle backwards replaces each `U_e` by `U_e^{-1} = U_e^†`
(SU(N) property). The resulting Wilson loop is `W(C^{-1}) = W(C)^*`.

For the SU(2) fundamental representation, traces are real: `Im(W) = 0`.
Verified: `Im(W_from_A) = 0` to machine precision.

### L.4 Trivial connection gives W = N

If `U_e = I` for all `e`, then `W(C) = Tr(I) = N`. Verified for
SU(2): `W = 2`.

### L.5 Pure-gauge connection gives W = N

If `U_e = g(j) g(i)^{-1}` for some `g : V → SU(N)`, the product
around a cycle telescopes to the identity:
```
W = Tr(g(v_0) g(v_{k-1})^{-1} · g(v_{k-1}) g(v_{k-2})^{-1} · ... · g(v_1) g(v_0)^{-1})
  = Tr(g(v_0) I g(v_0)^{-1})
  = Tr(I) = N
```
Verified numerically on random `g : V → SU(2)`. This is the
non-abelian analog of the scalar-case statement "cycle integral
of `d phi` is zero".

### L.6 Curvature gives nontrivial W ≠ N

When link variables don't commute around a cycle (genuine
non-abelian curvature), `W(C) ≠ N`. Tested with alternating
X- and Y-axis rotations at angle `π/3`: `W = -1.5`, clearly
different from the trivial value `N = 2`. The deviation
`|W - N|` measures the cycle's non-abelian flux.

### L.7 DAGs have no Wilson loop

Same structural forcing as the scalar case (T.3 / M.3): DAGs have
no cycles, so the cycle-holonomy observable has an empty domain.
The "N/A" designation is preserved.

### L.8 Abelian reduction to scalar case

In the U(1) limit, `U_e = e^{i a_e}` where `a_e` is the link phase.
Wilson loop is `W = e^{i · sum_e a_e}`.

- **Pure gauge `a_e = phi_j - phi_i`**: `sum_e a_e = 0` (discrete
  Stokes), so `W = 1`. This is the scalar-case loop-15 T.2
  statement in U(1) Wilson-loop form.
- **Nontrivial flux `a_e` not exact**: `sum_e a_e ≠ 0`, so `W ≠ 1`.
  Verified numerically with `W = -0.227 + 0.974i` at flux `1.8`.

### L.9 Edge-selection artifact dissolves

By L.2 (cyclic trace invariance), the Wilson loop does not
depend on which edge of the cycle is labeled as the "start".
There is no non-abelian analog of the loop-15 T.5 "source-
proximal non-bridge edge" rule: cycle-representative invariance
is built in by the trace.

### L.10 Honest open boundary

The theorem covers the **structural** character of Wilson loops.
The **dynamics** of `U_e` (Yang-Mills action, running coupling,
string tension, confinement) are separate physical questions and
are not proved here. Tested for SU(2); SU(N) works identically by
construction.

## 4. Verdicts

All 13 gates pass. See the runner output for the per-gate table.

## 5. Completion of the N+1 → N+4 arc

The force-vs-gauge separation framework is now complete across
four successive extensions:

| Step | Extension | Key result |
|---|---|---|
| Loop 15 | single-cycle scalar | force = 0-form, gauge = 1-form; cycle integral = 0 (Stokes) |
| N+2 | multi-cycle homology | `b_1` basis, per-cycle source-proximal rule |
| N+3 | package audit | 12 retained observables classified, no ambiguity |
| **N+4** | **non-abelian** | **Wilson loops nontrivial; edge-selection dissolves** |

The staggered backreaction lane is now fully characterized:

- Force rows = local 0-forms on any graph (loop 15).
- Scalar gauge/current rows = 1-forms with source-proximal rule on
  cycle-bearing graphs; zero on DAGs (loop 15 + N+2).
- All retained graph-native observables map cleanly into this
  classification (N+3).
- The framework extends to non-abelian gauge (N+4), where cycle
  holonomy is nontrivial and the edge-selection ambiguity
  disappears.

## 6. What this does NOT close

- The N+4 theorem is structural. The **dynamics** of non-abelian
  gauge (Yang-Mills action, running coupling, string tension,
  confinement) are separate and not addressed here.
- Tested explicitly for SU(2); SU(N) works identically by the same
  structural argument.
- Does not by itself close any of the retained package lanes;
  the theorem is a **framework unification**, not a new
  manuscript-core claim.

## 7. Falsifier

- Wilson loop failing gauge invariance under local transformation
  (contradicts L.1).
- Starting at different vertex giving different trace (contradicts
  L.2 cyclic trace).
- Pure-gauge connection giving `W ≠ N` (contradicts L.5
  telescoping).
- Non-commuting links giving `W = N` (would say there's no
  non-abelian curvature, contradicting L.6).

None observed; 13/13 PASS.

## 8. Next concrete step

The N+1 → N+4 arc is complete at the framework level. Natural
next steps:

- Extend the retained manuscript claim surfaces (CLAIMS_TABLE,
  DERIVATION_VALIDATION_MAP) to reference the unified
  classification framework, particularly for the 1-form /
  Wilson-loop gauge observables in the retained SU(2) and
  graph-first SU(3) packages.
- **Formal backreaction card template**: require 0-form / 1-form
  / 2-form labels for each observable row in any new retained
  package card, with explicit edge/face rules where applicable.
- Apply the framework to the Koide Q + K_TL Lagrange-multiplier
  work (loop 1): both are examples of "identify physical vs. gauge
  components of a multi-scalar observable"; a unified formulation
  would tie the Q-lane and staggered lane under the same structural
  principle.

## 9. Provenance

- Runner: `scripts/frontier_staggered_force_gauge_non_abelian_lift_theorem.py`
- Dependencies: `numpy`, `math` (no `sympy` needed; tests use
  numerical SU(2) matrices).
- Result: `13/13 PASS`, wallclock `0.03 s`.
- Reproducibility: deterministic with `np.random.default_rng(42)`.
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1 vs
  pinned 3.13.5, 2.4.4. Linear algebra on 2x2 complex matrices;
  version drift is not a confounder.
