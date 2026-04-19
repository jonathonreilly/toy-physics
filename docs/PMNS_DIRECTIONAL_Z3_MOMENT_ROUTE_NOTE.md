# PMNS Directional `Z_3^3` Moment Route

**Date:** 2026-04-16  
**Status:** exact native moment-route result on the microscopic lepton lane  
**Script:** `scripts/frontier_pmns_directional_z3_moment_route.py`

## Question

Can the native directional `Z_3^3` / generation-orbit moment algebra fix the
remaining microscopic PMNS data on the lepton lane, starting from the `Cl(3)`
on `Z^3` carrier and using only orbit moments?

## Bottom line

This route fixes a useful subset exactly:

- the passive monomial offset `q`
- the active/passive sector orientation bit `tau`

But the same moment algebra does **not** fix the full active five-real
corner-breaking source. It is blind to distinct off-seed source data that share
the same directional moments.

So the route is native and exact on the passive/orientation side, but it does
not close the full microscopic lepton pair.

## What is fixed exactly

The directional moment vector is

`m_r(D) = tr(D P_r^\dagger),  r = 0,1,2`,

with `P_r` the three `Z_3` permutation supports.

For a passive monomial lane

`D_passive = diag(a_1,a_2,a_3) P_q`,

exactly one moment survives. That surviving index is the passive offset `q`,
and its value is the passive coefficient sum `a_1 + a_2 + a_3`.

For a one-sided minimal PMNS pair, the active block has two surviving
directional moments while the passive block has one. So the same moment algebra
also reads off the sector orientation bit `tau`.

## What is not fixed

The active corner source

`(xi_1, xi_2, eta_1, eta_2, delta)`

is not fixed by these moments. Two distinct active operators can have identical
directional moment vectors while differing in the zero-sum breaking
coordinates.

So this route does not determine the generic off-seed active microscopic law.

## Interpretation

This is a genuine native reduction theorem, not a packaging theorem:

- passive monomial data are recoverable from directional moments
- the sector orientation bit is recoverable from moment support pattern
- the active five-real source remains in the kernel of this moment algebra

That means the directional `Z_3^3` moment route is useful, but it is not the
final closure theorem.

## Verification

```bash
python3 scripts/frontier_pmns_directional_z3_moment_route.py
```

Expected result:

```text
PASS=17  FAIL=0
```
