# Hierarchy BBS Staggered Taste-Blocking Bridge Scaffold Availability

**Date:** 2026-05-11
**Claim type:** bounded_theorem
**Status authority:** source note only. Audit verdicts and effective status
are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_hierarchy_bbs_staggered_taste_blocking_bridge_scaffold_availability_bounded.py`](../scripts/frontier_hierarchy_bbs_staggered_taste_blocking_bridge_scaffold_availability_bounded.py)

## Scope

This note narrows the BBS-style taste-blocking bridge question after the
earlier bridge no-go
[`HIERARCHY_BBS_STAGGERED_TASTE_BLOCKING_BRIDGE_NARROW_NO_GO_NOTE_2026-05-10.md`](HIERARCHY_BBS_STAGGERED_TASTE_BLOCKING_BRIDGE_NARROW_NO_GO_NOTE_2026-05-10.md).
It records that useful external scaffold pieces exist, while the framework
bridge remains open.

The relevant local functional-analysis input is the abstract Banach
contraction theorem
[`BBS_RG_BANACH_CONTRACTION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](BBS_RG_BANACH_CONTRACTION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md).
That theorem gives the norm inequality once a Banach space, map, and
contraction constant are supplied. This note does not supply those
framework-specific objects for the staggered taste-blocking bridge.

## Scaffold Availability

Two external scaffold domains are relevant:

1. Brydges-Guadagni-Mitter finite-range Gaussian covariance
   decompositions apply to scalar Gaussian covariance kernels, including
   massless lattice Green-function settings in dimension at least 3
   (arXiv:math-ph/0303013; J. Stat. Phys. 115 (2004), 415-449).
   This weakens any blanket claim that finite-range covariance
   decomposition is unavailable in four-dimensional scalar covariance
   contexts.
2. Balaban/Dimock constructive RG methods give small-field and
   contraction-style scaffolds in rigorous lattice field theory settings
   (for example Dimock, arXiv:1108.1335, and the Balaban lattice-gauge RG
   programme). This weakens any blanket claim that no constructive RG
   Banach-space scaffold exists near lattice gauge theory.

These are useful route-pruning facts, not a closure theorem for the
framework bridge.

## Admissions

The bridge remains bounded for three independent reasons:

1. The scalar Gaussian covariance scaffold is not a coupled
   gauge-plus-staggered-fermion covariance construction.
2. The constructive RG scaffold is not a completed framework Banach space
   and map for the staggered taste-blocking transformation.
3. The operational identification `kappa = alpha_LM` is not derived. The
   framework values from
   [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
   and
   [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
   are admitted numerical context for a transparency check, not a proof
   that a BBS contraction constant equals `alpha_LM`.

The observed-principle hierarchy surface
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
is therefore not promoted by this note.

## Boundary

This bounded note does not claim:

- construction of a framework Banach space for staggered taste blocking;
- a proof that the staggered taste-blocking map is a strict contraction;
- a derivation of `kappa = alpha_LM`;
- closure of the hierarchy formula;
- any new framework axiom or repo-wide premise.

The safe result is scaffold availability plus explicit open admissions.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_bbs_staggered_taste_blocking_bridge_scaffold_availability_bounded.py
```

Expected result: `PASS=9 FAIL=0`. A passing run checks only the bounded
scaffold/admission table and the `kappa = alpha_LM` transparency boundary.
