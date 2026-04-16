# First Non-Disk `Z_3` Face-Orientation Lift Theorem on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact first non-disk lift theorem; pure `p`-only quotient gas ruled out  
**Script:** `scripts/frontier_first_nondisk_z3_lift_theorem.py`

## Question

Can the first genuine non-disk correction to the direct quotient-surface gas be
carried by a pure fundamental-sheet activity law on unoriented quotient
surfaces?

Equivalently: if we take the exact first non-disk window in the unique
quotient-surface series, can every surface there be lifted to a sign assignment
on its plaquette faces that satisfies the exact local `SU(3)` link constraints?

## Exact answer

No.

At the first genuine non-disk power `p^14`, the unique quotient-surface sector
splits exactly into four geometric classes. Only two of those classes admit a
pure fundamental face-orientation lift. The other two classes admit **no**
such lift at all.

So a scalar `p`-only quotient-surface gas cannot be exact on the full first
non-disk sector. The direct exact closure object must be a character-labeled,
or equivalently sheet-enriched, quotient foam.

## Setup

From `docs/FUNDAMENTAL_DISK_ACTIVITY_THEOREM_NOTE.md`, the first genuine
non-disk deviation in the exact unique quotient-surface sector begins at

`72 p^14`.

Each quotient surface in that window has area `15`, so the `H`-series power is
`|S| - 1 = 14`.

For a pure fundamental-sheet lift, assign a sign `sigma_f = +-1` to each
plaquette face of the surface. Then:

- `sigma_f = +1` means the canonical fundamental plaquette orientation
- `sigma_f = -1` means the conjugate orientation

At each internal link, the exact `SU(3)` Haar integral can only be nonzero if
the local fundamental/anti-fundamental counts satisfy

`n_U - n_Udag == 0 mod 3`.

Since the first non-disk window has link incidences at most `4`, the only
allowed internal patterns are

- `(1,1)`
- `(2,2)`
- `(3,0)`
- `(0,3)`

The four boundary links must match the tagged plaquette boundary exactly.

So every candidate pure fundamental lift can be checked by exhaustive
enumeration of all `2^15` face-sign assignments on a representative surface.

## Theorem 1: exact geometric class split at `p^14`

The `72` exact first non-disk surfaces split into the following four classes:

- `(15, 3, 3, ((1,3), (2,21), (3,1), (4,3)))` with multiplicity `48`
- `(15, 3, 4, ((1,4), (2,20), (4,4)))` with multiplicity `12`
- `(15, -1, 4, ((1,4), (2,28)))` with multiplicity `8`
- `(15, 3, 0, ((2,24), (3,4)))` with multiplicity `4`

Here the tuple means

`(area, Euler characteristic, boundary-edge count, edge-incidence histogram)`.

So the first genuine non-disk window is already geometrically mixed: one
orientable manifold class, one quadrivalent crossing class, and two more
singular classes involving trivalent/quadruple local structure.

## Theorem 2: exact pure-fundamental lift counts

Exhaustive `2^15` face-sign enumeration gives the exact number of valid pure
fundamental `Z_3` lifts for each class:

- `(15, 3, 3, ((1,3), (2,21), (3,1), (4,3)))`: `0`
- `(15, 3, 4, ((1,4), (2,20), (4,4)))`: `3`
- `(15, -1, 4, ((1,4), (2,28)))`: `1`
- `(15, 3, 0, ((2,24), (3,4)))`: `0`

So exactly

- `20` of the `72` first non-disk surfaces admit a pure fundamental lift
- `52` of the `72` do not

This is already an exact no-go against a pure `p`-only quotient-surface gas on
the full first non-disk sector.

## Theorem 3: the genus-1 manifold subclass is exact ribbon data

The class

`(15, -1, 4, ((1,4), (2,28)))`

is the unique orientable manifold class in the `p^14` non-disk window.

It has

- `8` surfaces
- exactly `1` valid pure fundamental lift per surface
- only `(1,1)` internal links in that lift

So it is a pure ribbon-manifold sector, and its exact isolated color factor is

`3^(chi - 1) = 3^(-2) = 1/9`.

Therefore its exact contribution to the `H`-series at the first non-disk power
is

`(8/9) p^14`.

At `beta = 6`, using `p = P_1plaq(6) = 0.422531739649983`, that is

`(8/9) p^14 = 0.000005138995130`.

So one exact part of the first non-disk sector is now fully understood.

## Theorem 4: the first direct-route obstruction is now explicit

The remaining three classes fall into two sharply different behaviors:

- the quadrivalent crossing class with multiplicity `12` does admit pure
  fundamental lifts, but only through internal `(2,2)` link sectors
- the `48`-surface mixed trivalent/quadruple class and the `4`-surface
  trivalent class admit **no** pure fundamental face-orientation lift at all

That means the missing direct-route object is no longer vague.

It is not “some correction to `p^A`.”

It is specifically:

> an exact character-labeled or sheet-enriched quotient foam that can carry the
> lift-impossible first non-disk classes.

So the direct route has now crossed a real theorem threshold: the first place
where a pure fundamental-sheet gas fails is identified exactly.

## Why this matters

Before this note, the direct quotient route still left open the hope that the
entire non-disk sector might be an orientation-decorated but still scalar
`p`-only correction.

That hope is now gone.

The first genuine non-disk window already forces a richer exact object.

So the direct route is now:

1. exact local character anchor `p = P_1plaq(6)`
2. exact disk-sector activity law
3. exact first non-disk `Z_3` lift split
4. exact first non-disk character-foam split
5. exact finite-periodic-lattice character/intertwiner foam law
6. exact no-go against any small finite `B/X` low-carrier closure
7. exact Poissonized occupation/intertwiner compression of that infinite-carrier
   law
8. required next object: a faster evaluator for the already exact compressed law

## Honest status

This note still does **not** close the full plaquette `P(6)`.

What it does is remove the last credible version of the scalar direct-route
closure:

> a pure `p`-only quotient-surface gas cannot be exact once the first genuine
> non-disk sector turns on.

That is now an exact theorem, not a suspicion.

The exact next layer is now recorded in
`docs/FIRST_NONDISK_CHARACTER_FOAM_THEOREM_NOTE.md`: even the minimal
plaquette-character face alphabet `{3, 3bar, 8}` still misses the `52`
singular surfaces, so the direct carrier must include explicit local `B`
baryon-junction and `X` crossing defects in any low-carrier compression.

`docs/CHARACTER_INTERTWINER_FOAM_LAW_NOTE.md` now closes the full exact law on
the retained finite periodic lattice, and
`docs/FINITE_BX_LOW_CARRIER_NO_GO_NOTE.md` now rules out any exact small
finite `B/X` closure. `docs/POISSONIZED_OCCUPATION_INTERTWINER_COMPRESSION_NOTE.md`
now supplies the useful exact resummed/state-compressed representation itself.
So what remains open is not the law itself, not a small finite carrier, and not
the basic compression question either, but only a faster evaluator for the
already exact compressed law.

## Commands run

```bash
python3 scripts/frontier_first_nondisk_z3_lift_theorem.py
```

Output summary:

- exact `p^14` non-disk class multiplicities
- exact pure-fundamental `Z_3` lift counts by class
- exact admissible total `20`
- exact lift-impossible total `52`
- exact genus-1 manifold subclass contribution `(8/9) p^14`
