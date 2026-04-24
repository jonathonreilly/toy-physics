# Planck-Scale Boundary Action Source Versus Pressure Classification Theorem

**Date:** 2026-04-23
**Status:** terminology and object-class hardening theorem
**Verifier:** `scripts/frontier_planck_boundary_action_source_vs_pressure_classification_theorem.py`

## Question

Does the Planck lane prove

`p_phys = Tr(rho_cell P_A)`

as the ordinary scalar Schur boundary pressure?

## Result

No.

The branch must not use the word "pressure" without specifying the object
class. There are three different same-surface quantities:

1. the additive scalar Schur vacuum observable

   `p_scalar(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

2. the normal-ordered Schur boundary action-source density

   `p_action = nu - lambda_min(L_Sigma)`;

3. the primitive event insertion source density

   `p_event = d/ds log Tr(rho_cell exp(s P_A))|_(s=0)
            = Tr(rho_cell P_A)`.

The observable-principle pressure note already proves that the first quantity
is the scalar Schur observable. It is not `1/4` on the rational witness.

The Planck lane does something different. It identifies the second and third
quantities on the retained primitive boundary-action object class:

`p_action = p_event`.

Thus the safe object is not "scalar boundary pressure." It is the
normal-ordered primitive boundary action-source density.

## Theorem 1: scalar Schur pressure is not the Planck quarter

On the Schur boundary carrier, multiplicative partition factorization and
scalar additivity select

`p_scalar(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

For the rational witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

we have

`n = 2`,

`det(L_Sigma) = 5/3`,

so

`p_scalar = (1/4) log(5/3)`.

This is not `1/4`.

Therefore exact Planck closure is false if one insists that the physical
readout must be the additive scalar Schur free-energy observable.

## Theorem 2: the Planck readout is an action-source density

The Schur action family has generator

`G_nu = nu I - L_Sigma`.

After the exact Schur floor is removed, the one-cell boundary action-source
density is

`p_action = sup spec(G_nu) = nu - lambda_min(L_Sigma)`.

This is not the scalar Schur vacuum free energy. It is the normal-ordered
growth/source coefficient of the boundary action family.

The primitive event source gives the finite insertion group

`U_A(s) = exp(s P_A)`,

with normalized generator

`p_event = d/ds log Tr(rho_cell U_A(s))|_(s=0)`.

Since `P_A` is a projector,

`p_event = Tr(rho_cell P_A)`.

On the source-free primitive cell,

`rho_cell = I_16 / 16`,

and `rank(P_A) = 4`, hence

`p_event = 1/4`.

## Theorem 3: parent-source equivalence is the only bridge being claimed

The parent-source theorem identifies the Schur action-source representation
and the event insertion representation as reductions of one parent primitive
boundary source:

`B_parent = (H_A, P_A)`.

Under that object-class commitment,

`p_action = p_event = Tr(rho_cell P_A)`.

This does not imply

`p_scalar = p_event`.

It implies only that the normal-ordered boundary action-source density equals
the primitive event-source density.

## Consequence

The reviewer-facing Planck claim must be:

> The primitive boundary action-source density is `1/4`, and standard
> gravitational area/action normalization then gives `a = l_P`.

It must not be:

> The ordinary scalar Schur pressure is `1/4`.

If a reviewer defines physical pressure exclusively as the scalar Schur
free-energy observable, the Planck lane should concede that this route does not
close. If the reviewer accepts the retained primitive gravitational
boundary-action object class, the event/source route remains the active Planck
closure.

## Safe Claim

Use:

> The Planck lane reads `Tr(rho_cell P_A)` as a normal-ordered primitive
> boundary action-source density, not as the scalar Schur free-energy pressure.
> The scalar Schur pressure is `(1/(2n)) log det(L_Sigma)` and is not the
> Planck quarter.

Do not use:

> The observable-principle scalar boundary pressure equals `1/4`.

Do not use:

> `p_scalar = Tr(rho_cell P_A)`.
