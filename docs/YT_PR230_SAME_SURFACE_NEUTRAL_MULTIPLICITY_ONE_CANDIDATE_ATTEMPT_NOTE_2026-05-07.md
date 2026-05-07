# PR230 Same-Surface Neutral Multiplicity-One Candidate Attempt

**Status:** exact negative boundary / candidate attempt rejected on the current
PR230 surface

## Purpose

This note records the first concrete attempt to populate the candidate path
required by the same-surface neutral multiplicity-one intake gate:

```text
outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json
```

The attempt is intentionally strict.  A file at that path is not evidence by
itself; it must pass the same-surface representation, multiplicity-one or
primitive-generator, canonical metric/LSZ, source-overlap, and claim-firewall
obligations.

## Result

The current PR230 surface fails the candidate contract.  The same-surface
neutral completion still contains two neutral singlets:

```text
source_singlet, orthogonal_neutral_singlet
```

The current `Z3` action is trivial on that two-singlet block.  Source-only
observables remain fixed while the candidate canonical-Higgs direction rotates
through the orthogonal neutral slot.  The degree-one invariant dimension is
two, the commutant dimension is four, and the current surface supplies no
physical primitive/off-diagonal transfer selecting a unique canonical radial
generator.

The candidate also lacks the other load-bearing requirements:

- no canonical inverse-propagator derivative / LSZ metric;
- no finite-volume/IR/zero-mode limiting order;
- no source-to-canonical-Higgs identity;
- no measured `C_spH/C_HH` pole-overlap rows;
- no selection rule excluding the orthogonal neutral top coupling.

## Non-Claim

This is not retained or `proposed_retained` closure.  It does not certify
`O_H`, does not set `kappa_s = 1`, does not promote Z3 cone support into a
physical transfer, and does not treat source-only rows as source-Higgs overlap
evidence.

## Verification

```bash
python3 scripts/frontier_yt_pr230_same_surface_neutral_multiplicity_one_candidate_attempt.py
# SUMMARY: PASS=15 FAIL=0
```

## Exact Next Action

Retire at least one failed obligation with a same-surface artifact: derive a
physical primitive/off-diagonal neutral transfer, derive a selection rule
excluding the orthogonal neutral top coupling, supply canonical scalar LSZ
metric/FV/IR normalization, or measure `C_spH/C_HH` pole-overlap rows.
