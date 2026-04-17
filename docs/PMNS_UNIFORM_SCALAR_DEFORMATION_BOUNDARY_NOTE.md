# PMNS Uniform Scalar Deformation Boundary

**Date:** 2026-04-16  
**Status:** exact negative extension theorem  
**Script:** `scripts/frontier_pmns_uniform_scalar_deformation_boundary.py`

## Question

If we move beyond the sole-axiom free point by admitting the repo's
translation-invariant local scalar / Coleman-Weinberg deformation route, does
that generate a nontrivial retained PMNS lower-level response profile?

## Answer

No.

On the retained lepton `hw=1` triplets, a **uniform local scalar condensate**
is generation-blind. The most general retained microscopic pair on that lane is

`D_0^trip = u_0 I_3`,

`D_-^trip = u_- I_3`,

for real sector scalars `u_0, u_-`.

The induced lower-level response profiles are therefore just scalar resolvent
column sets, and the live retained PMNS closure stack rejects them exactly.

So even the admitted uniform scalar / Coleman-Weinberg deformation route does
**not** by itself realize the retained PMNS lane.

## Exact chain

### 1. Uniform scalar condensate keeps the `hw=1` triplet scalar

For the exact staggered unit-cell Hamiltonian with a uniform parity-coupled
scalar deformation `phi`,

`H(K, phi)^2 = -(1 + phi^2) I_8`

at each `hw=1` corner `K`.

Therefore each `hw=1` corner has the same positive energy

`E_X(phi) = sqrt(1 + phi^2)`,

so the uniform scalar condensate does not split or mix the three generation
corners. It only renormalizes their common scalar value.

### 2. Sector-scalar retained pair

Allowing for sector-dependent matching on the retained lepton surface, the most
general pair induced by such a uniform generation-blind scalar lane is

`(D_0^trip, D_-^trip) = (u_0 I_3, u_- I_3)`.

There is no active support `I + C`, no corner-breaking source, and no one-sided
minimal PMNS structure hiding inside this family.

### 3. Scalar lower-level response profiles

For a scalar active block `u_0 I_3`, the active lower-level response profile is

`R_act = (I - lambda_act (u_0 - 1) I)^(-1) = 1 / (1 - lambda_act (u_0 - 1)) I_3`.

For a scalar passive block `u_- I_3`, the passive lower-level response profile
is

`R_pass = (I - lambda_pass u_- I)^(-1) = 1 / (1 - lambda_pass u_-) I_3`.

So both response profiles are again scalar column sets.

### 4. Retained PMNS closure rejects the scalar lane

The retained PMNS lower-level closure stack requires a **one-sided minimal PMNS
class**: exactly one sector must carry the non-monomial active support.

But for the scalar family:

- both sectors stay scalar/diagonal
- neither sector carries the canonical active support
- the active four-real source vanishes identically

Hence the scalar lane cannot realize retained PMNS.

## Consequence

This is stronger than the sole-axiom free-point theorem.

The earlier boundary said:

> the sole axiom gives only the trivial free response profiles.

This note strengthens that to:

> even the admitted translation-invariant uniform scalar / Coleman-Weinberg
> deformation route only rescales the free point and still does not generate
> retained PMNS structure.

So the remaining open lane, if one wants a positive PMNS completion, is not a
uniform scalar condensate law. It would have to be a genuinely non-scalar
deformation on the retained lepton triplets.

## Boundary

This note closes only the **uniform scalar** extension route on the retained
PMNS lane.

It does **not** rule out:

- a nonuniform / corner-sensitive deformation law,
- a route that leaves the retained one-sided minimal class,
- or a different extension of the microscopic lepton dynamics.

## Command

```bash
python3 scripts/frontier_pmns_uniform_scalar_deformation_boundary.py
```
