# Wilson-Corrected m_H_tree at Extremum, All Orders in r — Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_wilson_m_h_tree_at_extremum_all_orders.py`](../scripts/frontier_wilson_m_h_tree_at_extremum_all_orders.py)

## Claim

Building on the exact-in-`r` curvature at the Wilson-shifted extremum
`m^* = -4 r` derived in
[`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
(forward-reference; sister branch — note that the sister filename's
`LEADING_ORDER_IN_R` qualifier refers to that note's own leading-order
expansion of the curvature about `r = 0`; the sister note's eq. (1)
itself, which we cite below, is the *exact* curvature at `m^*`),

```text
d^2 V^W / dm^2  |_{m = m^*}
   =  ( 1 / 4 ) · Σ_{k=0}^{4}  binomial(4, k) ·
        ( ( k - 2 )^2 r^2  -  u_0^2 )  /  ( ( k - 2 )^2 r^2  +  u_0^2 )^2,         (1)
```

and the parent Higgs note's
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) eqs.
`[3]–[5]` per-channel identification under the uniform-`N_taste = 16`
admission (non-derived; bounded in
[`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md)
forward-reference), the *all-orders-in-r* closed form for the tree-
level Wilson-corrected Higgs mass is

```text
( m_H_tree^W / v )^2
   =  ( 1 / 64 ) · Σ_{k=0}^{4}  binomial(4, k) ·
        ( u_0^2  -  ( k - 2 )^2 r^2 )  /  ( ( k - 2 )^2 r^2  +  u_0^2 )^2.        (2)
```

Equivalently:

```text
m_H_tree^W
   =  ( v / 8 ) · sqrt( Σ_{k=0}^{4} binomial(4, k) ·
                          ( u_0^2 - ( k - 2 )^2 r^2 )
                        / ( ( k - 2 )^2 r^2 + u_0^2 )^2 ).                       (3)
```

Equation (2) is exact in `r` (and in `u_0`). It reduces to the
parent eq. `[5]` `(m_H_tree / v)^2 = 1 / (4 u_0^2)` at `r = 0` (each
summand is `1/u_0^2`, summing to `16/u_0^2`, dividing by `64` gives
`1/(4 u_0^2)`); and it reduces to PR-#761's leading-order form
`(1/(4u_0^2)) · (1 - 3 r^2 / u_0^2) + O(r^4)` at small `r`.

Setting (2) equal to `(m_H_PDG / v)^2` (with `m_H_PDG = 125.10 GeV`
used as comparison input only, not load-bearing for derivation) gives
an exact algebraic comparison equation in `r`. Bisecting in `Fraction`
arithmetic (canonical `u_0 = 0.8776`, `v = 246.22 GeV`) on the
bracket `[0.26, 0.28]` gives the all-orders matching value

```text
r_all_orders  ≈  0.26855   ± 10^{-5}                                              (4)
```

