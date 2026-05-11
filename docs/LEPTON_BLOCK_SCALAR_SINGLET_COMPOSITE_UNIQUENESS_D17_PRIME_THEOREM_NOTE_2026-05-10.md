# Lepton-Block Scalar-Singlet Composite Uniqueness

**Date:** 2026-05-10
**Legacy lane label:** D17-prime
**Type:** bounded_theorem
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This source note proposes a bounded structural theorem and
does not assign retained status.

**Primary runner:** [`scripts/frontier_lepton_block_scalar_singlet_composite_uniqueness.py`](../scripts/frontier_lepton_block_scalar_singlet_composite_uniqueness.py)
**Cached output:** [`logs/runner-cache/frontier_lepton_block_scalar_singlet_composite_uniqueness.txt`](../logs/runner-cache/frontier_lepton_block_scalar_singlet_composite_uniqueness.txt)

## Claim

Given the charged-lepton Yukawa-shaped block

```text
bar L_L^alpha  H_alpha  e_R,
```

with `L_L` and `H` SU(2) doublets, `e_R` an SU(2) singlet, all three color
singlets, and the doubled-hypercharge assignment

```text
Y(L_L) = -1,   Y(H) = +1,   Y(e_R) = -2,
```

the unique color-singlet, SU(2)-singlet, Lorentz-scalar,
hypercharge-conserving contraction on this block is

```text
H_unit^lep = (1/sqrt(2)) sum_{alpha=1,2} bar L_L^alpha H_alpha e_R.
```

The normalization is

```text
Z_lep^2 = N_c N_iso = 1 * 2 = 2,
```

so the unit coefficient is `1/sqrt(2)`.

## Proof

The color part is trivial: `L_L`, `H`, and `e_R` are color singlets, so there
is no color alternative to contract.

For weak isospin, `bar L_L` is in the antifundamental and `H` is in the
fundamental. The tensor product `2bar x 2` decomposes as

```text
2bar x 2 = 1 + 3.
```

The singlet is the natural Kronecker pairing

```text
sum_alpha bar L_L^alpha H_alpha.
```

The triplet is the Pauli insertion `bar L_L sigma^a H`. It is not a scalar
unless an additional SU(2) triplet object is supplied. The stated block has
only the singlet `e_R`; it contains no `e_R^a` triplet or other triplet field
that could absorb the adjoint index. Therefore the triplet channel is outside
the stated Yukawa-shaped block.

Hypercharge selects the same monomial:

```text
bar L_L H e_R:        -Y(L_L) + Y(H)       + Y(e_R) = +1 + 1 - 2 = 0
bar L_L tilde H e_R:  -Y(L_L) + Y(tilde H) + Y(e_R) = +1 - 1 - 2 = -2
```

Thus `bar L_L H e_R` is allowed and the `tilde H` variant is rejected on this
charged-lepton block.

Finally, the normalized singlet sums over two weak-isospin components and one
color component. With an orthonormal component basis,

```text
(1/Z_lep^2) sum_{alpha,beta} <O_alpha | O_beta>
  = (1/2) * 2
  = 1.
```

This proves the bounded statement.

## Relation to Existing Rows

The result is the lepton-block analog of the scalar-singlet normalization step
used in the top-Yukawa source note `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`,
but the comparison is not a retained-status claim. The lepton block is simpler
than the quark block because `N_c=1` and no color alternatives exist.

The hypercharge bookkeeping is the same convention used by
[`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md).

## Non-Claims

This note does not claim:

- a charged-lepton Ward identity;
- a lepton mass or Yukawa-value prediction;
- a closure of any charged-lepton mass-retention lane;
- an SU(2) Fierz analog for the lepton block;
- tree-level Feynman-rule completeness for lepton exchange diagrams;
- any update to an unlanded or unaudited parent theorem.

It only establishes the bounded scalar-singlet composite and its `Z_lep^2=2`
normalization under the stated block inputs.

## Falsifiers

The row is falsified if any of the following is shown inside the same block
scope:

1. an additional SU(2)-singlet, Lorentz-scalar, hypercharge-conserving
   contraction independent of `sum_alpha bar L_L^alpha H_alpha e_R`;
2. an SU(2)-triplet right-handed charged-lepton field or other triplet carrier
   admitted into the block;
3. a correction to the doubled-hypercharge convention that makes the `tilde H`
   monomial gauge-allowed for charged leptons.

## Audit Metadata

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: |
  Conditional on the stated charged-lepton Yukawa block inputs
  (L_L and H SU(2) doublets, e_R an SU(2) singlet, all color singlets,
  and doubled hypercharges Y(L_L)=-1, Y(H)=+1, Y(e_R)=-2), the unique
  color-singlet, SU(2)-singlet, Lorentz-scalar, hypercharge-conserving
  contraction is (1/sqrt(2)) sum_alpha bar L_L^alpha H_alpha e_R, with
  Z_lep^2 = 2.
upstream_dependencies:
  - charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26
admitted_context_inputs:
  - charged-lepton Yukawa block representation content
  - SU(2) 2bar x 2 = 1 + 3 decomposition
```
