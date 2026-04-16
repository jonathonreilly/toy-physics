# Exact Fundamental-Disk Activity Theorem on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact local character theorem + exact disk-sector census through `n <= 5`  
**Script:** `scripts/frontier_fundamental_disk_activity_theorem.py`

## Question

Can any part of the current quotient-surface gas be promoted from a formal
`p^(|S|-1)` placeholder to an exact finite-`beta` activity law?

## Exact answer

Yes, one specific part can.

The exact one-plaquette anchor

`p = P_1plaq(beta)`

is the normalized fundamental character coefficient of the Wilson plaquette
weight. For simply-sheeted disk surfaces, the isolated fundamental-sheet
activity is therefore exactly `p^A`.

This does **not** yet close the full plaquette, because the full
character-labeled / sheet-enriched activity law for the non-disk /
higher-sheet sectors remains open.

## Theorem 1: `p` is an exact fundamental character coefficient

Expand the one-plaquette Wilson weight in `SU(3)` characters:

`w_beta(U) = exp[(beta/6)(Tr U + Tr U^dag)] = sum_R c_R(beta) chi_R(U)`.

For the trivial and fundamental representations, the exact Toeplitz/Bessel
minor formulas are

- `c_0(beta) = sum_m det[I_(m-i+j)(beta/3)]`
- `c_f(beta) = sum_m det[I_(m+lambda_i-i+j)(beta/3)]` with `lambda = (1,0,0)`

and at `beta = 6` the runner finds

- `c_0(6) = 3.441440354987778`
- `c_f(6) = 4.362353340283927`

The normalized fundamental coefficient is therefore

`c_f(6) / (3 c_0(6)) = 0.422531739649983`.

That is exactly the one-plaquette plaquette expectation:

`P_1plaq(6) = 0.422531739649983`.

So the local anchor `p` is not a heuristic local weight. It is the exact
normalized fundamental character coefficient.

## Theorem 2: exact isolated simply-sheeted disk activity

Take an oriented simply-sheeted plaquette surface `Sigma` with one boundary
component and area `A`.

Using only:

1. the fundamental character coefficient `c_f`
2. the trivial coefficient `c_0`
3. the two-point Haar identity `int dU U_ij U^dag_kl = delta_il delta_jk / 3`
4. the normalized observable factor `1/3 Tr`

the isolated fundamental-sheet amplitude of `Sigma` is

`(c_f / (3 c_0))^A = p^A`.

The reason is the usual ribbon-graph Euler counting on a disk:

- each plaquette contributes `c_f / c_0`
- each occupied link contributes `1/3`
- the free color loops contribute `3`
- the normalized boundary trace contributes `1/3`

and for a disk the net color factor is exactly `1`.

So for simply-sheeted disks, the direct quotient-surface activity is exact.

## Theorem 3: exact simply-sheeted disk census through `n <= 5`

Now take the quotient-distinct anchored surface set already constructed in
`docs/QUOTIENT_SURFACE_ENGINE_NOTE.md`.

For each quotient key `dV`, form the actual spanning surface

`S = dV xor q`

by removing the tagged plaquette.

The runner then checks, exactly:

- edge incidences are only `1` or `2`
- boundary edge count is exactly `4`
- the face adjacency graph is connected
- Euler characteristic is exactly `1`

to identify the simply-sheeted disk sector.

Through `n <= 5` this gives:

- total unique quotient surfaces: `589824`
- simply-sheeted disk surfaces: `449632`
- non-disk / higher-sheet remainder: `140192`
- exact unique quotient-surface polynomial:
  - `4 p^4 + 60 p^8 + 80 p^10 + 1092 p^12 + 2792 p^14 + 24468 p^16 + 70180 p^18 + 421432 p^20 + 68832 p^22 + 884 p^24`

and the exact disk-sector polynomial

`4 p^4 + 60 p^8 + 80 p^10 + 1092 p^12 + 2720 p^14 + 22740 p^16 + 62400 p^18 + 360536 p^20`.

## Theorem 4: first non-disk deviation

There is a small exact cross-level duplicate artifact in the old level-by-level
counting surface:

- `64 p^10 + 56 p^12`.

