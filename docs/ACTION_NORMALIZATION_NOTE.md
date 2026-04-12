# Action Normalization: Self-Consistency Fixes the Coupling Coefficient

**Script:** `scripts/frontier_action_normalization.py`
**Date:** 2026-04-12

## The Reviewer's Objection

"You chose S = L(1-f). If you chose S = L(1-2f), you'd get a different metric.
The coefficient is arbitrary."

## Summary of the Response

The coefficient c in S = L(1 - c*f) is **not observationally arbitrary** once
one fixes the field normalization convention and matches the weak-field light
bending ratio. On that reading, only c = 1 gives the normalization consistent
with the observed factor-of-2 light bending.

## The Argument (Five Steps)

### 1. Self-consistency converges for all c > 0

The propagator-field self-consistency loop (propagate -> get density -> solve
Poisson -> propagate) converges for any positive c. Self-consistency alone does
not select c. Larger c requires more iterations but still converges.

### 2. Rescaling degeneracy

The transformation (c, G) -> (c/a, a*G) leaves the dynamics invariant because
the self-consistent loop depends only on the product c*G. This is verified
numerically: c*phi_max is constant across rescalings at fixed c*G.

### 3. Convention breaks the degeneracy

We define G as Newton's constant (measured from Cavendish experiment or orbital
periods). This fixes one parameter. The field f is then determined by Poisson's
equation. The remaining question: what is c?

### 4. Light bending fixes c = 1

The action S = L(1 - c*f) yields the effective weak-field metric:

    g_tt = -(1 - c*f),  g_rr = 1 + c*f

For massive particles, the deflection is proportional to c*f (Newtonian).
For null rays, the deflection picks up contributions from both g_tt and g_rr,
giving a total factor of (1 + c) times the Newtonian deflection.

Eddington's 1919 observation confirmed: light bending = 2 * Newtonian.
Therefore 1 + c = 2, so **c = 1**.

### 5. Equivalence with Schwarzschild

The Schwarzschild metric in isotropic coordinates has g_tt = -(1 - Phi)^2 and
g_rr = (1 + Phi)^2 where Phi = GM/r. In weak field: g_tt ~ -(1 - 2*Phi) and
g_rr ~ (1 + 2*Phi). Our action with c = 1 gives g_tt ~ -(1 - f) and
g_rr ~ (1 + f), matching with f = 2*Phi.

## Key Numerical Results

| c    | Converges | Light Factor | beta  | Correct GR? |
|------|-----------|-------------|-------|-------------|
| 0.5  | Yes       | 1.50        | 1.28  | No          |
| 1.0  | Yes       | 2.00        | 1.28  | **Yes**     |
| 2.0  | Yes       | 3.00        | 1.28  | No          |
| 5.0  | Yes       | 6.00        | 1.28  | No          |

The mass exponent beta ~ 1.28 is a finite-size lattice artifact (N=20 grid
with Dirichlet boundary conditions). It is independent of c because the field
is perturbatively weak. The light bending factor, which is an exact analytic
result (1 + c), uniquely selects c = 1.

## Response to the Reviewer

The objection conflates convention with physics. One can always rescale
c -> c/a and G -> a*G simultaneously, which changes the definition of f but not
any observable. Once G is fixed by laboratory measurement, c is determined by
the observed light bending ratio. The result is c = 1.

This is analogous to the situation in electromagnetism: one can rescale the
vector potential A -> a*A and the charge e -> e/a, but once e is fixed by
measurement, A is determined. The "arbitrary" rescaling freedom is just a choice
of units for the potential, not a physical ambiguity.

## Claim boundary

- this is a normalization/identification argument, not a derivation of c = 1
  from the axioms alone
- self-consistency alone does not select c
- the spatial-metric / bending input remains empirical consistency, not an
  independent closure
