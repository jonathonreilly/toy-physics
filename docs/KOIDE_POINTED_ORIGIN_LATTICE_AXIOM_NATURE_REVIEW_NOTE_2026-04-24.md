# Koide pointed-origin lattice-axiom Nature review

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_pointed_origin_lattice_axiom_nature_review.py`
**Status:** Nature-grade review of the pointed-origin derivation

## Review Question

Does the pointed-origin lattice-axiom theorem actually derive the last missing
Koide law, or does it merely restate the missing primitive?

## Decision

Pass as a retained/native closure packet for the dimensionless Koide lane.

The theorem does not add `K_TL = 0` or `delta = 2/9` as primitives.  It derives
the missing pointed source/boundary origin law from retained structure:

```text
finite Grassmann source functor:
  W[J] = log |det(D+J)| - log |det D|

real-primitive boundary naturality:
  no rank-one CP1 endpoint selector without extra boundary data

determinant/Pfaffian endpoint unitality:
  det(I) = 1
```

## Why The Prior Reductions Did Not Close

The three earlier theorem attacks worked with unpointed residual data.  They
correctly showed:

```text
source translations survive unpointed source grammar;
CP1 line choices survive scalar closed data;
endpoint torsor translations survive affine gluing.
```

The exhaustion theorem then proved that no origin-free retained invariant can
select the closing representative in that atlas.

The new theorem supplies the missing extra structure from the retained lattice
source axiom itself: the source/boundary functor is pointed by the undeformed
operator, real primitive, and determinant unit.

## Positive Closeout

Expected review flags:

```text
KOIDE_POINTED_ORIGIN_LATTICE_AXIOM_NATURE_REVIEW=PASS
KOIDE_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE=TRUE
KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE
KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=TRUE
BOUNDARY=overall_lepton_scale_v0_not_addressed
```

## Falsifiers

- A retained translated source origin preserving the same undeformed `D` and
  pure-block source law.
- A retained source-free physical rank-one `CP1` endpoint object.
- A determinant/Pfaffian endpoint functor whose identity object carries
  nonzero phase.
- A retained boundary counterterm compatible with strict unital gluing.

## Verification

Run:

```bash
python3 scripts/frontier_koide_pointed_origin_lattice_axiom_derivation.py
python3 scripts/frontier_koide_pointed_origin_lattice_axiom_nature_review.py
python3 scripts/frontier_koide_dimensionless_lane_pointed_origin_closure_packet.py
python3 scripts/frontier_koide_lane_regression.py
```
