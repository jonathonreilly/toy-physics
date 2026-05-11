# Wilson-Corrected m_H_tree at Extremum, Leading Order in r — Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_wilson_m_h_tree_at_extremum_leading_order_in_r.py`](../scripts/frontier_wilson_m_h_tree_at_extremum_leading_order_in_r.py)

## Claim

Working with:
- the Wilson-corrected `V_taste^W` formula derived in
  [`WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md`](WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md)
  (landed in the same review-loop batch);
- the exact extremum location `m^* = -4r` and leading-order curvature at
  `m^*` derived in
  [`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
  (landed in the same review-loop batch);
- the *uniform-`N_taste = 16`* Higgs-channel admission used in
  [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  eqs. `[4]–[6]` (the channel admission that
  [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md)
  bounds as a non-derived convention),

the tree-level Wilson-corrected Higgs mass at the (Wilson-shifted)
extremum is

```text
( m_H_tree^W / v )^2
   =  ( 1 / ( 4 u_0^2 ) ) · ( 1  -  3 r^2 / u_0^2 )   +   O( r^4 ).               (1)
```

Equivalently,

```text
m_H_tree^W
   =  ( v / ( 2 u_0 ) ) · sqrt( 1 - 3 r^2 / u_0^2 )                              (2)
   ≈  ( v / ( 2 u_0 ) ) · ( 1  -  ( 3 / 2 ) r^2 / u_0^2  +  O( r^4 ) ).          (3)
```

At `r = 0` this reduces to `m_H_tree = v / ( 2 u_0 )`, the parent
note's eq. `[6]` headline `m_H_tree = 140.3 GeV` (with `v = 246.22 GeV`
and `u_0 = 0.8776`).

For small `r`, the Wilson correction *reduces* `m_H_tree^W` below the
`r = 0` value. Setting (3) equal to the PDG value
`m_H = 125.10 GeV` and solving for `r / u_0` at leading order (each
`≈` below absorbs an `O(r^4)` remainder from the leading-order Taylor
expansion in (3)):

```text
1  -  ( 3 / 2 ) ( r / u_0 )^2  ≈  m_H_PDG / m_H_tree^{r=0}  ≈  0.892,
( 3 / 2 ) ( r / u_0 )^2        ≈  0.108,
( r / u_0 )^2                  ≈  0.072,
r / u_0                        ≈  0.268,                                         (4)
r                              ≈  0.235                                          (5)
```

at `u_0 ≈ 0.8776`. This is a leading-order matching value under the
uniform-`N_taste = 16` admission, not a closure of the +12% Higgs gap.

This note records the leading-order Wilson correction to
`m_H_tree`. It does **not** close the +12% Higgs gap chain (the
admission is non-derived, the perturbative expansion fails at
`r = O(u_0)`, and the framework's canonical setup is `r = 0` pure
Kogut-Susskind staggered, so any specific `r > 0` requires admitting
a Wilson coefficient that is not part of the canonical surface). It
records what the leading-order Wilson correction *would be* given a
nonzero `r` plus the uniform admission.

## Proof-Walk

| Step | Load-bearing input | Lattice-action input? |
|---|---|---|
| Parent eq. `[3]`: total taste curvature `d^2 V/dm^2 \|_{m=0} = -N_taste / (4 u_0^2)` at uniform `N_taste = 16` (gives `-4 / u_0^2`) | parent Higgs note tree-level setup | already-admitted Wilson + staggered surface (cited upstream) |
| Wilson-shifted total curvature `d^2 V^W/dm^2 \|_{m=-4r} = -4/u_0^2 + 12 r^2/u_0^4 + O(r^4)` | same-batch source note [`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md) | no |
| Per-channel taste curvature under uniform-`N_taste = 16` admission: `(4/u_0^2 - 12 r^2/u_0^4) / 16  =  1/(4 u_0^2) · (1 - 3 r^2 / u_0^2)` at leading order | uniform-`N_taste = 16` admission (parent eqs. `[4]–[6]`) | no |
| Parent identification `(m_H_tree / v)^2 = \|per-channel curvature\|` (parent eq. `[5]`) | parent Higgs note observable mapping | no |
| Resulting `(m_H_tree^W / v)^2 = (1 / 4 u_0^2) · (1 - 3 r^2 / u_0^2) + O(r^4)` | direct substitution (1) | no |
| Square-root: `m_H_tree^W = v / (2 u_0) · sqrt(1 - 3 r^2 / u_0^2)` (positive convention) | algebra | no |
| Taylor expand at small `r`: `sqrt(1 - x) ≈ 1 - x/2 - x^2/8 - ...` with `x = 3 r^2 / u_0^2`: `m_H_tree^W ≈ v/(2 u_0) · (1 - (3/2) r^2 / u_0^2) + O(r^4)` | scalar Taylor expansion | no |
| Reduction at `r = 0`: `m_H_tree^W = v / (2 u_0) = 140.3 GeV` (with `v = 246.22 GeV`, `u_0 = 0.8776`) | matches parent eq. `[6]` headline | no |
| Leading-order matching `r` value: setting (3) equal to the comparison value `m_H_PDG = 125.10 GeV` and solving gives `r / u_0 ≈ 0.268`; with `u_0 = 0.8776`, `r ≈ 0.235` | scalar algebra | no |

Every load-bearing step is finite combinatorics (already verified at
the upstream notes), scalar calculus, or exact rational arithmetic.
The Wilson plaquette form, staggered phases, link unitaries, lattice
scale `a`, plaquette numerical value `<P>` (other than the admitted
`u_0 = 0.8776` from the parent surface), and Monte Carlo machinery
do not appear as load-bearing inputs to (1)–(5). The Wilson
coefficient `r` is carried symbolically.

