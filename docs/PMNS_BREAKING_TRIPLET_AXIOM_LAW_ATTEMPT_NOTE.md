# PMNS Breaking Triplet Axiom Law Attempt

**Date:** 2026-04-15  
**Status:** strongest exact obstruction theorem for the global breaking
triplet `(delta, rho, gamma)` on the canonical PMNS branch  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_breaking_triplet_axiom_law_attempt.py`

## Question

Can the current exact bank derive a positive axiom-side law for the global
breaking triplet `(delta, rho, gamma)` itself?

If not, what is the strongest exact theorem about its zero locus, source
locus, or minimally missing source?

## Bottom line

No positive axiom-side value law is currently derivable.

The strongest exact theorem is a zero-locus / minimal-source statement:

- the global breaking triplet is exactly the 3-real complement of the
  aligned residual-`Z_2` Hermitian core
- its zero locus is exactly the aligned core on the canonical positive patch
- its source space is exactly the 3-dimensional real span of three
  independent Hermitian generators
- the current retained bank does not derive the breaking coefficients

So the current bank does not merely leave `(delta, rho, gamma)` unnamed. It
identifies their exact source sector and proves that the source sector has
dimension three.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS global Hermitian mode package`
- `PMNS EWSB residual-Z2 Hermitian core`
- `PMNS EWSB alignment nonforcing`
- `PMNS EWSB breaking-slot nonrealization`
- `PMNS right-conjugacy-invariant no-go`
- `PMNS intrinsic completion boundary`

The point is not to rederive a positive breaking law from those files. The
point is to sharpen the remaining obstruction to the exact minimal source
space.

## Exact global decomposition

On the canonical active PMNS branch, the Hermitian law is

`H = H_core + B(delta, rho, gamma)`

where the aligned residual-`Z_2` core is

`H_core = [[a, b, b], [b, c, d], [b, d, c]]`

with `a, b, c, d in R`, and the breaking matrix is

`B(delta, rho, gamma) = [[0, rho, -rho - i gamma], [rho, delta, 0], [-rho + i gamma, 0, -delta]]`.

The global breaking coordinates are exactly

`delta = (d_2 - d_3)/2`

`rho = (r_12 - r_31 cos phi)/2`

`gamma = r_31 sin phi`.

So the global active Hermitian law is not a generic seven-real object. It is
an exact `4 + 3` split:

- a four-real aligned core
- plus a three-real breaking sector

## Zero locus

The breaking triplet vanishes exactly when the aligned core is reached:

`B(delta, rho, gamma) = 0  <=>  delta = rho = gamma = 0`.

On the canonical full-rank positive patch, that is exactly the residual
`Z_2` locus:

- `d_2 = d_3`
- `r_12 = r_31`
- `phi = 0`

equivalently

`P_23 H P_23 = H`.

So the zero locus of the breaking triplet is exact, and it is the aligned
Hermitian surface already isolated by the residual-`Z_2` theorem.

## Source locus

The breaking sector is exactly the real span of three independent Hermitian
generators:

`E_delta = [[0, 0, 0], [0, 1, 0], [0, 0, -1]]`

`E_rho   = [[0, 1, -1], [1, 0, 0], [-1, 0, 0]]`

`E_gamma = [[0, 0, -i], [0, 0, 0], [i, 0, 0]]`

with

`B(delta, rho, gamma) = delta E_delta + rho E_rho + gamma E_gamma`.

These three generators are linearly independent over `R`, so the breaking
source locus has exact minimal dimension three.

That is the strongest exact source theorem currently available:

- the breaking triplet is not a single latent coefficient
- it is not a two-source correction
- it is exactly a three-source complement to the aligned core

## Theorem-level statement

**Theorem (Zero-locus and minimal-source theorem for the PMNS breaking
triplet).** Assume the exact global Hermitian mode package, the exact
residual-`Z_2` Hermitian core theorem, the exact EWSB alignment nonforcing
theorem, the exact EWSB breaking-slot nonrealization theorem, and the exact
right-conjugacy no-go / intrinsic-completion boundary results. Then:

1. the global active Hermitian law splits exactly as
   `H = H_core + B(delta, rho, gamma)`
2. the breaking triplet vanishes if and only if the aligned residual-`Z_2`
   core is reached
3. the breaking sector is exactly the 3-dimensional real span of
   `E_delta, E_rho, E_gamma`
4. the current retained bank does not derive the breaking coefficients
   `(delta, rho, gamma)` as axiom-side outputs
5. therefore the strongest exact theorem currently available is the
   zero-locus / minimal-source theorem, not a positive value law

## What this closes

This closes the ambiguity about the global breaking triplet.

It is now exact that:

- the breaking triplet has a unique three-generator source sector
- its zero locus is exactly the aligned residual-`Z_2` surface
- the current bank does not already contain a hidden axiom-side law fixing
  the breaking coefficients

## What this does not close

This note does **not** derive:

- the actual values of `(delta, rho, gamma)` from the axiom bank
- the selected-branch Hermitian data law itself
- the generic generic-breaking law on the non-aligned branch
- the residual selected-branch coefficient sheet

So this is an exact obstruction theorem, not a positive completion theorem.

## Safe wording

**Can claim**

- the global breaking triplet is exactly a 3-real source complement
- its zero locus is exactly the aligned residual-`Z_2` core
- the current bank does not derive a positive law for its coefficients

**Cannot claim**

- that the current bank already determines `(delta, rho, gamma)` as
  axiom-side outputs
- that the breaking triplet is a hidden one-parameter or two-parameter
  source
- that the full PMNS closure problem is solved positively

## Command

```bash
python3 scripts/frontier_pmns_breaking_triplet_axiom_law_attempt.py
```
