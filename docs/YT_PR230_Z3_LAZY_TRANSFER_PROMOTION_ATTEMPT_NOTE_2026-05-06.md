# PR230 Z3 Lazy-Transfer Promotion Attempt

**Status:** exact negative boundary / Z3 lazy-transfer promotion not derivable
from current same-surface cyclic action

**Runner:** `scripts/frontier_yt_pr230_z3_lazy_transfer_promotion_attempt.py`

**Certificate:** `outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json`

## Purpose

The same-surface Z3 taste-triplet artifact now supplies an exact cyclic action
on the PR230 taste-scalar axes.  The conditional primitive theorem also proves
that the lazy matrix

```text
L = (I + P) / 2
```

is primitive once it is a same-surface neutral transfer.  This block asks
whether those two facts already authorize the missing PR230 neutral
primitive/lazy-transfer certificate.

## Result

No.  The promotion is not derivable on the current surface.

The runner verifies the exact finite-matrix facts:

- `P^3 = I`;
- the pure cyclic action `P` is periodic and not primitive;
- `L^2 = (I + 2P + P^2)/4` has strictly positive entries;
- `L` differs from `P` by a load-bearing identity/self edge.

The current PR230 parent artifacts encode only the symmetry action `P`.  They
do not encode a physical neutral transfer, same-source action row, lazy
aperiodic self term, off-diagonal neutral generator, or strict primitive-cone
certificate.

## Identifiability Boundary

The same current parent data are compatible with two physical interpretations:

```text
Model A: physical transfer = P
         periodic, not primitive

Model B: physical transfer = (I + P)/2
         primitive
```

Since the current artifacts specify the symmetry `P` but do not select `A`
versus `B` as PR230 dynamics, choosing `B` would import an unproved lazy/self
transfer term.  That is exactly the forbidden shortcut.

## Claim Boundary

This note does not claim retained or proposed-retained top-Yukawa closure.  It
does not write a neutral primitive-cone certificate, does not treat symmetry
averaging as physical dynamics, does not identify `O_sp`, `O_s`, or the taste
triplet with canonical `O_H`, and does not use `H_unit`, `yt_ward_identity`,
observed targets, `alpha_LM`, plaquette, `u0`, or unit assignments for
`kappa_s`, `c2`, or `Z_match`.

## Exact Next Action

To reopen this route positively, supply one of:

- `outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06.json`;
- a strict same-surface off-diagonal neutral-generator certificate;
- a strict neutral primitive-cone certificate;
- an independent bypass through canonical `O_H/C_sH/C_HH`, same-source W/Z
  response, Schur `A/B/C` rows, or scalar-LSZ authority.

## Verification

```bash
python3 scripts/frontier_yt_pr230_z3_lazy_transfer_promotion_attempt.py
# SUMMARY: PASS=17 FAIL=0
```
