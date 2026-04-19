# PMNS EWSB Residual-`Z_2` Spectral Primitive Reduction

**Date:** 2026-04-15  
**Status:** exact conditional reduction theorem on the EWSB-aligned active
Hermitian core  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_ewsb_residual_z2_spectral_primitive.py`

## Question

After the exact residual-`Z_2` Hermitian-core theorem reduces the active
aligned PMNS-producing Hermitian matrix to

```text
H_act =
[ a  b  b ]
[ b  c  d ]
[ b  d  c ],
```

can the current bank sharpen the four amplitudes `(a,b,c,d)` any further?

In particular, even if the Higgs / taste-condensate / `y_t` / flavor bank does
not yet derive them, is there a smaller exact primitive data set adapted to the
same aligned core?

## Bottom line

Yes.

On the exact even/odd basis supplied by the residual `2 <-> 3` symmetry, the
aligned core splits as

```text
[ a        sqrt(2) b   0   ]
[ sqrt(2)b  c + d     0   ]
[ 0        0         c - d ]
```

So the active aligned core is exactly equivalent to:

- one odd-sector eigenvalue
  `lambda_odd = c - d`
- two even-sector eigenvalues
  `lambda_+ >= lambda_-`
- one even-sector mixing angle
  `theta_even in [0, pi/2]`

Equivalently: fixing the aligned core is exactly fixing one `2 + 1` spectral
package:

- `3` nonnegative spectral invariants on the physical `H = Y Y^dag` lane
- plus `1` even-sector angle

So the strongest exact sharpening available today is:

`(a,b,c,d) <-> (lambda_+, lambda_-, lambda_odd, theta_even)`.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS EWSB residual-Z2 Hermitian core`

and nothing stronger. It is therefore a true sharpening of the already accepted
aligned-core surface, not a new bridge import from bounded Higgs or flavor
phenomenology.

## Exact spectral primitive data

Let

```text
H_act =
[ a  b  b ]
[ b  c  d ]
[ b  d  c ].
```

In the even/odd basis

- `e_1`
- `(e_2 + e_3)/sqrt(2)`
- `(e_2 - e_3)/sqrt(2)`

the core becomes

`B_even ⊕ [lambda_odd]`

with

```text
B_even =
[ a         sqrt(2) b ]
[ sqrt(2)b  c + d     ]
```

and

`lambda_odd = c - d`.

The two even-sector eigenvalues are therefore

`lambda_± = (a + c + d ± sqrt((a - c - d)^2 + 8 b^2)) / 2`.

Because `B_even` is real symmetric, on the generic patch `lambda_+ > lambda_-`
there is a unique angle `theta_even in [0, pi/2]` such that

`B_even = R(theta_even) diag(lambda_+, lambda_-) R(theta_even)^T`

with

`tan(2 theta_even) = 2 sqrt(2) b / (a - c - d)`.

## Exact inverse formulas

Conversely, from the primitive data

`(lambda_+, lambda_-, lambda_odd, theta_even)`

one reconstructs the aligned core exactly:

```text
a = lambda_+ cos^2(theta_even) + lambda_- sin^2(theta_even)
c + d = lambda_+ sin^2(theta_even) + lambda_- cos^2(theta_even)
b = (lambda_+ - lambda_-) sin(theta_even) cos(theta_even) / sqrt(2)
c = ((c + d) + lambda_odd) / 2
d = ((c + d) - lambda_odd) / 2
```

So the reduction is exact in both directions.

## Generic uniqueness and the degenerate locus

On the canonical aligned patch with

- `b >= 0`
- `lambda_+ >= lambda_-`

the primitive data are unique on the generic locus `lambda_+ > lambda_-`.

When the even block is degenerate,

`lambda_+ = lambda_-`,

the angle `theta_even` ceases to be physical. That happens exactly when

- `b = 0`
- `a = c + d`

so the even block is proportional to the identity.

Therefore the only loss of uniqueness is the expected nongeneric degeneracy
locus of the even block.

## Search outcome versus the Higgs / flavor bank

The current search through the Higgs / taste-condensate / `y_t` / flavor bank
does **not** supply a stronger exact law for these primitives.

What the current bank gives is:

- exact weak-axis / residual-`Z_2` alignment as a conditional symmetry surface
- exact reduction of the active Hermitian data from seven coordinates to the
  four-real aligned core
- exact selector-bank and flavor-bank boundary theorems saying the current
  Higgs/flavor toolkit still does not bridge to the PMNS selector or branch
  invariants

So this note is the strongest clean sharpening currently available:

- not a derivation of the primitive values
- but an exact reduction of the missing data to one `2 + 1` spectral package

## The theorem-level statement

**Theorem (Spectral primitive reduction of the aligned residual-`Z_2`
Hermitian core).** Assume the exact PMNS EWSB residual-`Z_2` Hermitian-core
theorem. Then on the aligned active branch:

1. the odd vector `(0,1,-1)/sqrt(2)` is an exact eigenvector with eigenvalue
   `lambda_odd = c - d`
2. the remaining data lie in the real symmetric even block
   `[[a, sqrt(2)b], [sqrt(2)b, c + d]]`
3. on the generic locus `lambda_+ > lambda_-`, the aligned core is exactly and
   uniquely encoded by the primitive data
   `(lambda_+, lambda_-, lambda_odd, theta_even)` with
   `theta_even in [0, pi/2]`
4. the inverse formulas above reconstruct `(a,b,c,d)` exactly

Therefore the aligned active Hermitian core is not merely a four-amplitude
object. It is exactly one `2 + 1` spectral package: three spectral invariants
plus one even-sector angle.

## What this closes

This closes the next exact reduction question on the aligned core.

It is now exact that:

- the aligned core is sharper than just “four free real amplitudes”
- its natural primitive data are adapted to the exact `2 + 1` split
- any future exact derivation can target these spectral primitives instead of
  the raw matrix entries

## What this does not close

This note does **not** derive:

- the alignment condition itself from the current bank
- the primitive values
  `(lambda_+, lambda_-, lambda_odd, theta_even)`
- a Higgs / taste / `y_t` / flavor bridge fixing those values

It is an exact reduction theorem only.

## Safe wording

**Can claim**

- on the EWSB-aligned residual-`Z_2` surface, the active Hermitian core is
  exactly equivalent to three spectral invariants plus one even-sector angle
- the odd eigenvalue is exactly `c - d`
- the even block carries the remaining two eigenvalues and one mixing angle

**Cannot claim**

- the current Higgs or flavor bank already derives those primitives
- the four aligned-core quantities are numerically closed

## Command

```bash
python3 scripts/frontier_pmns_ewsb_residual_z2_spectral_primitive.py
```