Once that is removed, the first genuine non-disk / higher-sheet deviation from
the exact unique quotient-surface sector turns on at

`72 p^14 + 1728 p^16 + 7780 p^18 + 60896 p^20 + 68832 p^22 + 884 p^24`.

So the isolated fundamental-disk law matches the full exact unique
quotient-surface sector through `p^12`, and the first genuine non-disk /
higher-sheet sector begins at `p^14`.

This is the direct quotient-surface analog of the earlier rooted-shell warning:
the geometry is controlled, but the non-disk sector appears early.

## Exact isolated disk-sector value at `beta = 6`

Evaluating the exact disk-sector polynomial at

`p = P_1plaq(6) = 0.422531739649983`

gives

- `H_fund,unique^(n<=5)(6) = 1.306925044135047`
- `P_fund,unique,iso^(n<=5)(6) = 0.552217312490512`
- `H_fund,disk^(n<=5)(6) = 1.300882882458081`
- `P_fund,disk,iso^(n<=5)(6) = 0.549664307405897`

So the isolated non-disk / higher-sheet sector contributes exactly

`0.002553005084615`

through the current unique quotient window.

These are exact isolated finite-`beta` sector values, not formal placeholders.

## Area-5 consistency check

The exact first nonlocal connected coefficient from
`docs/PLAQUETTE_FIRST_NONLOCAL_CONNECTED_CORRECTION_NOTE.md` is

`beta^5 / 472392`.

The isolated fundamental-disk law reproduces that exactly at leading order:

`4 p(beta)^5 = beta^5 / 472392 + O(beta^6)`.

So the first constructive nonlocal gauge theorem and the new direct
character-activity theorem are consistent on their overlap.

## Why this matters

This is the first exact finite-`beta` activity theorem on the direct
quotient-surface route.

It does not solve the whole plaquette, but it removes one major ambiguity:

- the local anchor `p` is now exact character data, not a guessed weight
- the exact unique quotient-surface sector is now separated from the small
  cross-level duplicate artifact
- the simply-sheeted disk sector is now an exact finite-`beta` sector
- the first genuine non-disk window is now sharply localized at `p^14`

So the route is now:

1. exact local character coefficient
2. exact disk-sector activity
3. first non-disk `Z_3` lift split
4. first non-disk character-foam split
5. exact finite-periodic-lattice character/intertwiner foam law
6. open low-carrier `B/X` defect compression

## Honest status

This note still does **not** by itself derive the full plaquette `P(6)`.

It proves the exact direct finite-`beta` law only for the isolated
simply-sheeted disk sector through the currently enumerated quotient surface
window.

The remaining missing theorem is now narrower:

`docs/FIRST_NONDISK_Z3_LIFT_THEOREM_NOTE.md` now proves that the first genuine
non-disk window cannot be carried by a scalar `p`-only quotient-surface gas:
`52` of the first `72` non-disk surfaces admit no pure fundamental
face-orientation lift at all.

`docs/FIRST_NONDISK_CHARACTER_FOAM_THEOREM_NOTE.md` sharpens that once more:
even the minimal plaquette-character face alphabet `{3, 3bar, 8}` still
misses those same `52` singular surfaces. The exact first non-disk defect
signatures are `B^1X^3` and `B^4`.

`docs/CHARACTER_INTERTWINER_FOAM_LAW_NOTE.md` now closes the full exact
finite-periodic-lattice law.

So the remaining missing theorem is no longer a vague “non-disk correction,”
or even the full finite-`beta` law. It is specifically:

> a compact compression of the exact character/intertwiner foam law onto the
> quotient foam with local baryon-junction `B` and crossing `X` defects.

## Commands run

```bash
python3 scripts/frontier_fundamental_disk_activity_theorem.py
```

Output summary:

- exact normalized fundamental character coefficient equals `P_1plaq(6)`
- exact disk-sector census through `n <= 5`
- exact unique quotient-surface polynomial
- exact cross-level duplicate polynomial `{10: 64, 12: 56}`
- exact disk-sector polynomial
- exact isolated unique-surface sector value `0.552217312490512`
- exact isolated disk-sector value `0.549664307405897`
- exact first genuine non-disk deviation polynomial starting at `p^14`
