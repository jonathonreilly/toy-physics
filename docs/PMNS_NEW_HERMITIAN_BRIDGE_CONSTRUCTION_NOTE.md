# PMNS New Hermitian Bridge Construction

**Date:** 2026-04-15  
**Status:** minimal extension theorem for the branch Hermitian-data bridge on
the canonical PMNS branch  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_new_hermitian_bridge_construction.py`

## Question

Starting from the exact global `2 + 2 + 3` package for the active Hermitian
law, what is the smallest new axiom-side bridge that would actually produce
the branch Hermitian data?

If the current bank cannot derive a positive value law, what is the exact
minimal missing bridge object?

## Bottom line

The current bank still does **not** derive a positive axiom-side value law
for the branch Hermitian data.

But the exact minimal bridge object is now identified sharply.

The smallest honest Hermitian bridge class is the selected-branch Hermitian
data package

`B_H,min = (A, B, u, v, delta, rho, gamma)`,

with the optional discrete coefficient-closure bit

`e in {0,1}`

only if full canonical coefficient closure is also required on the compatible
weak-axis seed patch.

This is not a hidden lower-dimensional law. It is the exact coordinate bridge
already forced by the current sector decomposition:

- weak-axis seed pair `(A, B)`
- aligned deformation pair `(u, v)`
- breaking triplet `(delta, rho, gamma)`

So the branch Hermitian-data bridge is exactly the selected-branch
Hermitian-data law itself, with one extra binary seed-edge selector only if
coefficient closure is part of the target.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS global Hermitian mode package`
- `PMNS intrinsic completion boundary`
- `PMNS EWSB residual-Z2 Hermitian core`
- `PMNS EWSB weak-axis Z3 seed`
- `PMNS EWSB weak-axis seed coefficient closure`
- `PMNS EWSB weak-axis seed edge-selector reduction`
- `PMNS breaking triplet axiom law attempt`
- `PMNS branch Hermitian data law attempt`

The point is not to discover a smaller package than these exact source
sectors. The point is to show that the current bank already isolates the
smallest bridge class that could possibly produce branch Hermitian data.

## Exact constructive bridge

On the canonical active PMNS branch,

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i phi}) C`,

the Hermitian law

`H = Y Y^dag`

splits exactly as

`H = H_core + B(delta,rho,gamma)`

with

`H_core = [[a,b,b],[b,c,d],[b,d,c]]`

and

`B(delta,rho,gamma) = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`.

The aligned core is exactly the `2 + 2` package:

- weak-axis seed pair `(A,B)`
- aligned deformation pair `(u,v)`

with the exact reconstruction rule

`lam_plus = A`

`lam_odd  = B`

`lam_minus = B + u`

`theta_even = arctan(sqrt(2)) + v`.

The aligned core is then reconstructed from the exact `2 + 1` spectral
primitive data

`(lambda_+, lambda_-, lambda_odd, theta_even)`

via the fixed even/odd basis.

So the full Hermitian bridge is exactly:

- `2` weak-axis seed coordinates
- `2` aligned deformation coordinates
- `3` breaking coordinates

and therefore exactly `2 + 2 + 3`.

## Minimality

This bridge is minimal in the exact sense available from the current bank:

- the aligned core has exact real rank `4`
- the breaking sector has exact real rank `3`
- together they span the full active Hermitian grammar of rank `7`
- the current bank does not collapse those seven continuous coordinates to a
  smaller continuous source

So there is no smaller continuous Hermitian bridge than the `2 + 2 + 3`
package itself.

If coefficient closure is also required, the remaining seed-patch ambiguity is
one independent binary edge bit:

- `Y = sqrt(A) I` on one monomial edge
- `Y = sqrt(A) C` on the other

equivalently the restricted Higgs-offset choice on the canonical `(0,1)`
pair.

That bit is not continuous and cannot be absorbed into the `2 + 2 + 3`
Hermitian package.

## Theorem-level statement

**Theorem (Minimal Hermitian bridge class for branch data).** Assume the exact
global Hermitian mode package, the exact intrinsic-completion boundary, the
exact weak-axis seed theorem, the exact weak-axis seed coefficient-closure
theorem, the exact weak-axis seed edge-selector reduction theorem, the exact
breaking-triplet axiom-law attempt, and the exact branch Hermitian-data-law
attempt. Then:

1. the global active Hermitian law is exactly a `2 + 2 + 3` package
2. the smallest continuous bridge object that could produce branch Hermitian
   data is exactly `B_H,min = (A, B, u, v, delta, rho, gamma)`
3. the current retained bank does not derive those branch values as
   axiom-side outputs
4. if canonical coefficient closure is also required, one additional binary
   seed-edge selector `e in {0,1}` is required on the compatible weak-axis
   seed patch
5. therefore the exact minimal missing bridge object is the selected-branch
   Hermitian-data law itself, with the optional seed-edge selector attached
   only when coefficient closure is part of the target

So the current bank does not reveal a smaller hidden bridge. It reveals the
exact minimal one.

## What this closes

This closes the ambiguity about the smallest possible Hermitian bridge class.

It is now exact that the branch-Hermitian problem is not:

- a generic seven-real fit
- a hidden lower-dimensional source law
- a right-conjugacy-invariant observable of `K = Y^dag Y`

It is the exact `2 + 2 + 3` branch bridge, with one optional binary edge bit
if coefficient closure is demanded.

## What this does not close

This note does **not** derive:

- the actual axiom-side values of `(A, B, u, v, delta, rho, gamma)`
- the aligned deformation law as a positive output of the axiom bank
- the breaking-triplet values as positive outputs of the axiom bank
- the restricted Higgs-offset selector itself

So this is a minimal-extension theorem, not a positive completion theorem.

## Command

```bash
python3 scripts/frontier_pmns_new_hermitian_bridge_construction.py
```