## Exact Arithmetic Check

The runner verifies, at exact rational precision via `fractions.Fraction`:

(A) **Reduction at `r = 0`:** with `u_0 = Fraction(8776, 10000)` and
`v = Fraction(24622, 100)`:

```text
m_H_tree^{r=0} = v / (2 u_0) = 24622 / (2 · 8776 / 100)
              = 24622 / 175.52  GeV
              = 140.281 GeV (rounded), within rounding of parent's 140.3.
```

The runner verifies the exact `Fraction` value matches the parent eq.
`[6]` headline.

(B) **Leading-order coefficient `(3/2)`:** verify `m_H_tree^W /
m_H_tree^{r=0} = sqrt(1 - 3r^2/u_0^2) ≈ 1 - (3/2) r^2/u_0^2` at small `r`.
Direct extraction at `r = 1/100, 1/1000, 1/10_000`:

```text
c(r) := (m_H_tree^{r=0} - m_H_tree^W) / (r^2 / u_0^2 · m_H_tree^{r=0})
      → (3/2) = 1.5  as  r → 0.
```

The runner extracts `c(r)` at successively smaller `r` and verifies
convergence to `3/2` cleanly.

(C) **Leading-order matching value `r ≈ 0.235`:** solving `1 - (3/2)(r/u_0)^2 ≈ m_H_PDG /
m_H_tree^{r=0}` for `r` at leading order (the `≈` absorbs the
`O(r^4)` remainder from (3)):
- `m_H_tree^{r=0} = v / (2 u_0) = 246.22 / (2 · 0.8776) ≈ 140.281` GeV
  (the parent's headline `140.3 GeV` is the same value rounded);
- `m_H_PDG / m_H_tree^{r=0} = 125.10 / 140.281 ≈ 0.8918` (note: PDG
  value is treated as a *comparison input*, not as a derivation input);
- `(3/2)(r/u_0)^2 ≈ 1 - 0.8918 = 0.1082`;
- `(r/u_0)^2 ≈ 0.0722`;
- `r/u_0 ≈ 0.2686`;
- `r ≈ 0.2686 · 0.8776 ≈ 0.2357`.

The runner reports this leading-order matching value with `m_H_PDG`
clearly labelled as a comparison input (no PDG-pin promotion to
load-bearing).

(D) **Perturbative-expansion validity boundary:** the leading-order
expansion (3) is valid when `(3/2)(r/u_0)^2 << 1`, i.e. `r/u_0 << 1`,
or roughly `r < u_0 / sqrt(3) ≈ 0.51` at `u_0 = 0.8776`. At `r = O(u_0)`
the expansion fails (the all-orders sum is needed). The runner exhibits
the breakdown by direct comparison of the closed-form (2) with the
leading-order (3) at `r ∈ {0.1, 0.235, 0.5, 0.8}`.

## Dependencies

- [`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
  for the curvature at `m^* = -4r`, leading-order in `r`.
- [`WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md`](WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md)
  for the explicit `V_taste^W` formula.
- [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
  for the staircase multiplicities `binomial(4, k)` and Wilson mass
  shifts `2 r k`.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  for the parent tree-level setup, the uniform-`N_taste = 16` channel
  identification (eqs. `[4]–[6]`), and the headline `v / (2 u_0) =
  140.3 GeV`. (Per Gap #3 lite 2026-05-10 the parent note now labels
  this quantity `m_curv_tree` — a per-channel symmetric-point curvature
  scale of V_taste, NOT a Higgs-mass pole; this Wilson-correction note
  continues to use the older `m_H_tree` symbol internally for its
  bounded source-surface calculation, but the imported quantity should
  be read as `m_curv_tree` for first-principles-honest scope.)
- [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md)
  for the boundary statement that the uniform-`N_taste = 16` choice is
  itself a non-derived admission.
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  for the staggered-Dirac realization gate context.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  for the framework baseline (physical Cl(3) local algebra plus Z^3
  spatial substrate).

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

The runner also remains tolerant of pre-merge validation order, but in
this landing the referenced Wilson notes are included in the same batch.

## Boundaries

This note does not close:

- the +12% Higgs gap chain in [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md). The leading-order closure value `r ≈ 0.235` is **conditional** on:
  1. the uniform-`N_taste = 16` Higgs-channel admission (non-derived; bounded in [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md));
  2. the leading-order Taylor expansion (which fails at `r = O(u_0)`);
  3. a non-zero Wilson coefficient `r`, which is **not** part of the canonical pure-Kogut-Susskind staggered setup of the parent Higgs note's eqs. `[1]–[2]`.
  Any of (1), (2), (3) failing voids the closure;
- the physical Higgs mass `m_H` numerical value (`m_H_PDG = 125.10` is treated as a comparison input only, not a derivation input);
- the all-orders Wilson correction to `m_H_tree`;
- the value of the Wilson coefficient `r` itself (a separate normalization choice; the `r ≈ 0.235` value is a *leading-order matching value under the channel admission*, not a derivation of `r`);
- the plaquette mean-field link `u_0` numerical value;
- the staggered-Dirac realization gate;
- the `g_bare = 1` derivation;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_wilson_m_h_tree_at_extremum_leading_order_in_r.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: m_H_tree^W = (v / (2 u_0)) · sqrt(1 - 3 r^2 / u_0^2) at the
Wilson-shifted extremum, leading order in r. Reduces to 140.3 GeV at
r = 0 (matches parent eq. [6]). Wilson correction REDUCES m_H_tree.
Leading-order matching to the comparison mass occurs at r ≈ 0.235 with u_0 ≈
0.8776, conditional on the uniform-N_taste=16 admission (non-derived
per HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE) and on the
perturbative-expansion validity (which fails at r = O(u_0)).
```
