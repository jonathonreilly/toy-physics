# Legendre Source-Pole Operator Construction

**Date:** 2026-05-03
**Status:** bounded-support / Legendre source-pole operator constructed; canonical `O_H` identity open
**Runner:** `scripts/frontier_yt_legendre_source_pole_operator_construction.py`
**Certificate:** `outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json`

```yaml
actual_current_surface_status: bounded-support
proposal_allowed: false
canonical_higgs_operator_identity_passed: false
bare_retained_allowed: false
```

## Result

The Cl(3)/Z3 scalar source functional does determine one same-surface operator:
the LSZ-normalized source-pole operator.

Let `s` couple to the PR230 scalar source operator `O_s`, and let the connected
same-source two-point function have an isolated pole

```text
C_ss(x) = Z_s / x + analytic,        x = p^2 - p_*^2.
```

Then the inverse connected source denominator satisfies

```text
dGamma_ss/dx | pole = 1 / Z_s,
```

so the Legendre/LSZ source-pole operator is

```text
O_sp(q) = sqrt(dGamma_ss/dx | pole) O_s(q).
```

It has unit pole residue:

```text
Res(C_sp,sp) = (dGamma_ss/dx | pole) Res(C_ss) = 1.
```

This construction is invariant under source-coordinate rescaling
`O_s -> c O_s`, since `Z_s -> c^2 Z_s` and
`dGamma_ss/dx -> (dGamma_ss/dx)/c^2`.  It is also insensitive to analytic
source contact terms: contact terms change the regular part of `C_ss`, not the
isolated pole residue.

Verification:

```bash
python3 scripts/frontier_yt_legendre_source_pole_operator_construction.py
# SUMMARY: PASS=17 FAIL=0
```

## What This Derives

This derives the maximal source-only operator currently available on PR230:

```text
O_sp = LSZ-normalized scalar source pole.
```

It is a real positive support object for the next route.  It removes the
arbitrary source-unit normalization from the source-pole side without setting
`kappa_s = 1`.

## Why This Is Not Yet `O_H`

The physical canonical Higgs radial operator used by `v` requires a further
identity:

```text
O_sp = O_H
```

up to a sign convention.  The current surface does not prove that identity.
A mixed neutral scalar family remains possible:

```text
O_sp = cos(theta) O_H + sin(theta) O_chi.
```

The source-pole normalization stays fixed for all `theta`, while the
source-Higgs Gram determinant changes as `1 - cos(theta)^2`.  Only
`cos(theta) = +/-1` certifies the `O_H` identity.

## Exact Next Certificate

To turn this source-pole operator into canonical `O_H`, one of the following
must close:

- same-surface canonical `O_H` identity and normalization certificate;
- pole-level `C_sH` / `C_HH` residues satisfying
  `Res(C_sH)^2 = Res(C_ss) Res(C_HH)`;
- a rank-one neutral-scalar theorem excluding orthogonal admixture;
- a same-source W/Z response certificate fixing the sector overlap.

## Non-Claims

- This note does not claim retained or `proposed_retained` top-Yukawa closure.
- This note does not define `O_H` by fiat.
- This note does not identify `O_s` or `O_sp` with canonical `H`.
- This note does not set `kappa_s = 1` or `cos(theta) = 1`.
- This note does not use `H_unit`, `yt_ward_identity`, observed targets,
  `alpha_LM`, plaquette, `u0`, `c2 = 1`, or `Z_match = 1`.
