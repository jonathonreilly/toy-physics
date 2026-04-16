# PMNS Branch Hermitian Data Law Attempt

**Date:** 2026-04-15  
**Status:** exact obstruction theorem for the branch Hermitian-data law;
the current atlas/axiom bank does not yet derive the branch values as
axiom-side outputs  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_branch_hermitian_data_law_attempt.py`

## Question

The current PMNS package now knows three things exactly:

1. the global active Hermitian law sectorizes into a real aligned core plus a
   three-real breaking triplet
2. the compatible weak-axis seed patch collapses to one exchange sheet and
   then to the restricted Higgs-offset selector on the canonical `(0,1)` pair
3. the selected-branch Hermitian inverse problems are exact once a branch is
   selected

But does the current atlas/axiom bank already derive the branch Hermitian-data
law itself?

## Bottom line

No positive axiom-side derivation is available from the current bank.

What the current bank does give is an exact, atlas-safe decomposition of the
branch Hermitian law into three layers:

- the global active Hermitian law is exactly a `2 + 2 + 3` package
- the aligned residual-`Z_2` core is exactly a `2 + 2` package
- the compatible weak-axis seed patch then collapses to one exchange sheet,
  and at `A = B` that sheet is exactly the restricted Higgs-offset /
  monomial-edge selector on the canonical `(0,1)` pair

So the branch Hermitian-data law is now identified exactly as a package, but
the package values are still not axiom-side outputs.

## Exact structure already available

On the canonical active branch,

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i phi}) C`

the Hermitian law `H = Y Y^dag` admits the exact decomposition

`H = H_core + B(delta,rho,gamma)`

with

`H_core = [[a,b,b],[b,c,d],[b,d,c]]`

and

`B(delta,rho,gamma) = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`.

Equivalently, the global branch Hermitian law is exactly:

- weak-axis seed pair `(A,B)`
- aligned deformation pair `(u,v)`
- breaking triplet `(delta,rho,gamma)`

That is the exact global `2 + 2 + 3` package.

The aligned surface is the vanishing of the triplet:

`delta = rho = gamma = 0`.

On that surface, `H_core` is exactly the four-real residual-`Z_2` core
`[[a,b,b],[b,c,d],[b,d,c]]`, and the weak-axis seed subcone further sharpens it
to the seed pair plus aligned deformations.

## The seed-patch selector is still discrete

On the compatible weak-axis seed patch `A <= 4B`, the canonical active
coefficients close to

`Y_+ = x_+ I + y_+ C`

and

`Y_- = y_+ I + x_+ C`.

At the equal-split edge `A = B`, those two sheets limit exactly to the two
one-Higgs monomial edges

`sqrt(A) I` and `sqrt(A) C`.

So the remaining seed-patch ambiguity is exactly the restricted Higgs-offset /
monomial-edge selector on the canonical `(0,1)` pair.

## What the current bank does not derive

The current retained bank does **not** derive:

- the selected-branch Hermitian data themselves as axiom-side outputs
- the aligned-core values `(A,B,u,v)` from the axiom bank
- the breaking-triplet values `(delta,rho,gamma)` from the axiom bank
- the restricted Higgs-offset selector on the canonical `(0,1)` pair

The current bank therefore does not contain a hidden lower-dimensional route
that would collapse the branch Hermitian law to fewer outputs.

This is visible in the exact boundary results already on the bank:

- aligned and generic full-rank points coexist on the same canonical support
  class while carrying different breaking-triplet vectors
- the current bank does not force EWSB alignment
- the current bank does not derive the breaking-slot vector
- the current bank does not fix the seed-edge selector

## Minimal missing bridge

The minimal missing object is therefore a single axiom-side bridge that
produces the branch Hermitian data as an exact package:

1. the selected-branch Hermitian values `H_core` and `B(delta,rho,gamma)`
2. if coefficient closure is also required, the residual seed-edge selector on
   the compatible weak-axis patch

Equivalently: the missing datum is not a hidden texture parameter. It is the
selected-branch Hermitian-data law itself.

## Theorem-level statement

**Theorem (Exact branch Hermitian-data obstruction and minimal bridge).**
Assume the exact global Hermitian mode package, the exact EWSB alignment
nonforcing theorem, the exact breaking-slot nonrealization theorem, the exact
weak-axis seed coefficient-closure theorem, and the exact weak-axis seed
edge-selector reduction theorem. Then:

1. the global active Hermitian law is exactly a `2 + 2 + 3` package
2. the aligned residual-`Z_2` surface is exactly the vanishing of the breaking
   triplet `(delta,rho,gamma)`
3. the compatible weak-axis seed patch closes to one exchange sheet, and at
   `A = B` that sheet is exactly the restricted Higgs-offset /
   monomial-edge selector on the canonical `(0,1)` pair
4. the current retained bank still does not derive the branch Hermitian-data
   values themselves as axiom-side outputs
5. therefore the minimal missing bridge is the selected-branch Hermitian-data
   law, together with the seed-edge selector if full coefficient closure is
   also required

So there is no positive branch Hermitian-data derivation from the current
bank, but there is now an exact obstruction theorem that identifies the
smallest missing object.

## What this closes

This closes the ambiguity around the branch Hermitian target.

It is now exact that the remaining object is not:

- a generic seven-number fit
- a hidden lower-dimensional selector
- a right-conjugacy-invariant observable of `K = Y^dag Y`

It is the branch Hermitian-data law itself.

## What this does not close

This note does **not** derive:

- the branch Hermitian-data values from the axiom bank
- the generic breaking-triplet values from the axiom bank
- the restricted Higgs-offset selector from the current stack

So the branch Hermitian-data law remains open as a positive derivation.

## Command

```bash
python3 scripts/frontier_pmns_branch_hermitian_data_law_attempt.py
```
