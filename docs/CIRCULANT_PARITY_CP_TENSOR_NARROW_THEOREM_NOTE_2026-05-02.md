# Hermitian Circulant Parity Decomposition + CP-Tensor Narrow Theorem

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the standalone linear-algebra identity that, on the
3-dimensional Hermitian-circulant family parametrized by `(d, c_even, c_odd)
∈ R^3` via `K = d I + c_even (S + S^2) + i c_odd (S - S^2)`, the residual-Z_2
transposition `P_{23}` swapping basis indices 2 and 3 sends `c_odd → -c_odd`
while leaving `d` and `c_even` invariant, and the (1,2)-entry CP-tensor
formula `Im[(K_{01})^2] = 2 c_even c_odd` holds exactly. This is purely a
fact of linear algebra on 3x3 matrices and the residual Z_2 transposition;
no DM-neutrino / Wilson-environment / weak-axis split / two-Higgs / standard
CP tensor readout authority is consumed.
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
Audit-lane ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_circulant_parity_cp_tensor_narrow.py`](./../scripts/frontier_circulant_parity_cp_tensor_narrow.py)
**Authority role:** Pattern A narrow rescope of the load-bearing class-(C)
algebraic core of [`DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15`](DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md).

## Statement

Let `S` be the 3x3 cyclic permutation matrix `S e_k = e_{k+1 mod 3}`, and
let `P_{23}` be the residual-Z_2 transposition matrix swapping basis
indices 2 and 3. Consider the 3-real-parameter Hermitian-circulant family

```text
K(d, c_even, c_odd)  =  d * I  +  c_even * (S + S^2)  +  i * c_odd * (S - S^2),
```

with `d, c_even, c_odd ∈ R`.

**Conclusion (T1).** `P_{23} S P_{23} = S^2` (and conversely
`P_{23} S^2 P_{23} = S`).

**Conclusion (T2).** Under conjugation by `P_{23}`, the basis matrices
transform as

```text
P_{23} I P_{23}              =  I,
P_{23} (S + S^2) P_{23}      =  S + S^2,
P_{23} [i (S - S^2)] P_{23}  =  -i (S - S^2).
```

Hence `d` and `c_even` are residual-Z_2-even coefficients on this basis,
while `c_odd` is residual-Z_2-odd.

**Conclusion (T3).** The CP-tensor of the (1, 2)-entry of `K` is

```text
Im[(K_{01})^2]  =  2 c_even c_odd,                                          (*)
```

exactly.

**Corollaries.**

- `c_odd = 0  ⇒  Im[(K_{01})^2] = 0` (CP vanishes on the even-only sector).
- `c_odd ≠ 0` and `c_even ≠ 0  ⇒  nonzero CP tensor`.

## Proof

`(T1)` Direct computation: `P_{23}` exchanges rows 2 and 3 (and columns
2 and 3). Applied to `S`, this exchanges the cycle direction, giving `S^2`.

`(T2)` Linearity plus `(T1)` gives the three identities. The `i` factor
on the antisymmetric basis stays fixed under the real conjugation `P_{23}
[\cdot] P_{23}^T`, but the underlying matrix `(S - S^2)` flips sign, so
the product flips sign overall.

`(T3)` Compute `K_{01}` directly:

```text
K_{01}  =  d * I_{01}  +  c_even * (S + S^2)_{01}  +  i * c_odd * (S - S^2)_{01}.
```

`I_{01} = 0`, `(S + S^2)_{01} = 1 + 0 = 1`, `(S - S^2)_{01} = 1 - 0 = 1`.
So `K_{01} = c_even + i c_odd`. Hence

```text
(K_{01})^2  =  (c_even + i c_odd)^2  =  c_even^2 - c_odd^2 + 2 i c_even c_odd,
Im[(K_{01})^2]  =  2 c_even c_odd.
```

The corollaries follow immediately. ∎

## What this claims

- `(T1)`: `P_{23} S P_{23} = S^2` exact.
- `(T2)`: parity decomposition of the basis `{I, S + S^2, i(S - S^2)}`.
- `(T3)`: `Im[(K_{01})^2] = 2 c_even c_odd` exact.
- Corollaries on CP-vanishing / non-vanishing.

## What this does NOT claim

- Does **not** identify `(d, c_even, c_odd)` with any specific physical
  Hermitian kernel. The narrow theorem treats them as abstract real
  symbols.
- Does **not** consume the upstream DM-neutrino circulant / weak-axis-1+2
  split / two-Higgs right-Gram / standard CP tensor readout authorities
  that the parent imports.
- Does **not** consume any PDG observed value, literature numerical
  comparator, fitted selector, or admitted unit convention.

## Relation to the parent DM neutrino odd-circulant Z_2 slot theorem

[`DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15`](DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md)
applies this circulant parity-decomposition + CP-tensor algebra to the
DM-neutrino-side Hermitian circulant kernel and identifies the unique
residual-Z_2-odd slot as the local coefficient that must be activated to
generate a nonzero CP tensor. Per the audit verdict on that row, the
DM-side authority-stack inputs (DM minimal Z_3 circulant CP tool,
two-Higgs right-Gram bridge, exact weak-axis 1+2 split, standard CP
tensor readout) are imported but not derived from retained primitives.

This narrow theorem isolates the underlying linear-algebra content from
the DM-side framing. The parity decomposition + CP-tensor formula can be
ratified independently of any DM-neutrino authority.

## Cited dependencies

None. This narrow note has zero ledger dependencies because it states
only elementary linear algebra on 3x3 Hermitian circulants and the
residual Z_2 transposition.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_circulant_parity_cp_tensor_narrow.py`](./../scripts/frontier_circulant_parity_cp_tensor_narrow.py)
verifies (PASS=14/0):

1. `S^3 = I`, `P_{23}^2 = I`.
2. `P_{23} S P_{23} = S^2` and `P_{23} S^2 P_{23} = S` exact.
3. `I` and `(S + S^2)` are Z_2-even; `(S - S^2)` is Z_2-odd; therefore
   `i(S - S^2)` is Z_2-odd under the real conjugation.
4. `K(d, c_even, c_odd)` is Hermitian; `P_{23} K P_{23}` sends
   `c_odd → -c_odd`.
5. `Im[(K_{01})^2] = 2 c_even c_odd` exact symbolic.
6. `c_odd = 0 ⇒ Im[(K_{01})^2] = 0` (CP-vanishing).
7. Concrete instance `(d, c_even, c_odd) = (1, 1/3, 1/5)` gives
   `Im[(K_{01})^2] = 2/15` exact.
8. Parent row's `load_bearing_step_class == 'C'` ledger check.

## Cross-references

- [`DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15`](DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md) —
  parent bundled note that applies this circulant parity-decomposition to
  the DM-neutrino-side Hermitian circulant kernel and identifies `c_odd`
  as the unique slot that must be activated to generate a nonzero CP
  tensor.
- [`audit_companion_dm_neutrino_odd_circulant_zero_law_exact.py`](./../scripts/audit_companion_dm_neutrino_odd_circulant_zero_law_exact.py) —
  Pattern B audit companion (cycle 32) that verifies the related
  `c_odd,current = 0` conclusion at exact precision on the DM-side
  current stack.
