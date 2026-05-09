# Higgs Taste-Singlet Projection on Hamming-Weight Staircase — Bounded Note

**Date:** 2026-05-09
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_higgs_taste_singlet_projection.py`](../scripts/frontier_higgs_taste_singlet_projection.py)

## Claim

Under the parent Higgs note's
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) eq.
`[4]` identification of the physical Higgs `σ` with the staggered
**taste-singlet** scalar (i.e. `σ` couples to the trace `<ψ̄ψ>` over
the 16 BZ corners on `Z³+t`, line 146 of the parent), the all-orders
Wilson-corrected `(m_H_W / v)²` formula from PR #773 eq. (2)
decomposes, on the Hamming-weight staircase of
[`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md),
into a weighted sum over the 5 Hamming-weight levels
`k ∈ {0, 1, 2, 3, 4}` with **derived** weights:

```text
( m_H_W / v )^2  =  Σ_{k=0}^{4}  w_k · c_k ( r, u_0 )                              (1)
```

where

```text
w_k       =  binomial(4, k) / 16                                                   (2)

c_k ( r, u_0 )  =  ( u_0^2  -  ( k - 2 )^2 r^2 )
                  /  ( 4 · ( ( k - 2 )^2 r^2  +  u_0^2 )^2 ).                      (3)
```

The weights `w_k` are the projection probabilities of the taste-singlet
state (uniform amplitude across all 16 BZ corners) onto the
Hamming-weight-`k` subspace; they sum to unity:

```text
Σ_{k=0}^{4}  w_k  =  ( 1 + 4 + 6 + 4 + 1 ) / 16  =  16 / 16  =  1.                 (4)
```

The per-corner Wilson-shifted curvature `c_k ( r, u_0 )` is the level-`k`
contribution to `|d²V_taste^W/dσ²| / 16` at the extremum `σ* = -4r`,
divided by the level multiplicity `binomial(4, k)` to yield the
per-corner value (so that `binomial(4, k) · c_k` is the level-`k` total).

Three structural consequences of (1)–(3) follow directly:

(i) **Central level `k = 2` is Wilson-decoupled.** Because `(k - 2)² = 0`
when `k = 2`, the Wilson shift drops out of (3) at this level:

```text
c_2 ( r, u_0 )  =  u_0^2 / ( 4 · u_0^4 )  =  1 / ( 4 u_0^2 ),
   r-independent for all r ∈ ℝ.                                                    (5)
```

(ii) **Reflection symmetry under `k → 4 - k`.** The substitution
`k → 4 - k` fixes `(k - 2)²` (since `(4 - k - 2)² = (2 - k)² = (k - 2)²`),
hence

```text
c_0 ( r, u_0 )  =  c_4 ( r, u_0 ),       c_1 ( r, u_0 )  =  c_3 ( r, u_0 ).        (6)
```