vs the leading-order matching value `r_leading ≈ 0.23572` from
[`WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
(forward-reference; sister branch). The sister note's `r_leading ≈
0.23572` is the *mass-level linear-Taylor* matching value, obtained by
truncating `sqrt(1 - 3 r^2/u_0^2)` linearly to give `m_H_W ≈ m_H_zero·(1
- (3/2) r^2/u_0^2)` and solving for `r`. The relative shift between
this leading-order value and all-orders is

```text
( r_all_orders  -  r_leading )  /  r_leading   ≈   13.9 %                        (5)
```

(mass-level linear-Taylor comparison). For an apples-to-apples
square-form comparison, the square-form leading-order matching equation
`(m_H_W/v)^2 = (1/(4u_0^2))·(1 - 3 r^2/u_0^2) = (m_H_PDG/v)^2` (no
sqrt-truncation) solves exactly to `r_LO_square ≈ 0.22925`, giving

```text
( r_all_orders  -  r_LO_square )  /  r_LO_square   ≈   17.1 %                    (5')
```

Both comparisons (5) and (5') describe the same all-orders shift; they
differ in *which* leading-order observable is being squared. Either
way the all-orders correction is non-trivial (`~14–17 %`) and is not
captured by the leading-order Taylor truncation.

The all-orders value sits within the perturbative-Taylor
radius-of-convergence boundary `r < u_0 / 2 ≈ 0.439` (set by the
dominant `k = 0, 4` summands, which control the ratio test). At
`r ≈ 0.269` the dimensionless expansion parameter is
`(2r/u_0)^2 ≈ 0.37`, so the perturbative Taylor expansion converges
but with non-negligible higher-order corrections — successive Taylor
contributions fall by a factor `~2-3` at `r ≈ 0.269` (asymptotic
ratio `~4` only at much smaller `r`). The all-orders closed form (2)
is the unique resummation that captures these corrections exactly.

This note records the all-orders closed form and the all-orders
matching value. It does **not** close the +12% Higgs gap chain. The
matching readout (4) is conditional on:
1. the uniform-`N_taste = 16` channel admission (non-derived);
2. the tree-level mean-field formalism (no CW corrections, no RGE
   running);
3. a non-zero Wilson coefficient `r` (not part of the canonical pure-
   Kogut-Susskind staggered setup).

Any of (1)–(3) failing voids the matching readout.

## Proof-Walk

| Step | Load-bearing input | Lattice-action input? |
|---|---|---|
| Exact curvature at `m^* = -4r` from sister extremum note: `(1/4) Σ_k binomial(4,k)·((k-2)^2 r^2 - u_0^2)/((k-2)^2 r^2 + u_0^2)^2` | sister forward-reference [`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md) | no |
| Per-channel identification under uniform-`N_taste = 16` (parent eqs. `[4]–[5]`): `\|d^2V/dm^2\|_per-channel = \|total\|/16` | parent Higgs note + admitted convention | no |
| Sign flip: total curvature is negative (tachyonic), so `\|d^2V/dm^2\| = u_0^2 - (k-2)^2 r^2` per term, etc. | algebraic sign | no |
| Resulting `(m_H_W / v)^2 = \|per-channel\| = (1/64) · Σ_k binomial(4,k) · (u_0^2 - (k-2)^2 r^2) / ((k-2)^2 r^2 + u_0^2)^2` (eq. (2)) | direct substitution | no |
| Reduction at `r = 0`: each summand `→ 1/u_0^2`; sum `→ 16/u_0^2`; divide by 64 `→ 1/(4 u_0^2)`; matches parent eq. `[5]` | binomial-state-count `Σ binom = 16` | no |
| Reduction at leading order in `r^2` via Taylor `(u_0^2 - x) / (u_0^2 + x)^2 = 1/u_0^2 - 3 x / u_0^4 + O(x^2)` with `x = (k-2)^2 r^2`: leading term gives `1/(4 u_0^2)`, second term gives `-(3/64) · Σ binom·(k-2)^2 r^2 / u_0^4 = -(3·16)/(64·u_0^4) r^2 = -3 r^2 / (4 u_0^4)`. Combining: `(1/(4u_0^2))·(1 - 3 r^2 / u_0^2) + O(r^4)`, matching PR #761 | scalar Taylor + binomial-moment `Σ binom·(k-2)^2 = 16` | no |
| All-orders matching equation: `(m_H_W / v)^2 = (m_H_PDG / v)^2` with `m_H_PDG = 125.10` (comparison input only), giving `(2)` evaluated at unknown `r` equal to a known rational target | algebraic equation in one variable `r` | no |
| Bisection in `Fraction`: bracket `r ∈ [0.26, 0.28]` (chosen so that the bracket endpoints have opposite-sign `(m_H_W/v)^2 - (m_H_PDG/v)^2` — verified directly: `f(0.26) > 0`, `f(0.28) < 0`); evaluate at midpoint and halve bracket until width `≤ 10^{-5}` | exact-rational bisection | no |
| Result: `r_all_orders ≈ 0.26855` after N bisection steps | bisection convergence | no |
| Comparison to leading-order linear-form (PR #761): `r_leading ≈ 0.23572`; relative shift `(r_all_orders - r_leading)/r_leading ≈ 0.139` (≈ 13.9 %) | scalar arithmetic | no |
| Validity check: `r_all_orders ≈ 0.269 < u_0 / 2 ≈ 0.439`, well within the radius of convergence of the perturbative Taylor expansion (set by the dominant `k = 0, 4` summands, where the relevant ratio is `(2r/u_0)^2 ≈ 0.37 < 1`) | scalar comparison | no |

Every load-bearing step is exact-rational arithmetic, scalar calculus
on a known closed form, or `Fraction` bisection. The Wilson plaquette
form, staggered phases, link unitaries, and lattice scale `a` do not
appear as load-bearing inputs to (2)–(5).

## Exact Arithmetic Check

The runner verifies, at exact rational precision via
`fractions.Fraction`:

(A) **Exact closed form.** Direct evaluation of (2) at several
`(r, u_0)` pairs, including `r = 0` (which gives `1/(4 u_0^2)`
exactly, matching parent eq. `[5]`).

(B) **Reduction to PR-#761 leading order.** Taylor-expand (2) in `r^2`
at `r = 0`. The leading term is `1/(4 u_0^2)`, the next term is
`-3 r^2 / (4 u_0^4)`, summing to `(1/(4u_0^2))·(1 - 3 r^2 / u_0^2) +
O(r^4)`. Verified by extracting the coefficient of `r^2 / u_0^4` in
the Taylor expansion at small `r`; it equals `-3/4` exactly (the
runner extracts this directly).

(C) **Bisection for `r_all_orders`.** Solve `(m_H_W / v)^2 = (m_H_PDG /
v)^2` by bisection in `Fraction` arithmetic on the bracket `[0.26,
0.28]`. The `m_H_PDG = 125.10 GeV` is used as comparison input only
(NOT load-bearing for derivation; runner labels this explicitly).
Bracket endpoints verified opposite-sign: `f(0.26) > 0`, `f(0.28) < 0`.
Bisect until the bracket width is `≤ 10^{-5}`. Result: `r_all_orders
∈ [0.26854, 0.26856]`, i.e. `0.26855 ± 10^{-5}`.

(D) **Comparison to leading-order.** `r_leading = 0.23572` (from PR
#761, which solves the linear-Taylor matching equation). Relative
shift `(r_all_orders - r_leading) / r_leading ≈ 0.139 = 13.9 %`. The
leading-order linear-Taylor approximation under-estimates `r` by
about `14 %`.

(E) **Perturbative-validity confirmation.** `r_all_orders ≈ 0.269 <
u_0 / 2 ≈ 0.439`, well within the radius of convergence of the
perturbative Taylor expansion of the all-orders form. The dominant
expansion parameter is `(2r / u_0)^2 ≈ 0.37` (set by the `k = 0, 4`
summands, where `(k - 2)^2 = 4`), so successive Taylor coefficients
fall by a factor `~3-5` per order — convergent but slow, which is
why leading-order is `~14 %` off.

## Dependencies

- [`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
  for the exact curvature at `m^* = -4r`. **Forward-reference;** on a
  sister branch.
- [`WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
  for the leading-order matching value `r ≈ 0.235`. **Forward-reference;**
  on a sister branch.
- [`WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md`](WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md)
  for the `V_taste^W` formula. **Forward-reference;** on a sister
  branch.
- [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
  for the staircase multiplicities `binomial(4, k)`.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  for the parent tree-level setup, eqs. `[3]–[6]`, and the uniform-
  `N_taste = 16` channel admission. (Per Gap #3 lite 2026-05-10 the
  parent note's headline quantity is now labeled `m_curv_tree` — a
  per-channel symmetric-point curvature scale of V_taste, NOT a
  Higgs-mass pole; this all-orders Wilson-correction note continues to
  use the older `m_H_tree` symbol internally for its bounded
  source-surface calculation, but the imported quantity should be read
  as `m_curv_tree` for first-principles-honest scope.)
- [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md)
  for the boundary statement that the uniform-`N_taste = 16` choice is
  itself a non-derived admission. **Forward-reference;** on a sister
  branch.
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  for the staggered-Dirac realization gate context.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  for the framework baseline (physical Cl(3) local algebra plus Z^3
  spatial substrate).

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner. The runner handles the forward-references
gracefully (per the established pattern: `[INFO]` rather than `[FAIL]`
when a sister-branch note is not yet on `origin/main`).

## Boundaries

This note does not close:

- the +12% Higgs gap chain in [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md). The all-orders matching value `r ≈ 0.269` is **conditional** on:
  1. the uniform-`N_taste = 16` channel admission (non-derived);
  2. the tree-level mean-field formalism (no CW corrections, no RGE
     running);
  3. a non-zero Wilson coefficient `r`, **not** part of the canonical
     pure-Kogut-Susskind staggered setup.
  Any of (1)–(3) failing voids the matching readout;
- the physical Higgs mass `m_H` numerical value (`m_H_PDG = 125.10` is
  treated as a comparison input only, not a derivation input);
- the value of the Wilson coefficient `r` itself (the `r ≈ 0.269`
  value is the *all-orders matching value under the admissions*, not a
  derivation of `r`);
- the plaquette mean-field link `u_0` numerical value;
- the staggered-Dirac realization gate;
- the `g_bare = 1` derivation;
- any parent theorem/status promotion;
- the exact algebraic matching root for `r`. The bisection result
  `r ≈ 0.26855 ± 10^{-5}` is approximate; it is not a derivation of
  a canonical Wilson coefficient.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_wilson_m_h_tree_at_extremum_all_orders.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: all-orders closed form (m_H_W/v)^2 = (1/64) Σ_k binomial(4,k) ·
(u_0^2 - (k-2)^2 r^2) / ((k-2)^2 r^2 + u_0^2)^2 verified at exact
rational precision. Reduces to 1/(4u_0^2) at r=0 (matches parent eq.
[5]) and to PR-#761's leading order at small r. Bisection gives
r_all_orders ≈ 0.26855 ± 10^{-5}, a ~14% shift from the leading-order
matching value 0.23572. The all-orders shift is non-trivial: leading-
order linear-Taylor under-estimates r by ~14% under the canonical
admissions. The matching readout is conditional on uniform-N_taste=16 + tree-level
+ non-zero r.
```
