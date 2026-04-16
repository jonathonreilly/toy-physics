# First Non-Disk Character-Foam Theorem on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact first non-disk carrier split; plaquette-character foam incomplete  
**Script:** `scripts/frontier_first_nondisk_character_foam_theorem.py`

## Question

After the exact `Z_3` lift no-go, what is the smallest honest character
carrier for the first genuine non-disk sector?

More concretely:

1. does the minimal plaquette-character face alphabet `{3, 3bar, 8}` already
   carry the full first non-disk window?
2. if not, what exact extra local carrier data is forced?

## Exact answer

The minimal plaquette-character face alphabet does **not** carry the whole
first non-disk window.

It carries exactly:

- the `8` genus-1 ribbon surfaces
- the `12` quadrivalent crossing surfaces

and it fails exactly on:

- the `48` mixed singular surfaces
- the `4` trivalent singular surfaces

So the first honest direct-route object is not:

- a scalar `p`-only surface gas
- or even a plaquette-character foam with face labels only

It is a quotient foam with explicit local singular-link defect slots.

At first non-disk order those exact defect slots are:

- `X`: the quadrivalent crossing link tensor
- `B`: the baryon junction link tensor

## Exact local character data

At `beta = 6`, the exact normalized one-plaquette character coefficients are:

- fundamental:
  - `p_3(6) = c_(1,0,0)(6) / (3 c_0(6)) = 0.422531739649983`
- adjoint:
  - `p_8(6) = c_(2,1,0)(6) / (8 c_0(6)) = 0.162259799479938`

So the smallest plausible face alphabet is

`{3, 3bar, 8}`.

Here `8` is the minimal center-neutral plaquette character.

## Exact local singular-link tensors

Two exact local `SU(3)` link tensors are forced immediately:

### Crossing tensor `X`

At a quadrivalent singular link the local integral is the `2U 2Udag` Haar
tensor. For `SU(3)` it has two invariant channels with exact coefficients

- `+1/8`
- `-1/24`

So `X` is a genuine two-channel local link carrier.

### Baryon tensor `B`

At a trivalent singular link the local integral is the `3U` or `3Udag` baryon
tensor, with exact coefficient

- `1/6`

and unique invariant tensor `epsilon`.

So `B` is a genuine one-channel baryon junction carrier.

## Theorem 1: exact first non-disk class split

The exact first genuine non-disk sector at `p^14` consists of:

- `(15, -1, 4, ((1,4), (2,28)))` with multiplicity `8`
- `(15, 3, 4, ((1,4), (2,20), (4,4)))` with multiplicity `12`
- `(15, 3, 3, ((1,3), (2,21), (3,1), (4,3)))` with multiplicity `48`
- `(15, 3, 0, ((2,24), (3,4)))` with multiplicity `4`

where the tuple is

`(area, Euler characteristic, boundary-edge count, edge-incidence histogram)`.

## Theorem 2: exact plaquette-character feasibility

Now allow the minimal face alphabet `{3, 3bar, 8}` on each plaquette face.

The runner solves the exact mod-`3` boundary-charge system and then imposes the
exact boundary pair constraint together with the exact local `SU(3)` link
support condition on all internal links.

Result:

- genus-1 ribbon class:
  - feasible assignments: `1`
- quadrivalent crossing class:
  - feasible assignments: `9`
- mixed singular class:
  - feasible assignments: `0`
- trivalent singular class:
  - feasible assignments: `0`

So the minimal plaquette-character foam carries exactly `20` of the first `72`
non-disk surfaces, and misses exactly `52`.

This sharpens the earlier `Z_3` lift theorem:

the failure is not just “no pure fundamental orientation lift.”

Even after adding the minimal neutral plaquette character `8`, the `52`
singular surfaces are still not carried.

## Theorem 3: exact defect signatures

Read the singular-link content directly from the exact edge-incidence
histograms:

- genus-1 ribbon class:
  - defect signature `B^0 X^0`
- quadrivalent crossing class:
  - defect signature `B^0 X^4`
- mixed singular class:
  - defect signature `B^1 X^3`
- trivalent singular class:
  - defect signature `B^4 X^0`

So the exact first non-disk carrier split is:

- pure ribbon sector
- pure crossing sector
- mixed baryon-plus-crossing sector
- pure baryon-junction sector

## What this closes

This closes the next layer of ambiguity in the direct plaquette route.

The missing object is no longer just “a character-labeled surface foam.”

That is still too small.

The first non-disk theorem now forces the direct exact carrier to be:

> a quotient foam with plaquette character labels on faces and explicit local
> `B` / `X` defect slots on singular links.

So the direct route is now:

1. exact quotient-distinct anchored surfaces
2. exact local plaquette characters `3`, `3bar`, `8`
3. exact first non-disk carrier split
4. exact finite-periodic-lattice character/intertwiner foam law
5. required next object: a compact low-carrier compression onto the `B/X`
   defect foam

## Honest status

This note still does **not** by itself derive the full plaquette `P(6)`.

What it does derive is the exact first non-disk carrier structure.

That is enough to kill the last remaining “face-only” version of the direct
closure and replace it with the right local object.

`docs/CHARACTER_INTERTWINER_FOAM_LAW_NOTE.md` now supplies the full exact
finite-periodic-lattice law, and
`docs/FINITE_BX_LOW_CARRIER_NO_GO_NOTE.md` now rules out any exact small
finite `B/X` closure. So the open problem is now narrower:

`docs/POISSONIZED_OCCUPATION_INTERTWINER_COMPRESSION_NOTE.md` now supplies that
useful exact resummed/state-compressed representation. So the open problem is
now narrower still:

> find a faster evaluator or recursion for the already exact compressed law
> whose first explicit singular-link sectors are the local `B` and `X`
> defects.

## Commands run

```bash
python3 scripts/frontier_first_nondisk_character_foam_theorem.py
```

Output summary:

- exact `p_3(6)` and `p_8(6)`
- exact `X` coefficients `1/8` and `-1/24`
- exact `B` coefficient `1/6`
- exact plaquette-character feasibility split `20 / 52`
- exact first non-disk defect signatures `B^0X^0`, `B^0X^4`, `B^1X^3`, `B^4X^0`
