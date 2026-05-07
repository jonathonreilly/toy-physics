# PR230 Degree-One Radial-Tangent O_H Theorem

**Status:** exact-support / degree-one radial-tangent `O_H` uniqueness theorem;
same-surface action/LSZ premise and pole rows absent

**Runner:** `scripts/frontier_yt_pr230_degree_one_radial_tangent_oh_theorem.py`
**Certificate:** `outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json`

## Purpose

This block sharpens the cleanest source-Higgs route.  The question is not
whether Z3 symmetry alone identifies canonical `O_H`; that shortcut is already
blocked.  The narrower theorem is:

```text
If a future same-surface EW/Higgs action proves that canonical O_H is a
linear Z3-covariant infinitesimal radial tangent in span{S0,S1,S2}, which
axis is selected?
```

## Exact Result

On `C^8 = (C^2)^{otimes 3}`, define

```text
S0 = sigma_x I I
S1 = I sigma_x I
S2 = I I sigma_x
```

The tensor-factor cycle sends `S0 -> S1 -> S2 -> S0`.  A degree-one tangent

```text
T = a0 S0 + a1 S1 + a2 S2
```

is Z3-invariant only when `a0 = a1 = a2`.  Therefore the unique degree-one
radial line is

```text
R = (S0 + S1 + S2) / sqrt(3)
```

with Hilbert-Schmidt norm matched to the source identity on the taste block.
The unit Hilbert-Schmidt axis is `(S0 + S1 + S2) / sqrt(24)`.

This exactly selects the taste-radial source axis implemented by the
two-source harness, but only under the future action premise that canonical
`O_H` is a degree-one radial tangent.

## Boundary

The current PR230 surface does not derive that action premise.  If higher
commuting taste invariants are allowed, Z3-invariant trace-zero candidates
remain nonunique:

```text
E1 = S0 + S1 + S2
E2 = S0 S1 + S1 S2 + S2 S0
E3 = S0 S1 S2
```

Thus this theorem is a real axis-selection support artifact, not closure.  It
does not provide the same-surface EW/Higgs action, canonical kinetic/LSZ
normalization, canonical `O_H` certificate, `C_ss/C_sH/C_HH` pole rows,
source-Higgs Gram purity, FV/IR control, matching/running, or retained-route
authorization.

## Non-Claim

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not identify the current taste-radial source with canonical `O_H` on
the actual surface, does not set `kappa_s`, `c2`, or `Z_match` to one, and
does not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`,
plaquette, `u0`, reduced pilots, or value recognition.

## Verification

```bash
python3 scripts/frontier_yt_pr230_degree_one_radial_tangent_oh_theorem.py
# SUMMARY: PASS=14 FAIL=0
```

## Exact Next Action

Use this theorem only after deriving the same-surface EW/Higgs action and
canonical LSZ normalization.  Then run source-Higgs pole rows
`C_ss/C_sH/C_HH` and the Gram/FV/IR gates.