This is the same reflection that pins the Wilson extremum to
`m* = -4r` exactly (sister forward-reference
[`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)).

(iii) **Reduction at `r = 0`.** Each `c_k → 1 / (4 u_0^2)` independently,
so `(m_H_W / v)² → (Σ_k w_k) · (1 / (4 u_0^2)) = 1 / (4 u_0^2)`, matching
the parent eq. `[5]`.

The two structural inputs to the uniform-`N_taste = 16` weighting in
the parent — namely

  (A) `σ = taste-singlet` (couples uniformly to all 16 BZ corners), the
      standard staggered identification via `σ ↔ <ψ̄ψ>`;
  (B) the 16 corners of `Z³+t` decompose into Hamming-weight levels
      with multiplicities `binomial(4, k)` (PR #739 staircase);

are made explicit in (1)–(4). Input (A) is a structural identification
(not a free numerical parameter); input (B) is a counting fact about
`(Z/2)⁴`. The decomposition (1) is then forced.

This note **does not** change the all-orders closure value
`r_all_orders ≈ 0.26855` from PR #773 — it is a re-organization of the
same total curvature as a sum over Hamming-weight levels, not a new
computation. It does, however, factor the parent's "uniform-`N_taste = 16`
admission" into the two more-constrained inputs (A) and (B) above, and
makes the per-level structure explicit.

## Proof-Walk

| Step | Load-bearing input | Lattice-action input? |
|---|---|---|
| Parent eq. `[4]–[5]`: `(m_H/v)² = |d²V_taste/dm²| / N_taste`, with `N_taste = 16` and `σ` identified with the taste-singlet scalar `↔ <ψ̄ψ>` (parent line 146) | parent Higgs note structural identification | no |
| All-orders Wilson-corrected total curvature (PR #773 eq. (2)): `(m_H_W/v)² = (1/64) Σ_k binomial(4,k) (u_0² - (k-2)²r²) / ((k-2)²r² + u_0²)²` | sister forward-reference [`WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md) | no |
| Define `w_k = binomial(4, k)/16`: this is the level-`k` projection of the taste-singlet (= uniform on all 16 corners) state, by basic counting on `(Z/2)⁴` | counting on Hamming staircase (PR #739) | no |
| Define `c_k(r, u_0) = (u_0² - (k-2)²r²) / (4 · ((k-2)²r² + u_0²)²)`: this is `((1/4)·(u_0² - (k-2)²r²) / ((k-2)²r² + u_0²)²)`, the per-corner curvature at level `k` | algebraic factoring of the all-orders integrand | no |
| Identity `(1/64) Σ_k binomial(4,k) · X_k = Σ_k w_k · (X_k / 4)` for any sequence `X_k`, so PR #773 eq. (2) `=` Σ_k w_k · c_k(r, u_0) | trivial algebraic rearrangement | no |
| `Σ_k w_k = (1+4+6+4+1)/16 = 1` | binomial sum `Σ binom = 2⁴` | no |
| `c_2(r, u_0) = 1/(4 u_0²)` r-independent: at `k=2`, `(k-2)² = 0`, so the Wilson shift drops | scalar substitution | no |
| `c_0 = c_4`, `c_1 = c_3`: under `k → 4-k`, `(k-2)² → (2-k)²` is invariant | scalar `k ↔ 4-k` symmetry | no |
| At `r = 0`: every `c_k → u_0²/(4·u_0⁴) = 1/(4 u_0²)`, hence `Σ w_k c_k = (1)·(1/(4u_0²)) = 1/(4u_0²)`, matching parent eq. `[5]` | scalar substitution + (4) | no |
| At `r = r_all_orders ≈ 0.26855`: `Σ w_k c_k(r) = (m_H_PDG/v)²` exactly (in `Fraction` arithmetic to bisection precision); cross-validates PR #773's bisection result | exact-rational evaluation | no |

Every load-bearing step is exact-rational arithmetic, scalar algebra,
or a counting fact on `(Z/2)⁴`. The Wilson plaquette form, staggered
phases, link unitaries, and lattice scale `a` do not appear as load-
bearing inputs to (1)–(6).

## Exact Arithmetic Check

The runner verifies, at exact rational precision via
`fractions.Fraction`:

(A) **Weight normalization.** `Σ_k w_k = 1` exactly with
`w_k = binomial(4, k)/16`.

(B) **Reduction at `r = 0`.** `c_k(0, u_0) = 1/(4 u_0²)` for every
`k ∈ {0,1,2,3,4}`, so `Σ_k w_k c_k(0, u_0) = 1/(4 u_0²)` (matches parent
eq. `[5]`).

(C) **`k = 2` Wilson-decoupling.** `c_2(r, u_0) = 1/(4 u_0²)` exactly,
independent of `r`. Verified at `r ∈ {0, 0.1, 0.235, 0.26855, 0.4}`.

(D) **Reflection symmetry.** `c_0(r, u_0) = c_4(r, u_0)` and
`c_1(r, u_0) = c_3(r, u_0)` exactly. Verified at multiple `r`.

(E) **Cross-validation against PR #773 all-orders form.** Define
`total_PR773(r) = (1/64) Σ_k binomial(4,k) · (u_0² - (k-2)²r²) / ((k-2)²r² + u_0²)²`
and compare to `Σ_k w_k c_k(r) = (1/16) Σ_k binomial(4,k) · c_k(r) · 4`.
Verify `Σ_k w_k c_k(r) == total_PR773(r)` exactly in `Fraction` at
`r ∈ {0, 0.1, 0.235, 0.26855, 0.4}`.

(F) **Closure cross-check at `r = 0.26855`.** Verify
`Σ_k w_k c_k(0.26855) ≈ (m_H_PDG/v)²` with `m_H_PDG = 125.10 GeV`
(comparison input only, NOT load-bearing for derivation), to within the
bisection tolerance of PR #773.

(G) **Per-level numerical breakdown at `r = r_all_orders ≈ 0.26855`.**
Print each `w_k`, `c_k`, and `w_k · c_k`, showing how the total `≈
(m_H_PDG/v)² ≈ 0.2581` decomposes across the 5 levels.

## Dependencies

- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  for the parent eq. `[4]–[5]` uniform-`N_taste = 16` identification and
  the `σ ↔ <ψ̄ψ>` taste-singlet identification (line 146).
- [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
  for the staircase multiplicities `binomial(4, k)` on the 16 BZ corners
  of `Z³+t`.
- [`WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md)
  for the all-orders total formula and the closure value `r_all_orders ≈
  0.26855`. **Forward-reference;** on a sister branch.
- [`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
  for the `m* = -4r` extremum and the underlying `k → 4-k` reflection
  symmetry. **Forward-reference;** on a sister branch.
- [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md)
  for the prior boundary statement that uniform-`N_taste = 16` is non-
  derived. **Forward-reference;** on a sister branch.
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  for the staggered-Dirac realization gate context.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  for the framework axioms `A1` (`Cl(3)`) and `A2` (`Z³`).

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner. The runner handles the forward-references
gracefully (per the established pattern: `[INFO]` rather than `[FAIL]`
when a sister-branch note is not yet on `origin/main`).

## Boundaries

This note does **not** close:

- **the +12% Higgs gap chain.** The all-orders closure value
  `r_all_orders ≈ 0.26855` is unchanged by this re-organization (the
  decomposition (1) is mathematically equivalent to PR #773 eq. (2)).
- **the σ = taste-singlet identification itself.** This note treats
  σ = taste-singlet as the **structural** input from the parent Higgs
  note (line 146); it does not derive that identification from
  framework axioms. The identification follows the standard staggered
  prescription `σ ↔ <ψ̄ψ>` (chiral condensate is a trace ⇒ taste-
  singlet). **Boundary statement:** if a future framework derivation
  identifies `σ` with a non-taste-singlet representation (taste-octet,
  taste-pseudoscalar, etc.), the weights `w_k` would change and the
  closure value of `r` would shift accordingly. Per-channel closure
  values for non-taste-singlet identifications are computed in the
  parallel sister note
  [`WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md`](WILSON_M_H_PER_CHANNEL_CLOSURE_BOUNDED_NOTE_2026-05-09.md)
  (forward-reference; sister branch).
- **other admissions of PR #773.** Tree-level mean-field formalism (no
  CW, no RGE) and non-zero Wilson coefficient `r` (not part of canonical
  pure-Kogut-Susskind staggered) remain in place.
- **the value of the Wilson coefficient `r` itself.** Closure value
  `r ≈ 0.26855` is the all-orders closure under the σ = taste-singlet
  identification + parent admissions, not a derivation of `r`.
- **any parent theorem/status promotion.**

What this note **does** do is factor the parent's previously-monolithic
"uniform-`N_taste = 16` admission" into:

  (A) the structural identification `σ = taste-singlet` (standard
      staggered prescription, not a free numerical parameter); plus
  (B) the counting fact that 16 corners of `Z³+t` decompose with
      multiplicities `binomial(4, k)` (PR #739 staircase, on `origin/main`).

Both (A) and (B) are more constrained than a free choice of `N_taste`,
so this is a meaningful tightening even though it does not retire (A)
to an axiom-level derivation.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_higgs_taste_singlet_projection.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: under σ = taste-singlet (parent identification), the all-orders
Wilson-corrected (m_H_W/v)² decomposes on the Hamming staircase as
Σ_k w_k · c_k(r, u_0) with derived weights w_k = binomial(4,k)/16 and
per-corner curvatures c_k(r, u_0) = (u_0² - (k-2)²r²)/(4·((k-2)²r² + u_0²)²).
Three structural consequences verified: (i) k=2 channel r-decoupled
(c_2 = 1/(4u_0²) for all r); (ii) k → 4-k reflection symmetry
(c_0 = c_4, c_1 = c_3); (iii) reduction at r=0 to parent's 1/(4u_0²).
Cross-validates PR #773 total at r ∈ {0, 0.1, 0.235, 0.26855, 0.4}.
The decomposition factors the parent's uniform-N_taste=16 admission
into σ = taste-singlet (structural) + binom(4,k) staircase counting,
both more constrained than a free N_taste numerical choice.
```
