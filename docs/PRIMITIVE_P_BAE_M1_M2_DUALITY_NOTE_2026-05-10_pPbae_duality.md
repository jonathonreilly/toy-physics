# P-BAE M1/M2 Candidate Duality - Narrow Bounded Theorem

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status:** source-note proposal; independent audit owns audit verdict and
pipeline-derived effective status.
**Scope:** finite algebra on the `C_3`-equivariant Hermitian circulant
`H = a I + b C + conj(b) C^2`.
**Primary runner:** [`scripts/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.py`](../scripts/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.py)
**Cache:** [`logs/runner-cache/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.txt`](../logs/runner-cache/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.txt)

## Claim

Let

```
H = a I + b C + conj(b) C^2
E_plus = ||pi_plus(H)||_F^2 = 3 a^2
E_perp = ||pi_perp(H)||_F^2 = 6 |b|^2
```

on the finite `C_3`-circulant model. The branch's candidate M1/M2
comparison has the following bounded content:

1. The literal linear trace-state expression
   `tau_M(H) = Tr(pi_plus(H)) + Tr(pi_perp(H))` degenerates to
   `Tr(H) = 3a` for every such `H`; it cannot distinguish the
   one-dimensional trivial block from the two-real-dimensional doublet.
2. The non-linear equal block-log functional
   `L(E_plus,E_perp) = log(E_plus) + log(E_perp)`, constrained by
   `E_plus + E_perp = N`, has its unique interior stationary point at
   `E_plus = E_perp = N/2`.
3. Translating `E_plus = E_perp` through the displayed Frobenius
   identities gives the Brannen amplitude equipartition condition
   `|b|^2/a^2 = 1/2`.
4. A half-scaled saddle/action variant has the same stationary point
   and a Hessian smaller by a factor of two in the energy coordinate.
   Thus the two candidate descriptions are saddle-equivalent for this
   finite calculation, but they are not identical fluctuation measures.

## Boundary

This note does not elect a primitive, close the Brannen amplitude
equipartition condition from the framework, modify a parent theorem, or add
an axiom. In particular, the bare reduced coordinate measure `dr_plus d|b|`
does not select the BAE point by itself; the selection enters only after a
separate equal block-log saddle/action is supplied.

The result is useful as a design guard: future work may cite the finite
calculation to avoid treating the literal trace expression as the
load-bearing M1 primitive, and to keep saddle equivalence separate from full
measure equivalence.

## Import And Support Inventory

The calculation is zero-input finite algebra. It uses no measured values, no
PDG values, no fitted constants, and no external physics normalization. The
symbols `a`, `b`, and `N` are internal variables of the finite model.

## Runner Checks

The paired runner verifies:

- the `C_3` circulant identities and Frobenius block energies;
- the degeneracy of the literal trace-state expression;
- the stationary point of the equal block-log functional;
- the equivalence between `E_plus = E_perp` and `|b|^2/a^2 = 1/2`;
- the constant factor-two Hessian distinction for the half-scaled variant;
- that the branch does not promote a retained-grade or empirical claim.
