# Higgs-Channel Effective N_taste Boundary Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_higgs_channel_effective_ntaste_boundary.py`](../scripts/frontier_higgs_channel_effective_ntaste_boundary.py)

## Claim

Given the Wilson-term Hamming-weight staircase identity for the 16 BZ
corners of the staggered Kogut-Susskind Dirac fermion action with Wilson
plaquette gauge action on `Z^3 + t = Z^4` APBC at the minimal block
(`L = 2`, `N_sites = 2^4 = 16`), proved combinatorially in
[`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
with multiplicities `(1, 4, 6, 4, 1) = binomial(4, hw)` and Wilson mass
shifts `(0, 2r, 4r, 6r, 8r)` for `hw ∈ {0, 1, 2, 3, 4}`, the staircase
identity does **not** by itself fix the effective `N_taste` appearing in
formula [5] of
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md):

```text
(m_H / v)^2  =  4 / ( u_0^2 · N_taste )                                  [5]
```

Specifically, if the Higgs is identified with a **single** Hamming-weight
class `hw = k`, the effective `N_taste^(k) = binomial(4, k)`, and the
five candidate single-class assignments give five distinct tree-level
values `m_H_tree^(k)`. None of them coincide with the existing 140.3 GeV
headline of `HIGGS_MASS_FROM_AXIOM_NOTE.md`. The `N_taste = 16` choice
that produces the existing 140.3 GeV headline is the **uniform**
all-corners admission that treats the 16 corners as one Higgs channel;
that choice is itself an admitted convention, not a structural derivation
from the Wilson staircase.

This is a narrow boundary statement on the Wilson staircase identity.
It does not add a new axiom, does not pick a Higgs channel, does not
close the `+12%` Higgs gap, and does not promote
`HIGGS_MASS_FROM_AXIOM_NOTE.md` or
`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`.

## Channel-assignment table

For each Hamming-weight class `k ∈ {0, 1, 2, 3, 4}`, treating the Higgs
as identified with that single class gives effective
`N_taste^(k) = binomial(4, k)` in formula [5] and the tree-level value

```text
m_H_tree^(k)  =  v · sqrt( 4 / ( u_0^2 · binomial(4, k) ) ),             (1)
```

with the Higgs note's stated `v = 246.22 GeV` and `u_0 = 0.8776`. The
runner computes `(m_H_tree^(k))^2` exactly as `Fraction` and reports
the numerical square root only for display. Numerical values rounded to
0.1 GeV:

| `k` | `N_taste^(k) = binomial(4, k)` | `m_H_tree^(k)` (GeV) |
|---|---|---|
| 0 | 1  | 561.1 |
| 1 | 4  | 280.6 |
| 2 | 6  | 229.1 |
| 3 | 4  | 280.6 |
| 4 | 1  | 561.1 |

For comparison, the **uniform all-corners** assignment (the choice made
by `HIGGS_MASS_FROM_AXIOM_NOTE.md`) sets `N_taste = 1 + 4 + 6 + 4 + 1
= 16`, giving the existing headline

```text
m_H_tree(uniform 16)  =  v · sqrt( 4 / ( u_0^2 · 16 ) )  =  v / ( 2 u_0 )
                     =  140.3 GeV.                                       (2)
```

None of the five single-class values in (1) coincides with the uniform
value (2). The uniform choice `N_taste = 16` is therefore an
independent admission about how the Wilson-broken corner classes
contribute to the Higgs-mass curvature; the staircase identity alone
does not select it.

## Exact Arithmetic Check

The runner repeats the channel-assignment computation with
`fractions.Fraction`, using

- `v = Fraction(24622, 100) = Fraction(12311, 50)` (the Higgs note's
  stated `v = 246.22 GeV`);
- `u_0 = Fraction(8776, 10000) = Fraction(1097, 1250)` (the Higgs note's
  stated `u_0 = 0.8776`);
- `binomial(4, k)` for `k ∈ {0, 1, 2, 3, 4}` evaluated as exact integers.

For each `k` the runner computes

```text
( m_H_tree^(k) )^2  =  v^2 · 4  /  ( u_0^2 · binomial(4, k) )            (3)
```

as an exact `Fraction`, and verifies that the five values are pairwise
different from the uniform-`N_taste = 16` value `v^2 / (4 u_0^2)`. The
runner also verifies

```text
binomial(4, 0) + binomial(4, 1) + binomial(4, 2) + binomial(4, 3)
   + binomial(4, 4)  =  1 + 4 + 6 + 4 + 1  =  16,                        (4)
```

confirming that summing the staircase multiplicities back gives the
uniform-16 admission, which is the structural identity that makes the
`N_taste = 16` choice consistent with the staircase but not selected by
it.

## Dependencies

- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  for the parent assertion (formula [5]: `m_H/v = 1/(2 u_0)` with
  `N_taste = 16`) being bounded by this note. This note bounds the
  parent's `N_taste` slot from below; it does not promote, replace, or
  extend the parent. (Per Gap #3 lite 2026-05-10 the parent note now
  labels the `v/(2 u_0)` quantity `m_curv_tree` — a per-channel
  symmetric-point curvature scale of V_taste, NOT a Higgs-mass pole;
  this channel-boundary note continues to use the older `m_H_tree`
  symbol internally for the bounded staircase calculation, but the
  imported quantity should be read as `m_curv_tree` for
  first-principles-honest scope.)
- [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
  for the upstream load-bearing combinatorial input (the
  `(1, 4, 6, 4, 1)` multiplicities and `(0, 2r, 4r, 6r, 8r)` Wilson
  shifts on the 16 BZ corners of `Z^3 + t` APBC at `L = 2`).
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  and [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- the `+12%` Higgs gap chain in `HIGGS_MASS_FROM_AXIOM_NOTE.md`;
- the Higgs-channel assignment itself (which Hamming-weight class is
  the Higgs, or whether the uniform sum over all 16 corners is forced);
- any derivation of the Wilson coefficient `r` or the mean-field
  plaquette link `u_0`;
- the staggered-Dirac realization gate;
- the continuum-limit `m_H / m_W` flow;
- any retention upgrade of `HIGGS_MASS_FROM_AXIOM_NOTE.md`;
- any retention upgrade of
  `WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`;
- any claim that one of the five single-class values is preferred over
  the others;
- any claim that the uniform `N_taste = 16` choice is wrong; the
  boundary statement is only that it is an admission, not a derived
  consequence of the staircase identity;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_higgs_channel_effective_ntaste_boundary.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: the Wilson Hamming-weight staircase does not by itself fix
N_taste in HIGGS_MASS_FROM_AXIOM_NOTE.md formula [5]; the five
single-class assignments give five distinct m_H_tree values, none of
which coincides with the uniform-16 admission that produces the
existing 140.3 GeV headline.
```
