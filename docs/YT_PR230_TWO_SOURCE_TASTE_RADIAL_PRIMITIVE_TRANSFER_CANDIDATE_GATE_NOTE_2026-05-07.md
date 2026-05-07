# PR230 Two-Source Taste-Radial Primitive-Transfer Candidate Gate

**Status:** bounded support plus exact boundary / finite `C_sx` rows do not
certify a physical primitive neutral transfer

## Purpose

This block tests whether the ready two-source taste-radial production rows can
populate the missing physical primitive/off-diagonal neutral transfer premise
from the same-surface neutral multiplicity-one contract.

The candidate is intentionally narrow: the existing row packet supplies
finite same-ensemble `C_ss/C_sx/C_xx` correlator blocks for the certified
source/complement chart.  The gate asks whether that finite off-diagonal
correlator support is already enough to act as H3, the physical neutral
transfer or off-diagonal generator.

## Result

It is not enough on the current surface.

The ready packet has 20 of 63 chunks.  On those ready rows the finite
off-diagonal `C_sx` entries are present, and the finite `2x2`
`C_ss/C_sx/C_xx` blocks have positive Gram determinants.  That is real
support for the two-source chart and for future Schur/source-Higgs work.

The row is still a correlator/covariance entry, not a transfer/action matrix.
It does not provide a positive primitive cone orientation, a primitive power,
an irreducible generator, an isolated-pole kernel derivative, a finite-volume
or IR transfer limit, a canonical `O_H` identity, or `kappa_s` authority.
Taking absolute values or stochastic-normalizing the finite covariance rows
would import the missing transfer theorem.

## Non-Claim

This is not retained or `proposed_retained` closure.  It does not promote
taste-radial `x` to canonical `O_H`, does not treat finite `C_sx/C_xx` aliases
as `C_sH/C_HH` pole rows, and does not set `kappa_s`, `c2`, or `Z_match` to
one.

## Verification

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate.py
# SUMMARY: PASS=13 FAIL=0
```

## Exact Next Action

Supply a same-surface physical neutral transfer/action row or off-diagonal
generator theorem, or a model-class/pole/FV/IR theorem that converts the
measured `C_ss/C_sx/C_xx` block into a primitive neutral transfer and couples
it to canonical `O_H`.
