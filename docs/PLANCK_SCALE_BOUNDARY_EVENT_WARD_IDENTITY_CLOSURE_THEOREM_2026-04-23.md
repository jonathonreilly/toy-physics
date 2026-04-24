# Planck-Scale Boundary Event Ward Identity Closure Theorem

**Date:** 2026-04-23
**Status:** proposed closure theorem for the additive boundary-density law
**Verifier:** `scripts/frontier_planck_boundary_event_ward_identity_closure_theorem.py`
**Derivation theorem:** [PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md)

## Question

The previous audit reduced the final bare-density problem to

`delta = m_axis`,

where

`delta := nu - lambda_min(L_Sigma)`

and

`m_axis := Tr(rho_cell P_A)`.

Can this equality be derived by a real same-surface Ward identity, rather than
inserted as the remaining physical readout law?

## Result

Yes, on the primitive boundary-event action surface.

The follow-up derivation theorem shows that the Ward identity used here is not
an extra value postulate. It is the derivative at the identity source of the
unique primitive incidence insertion group

`U_A(s) = exp(s P_A)`.

The key point is that the relevant Ward identity is not a source-response Ward
identity on the Schur variables. Those identities erase additive constants.
The needed identity is the **normal-ordered boundary event Ward identity**:

> after the exact Schur floor is removed, the source-free one-cell boundary
> action growth is the expectation of the forced primitive boundary incidence
> charge.

In formulas:

`G_nu = (nu - lambda_min(L_Sigma)) I - (L_Sigma - lambda_min(L_Sigma) I)`,

`p_normal := sup spec(G_nu)`,

`N_grav := P_A`,

and the event Ward identity is

`p_normal = Tr(rho_cell N_grav)`.

Since

`G_nu = nu I - L_Sigma`,

one has

`p_normal = nu - lambda_min(L_Sigma) = delta`.

The forced primitive boundary charge is

`N_grav = P_A`,

and the source-free primitive-cell state is

`rho_cell = I_16 / 16`.

Therefore

`delta = Tr(rho_cell P_A) = 4/16 = 1/4`.

Equivalently,

`nu = lambda_min(L_Sigma) + Tr(rho_cell P_A)`.

On the exact rational witness with `lambda_min(L_Sigma) = 1`,

`nu = 1 + 1/4 = 5/4`.

This is the missing additive density.

## Why This Is Not The Failed Ward Route

The failed Ward route was:

`W_nu(j) = tau nu + W_0(j)`.

Differentiating with respect to the Schur source `j` removes `tau nu`, so
ordinary source-response Ward identities cannot determine `nu`.

The event Ward route asks a different physical question:

> what is the normal-ordered action growth of one primitive boundary cell?

That question is not answered by `partial_j W`. It is answered by the
primitive boundary incidence charge selected by the physical lattice carrier.

The event Ward identity therefore includes the constant term because it is a
Ward identity for boundary-cell insertion, not for Schur-source response.

## Inputs

This theorem uses already isolated ingredients:

1. the exact Schur boundary action family

   `G_nu = nu I - L_Sigma`;

2. the exact Schur floor

   `lambda_min(L_Sigma)`;

3. the primitive boundary carrier theorem, which identifies the microscopic
   one-step gravitational boundary incidence charge as

   `N_grav = P_A`;

4. the source-free primitive-cell state

   `rho_cell = I_16 / 16`;

5. the finite-source event Ward derivation:

   `d/ds log Tr(rho_cell exp(s P_A))|_(s=0) = Tr(rho_cell P_A)`;

6. same-source covariance:
   the Schur normal-ordered pressure and the primitive event insertion
   generator are two representations of the same one-cell boundary action
   source.

Neither item contains the numerical density `5/4`. The finite-source Ward
derivation fixes the primitive event derivative; same-source covariance says
that this derivative is the same physical infinitesimal boundary action
generator as the Schur normal-ordered pressure.

## Theorem 1: normal-ordering removes the Schur floor uniquely

Let `L_Sigma` be a positive boundary Schur operator and define

`G_nu := nu I - L_Sigma`.

The top growth pressure is

`p_*(nu) = sup spec(G_nu) = nu - lambda_min(L_Sigma)`.

Equivalently, rewrite the generator in floor-subtracted form

`G_nu = (nu - lambda_min(L_Sigma)) I - (L_Sigma - lambda_min(L_Sigma) I)`.

Then

`sup spec(G_nu) = nu - lambda_min(L_Sigma)`.

This is the unique floor subtraction that makes the floor-subtracted Schur
ground boundary mode carry zero decay before any primitive boundary-event
action is inserted.

No coefficient is chosen here. The floor is the exact spectral floor of the
already fixed same-surface Schur operator.

## Theorem 2: the primitive boundary event charge is `P_A`

On the time-locked primitive cell

`H_cell = span{|eta> : eta in {0,1}^4}`,

the one-step boundary incidence sector is the Hamming-weight-one packet

`A = {eta : |eta| = 1}`.

The corresponding projector is

`P_A = sum_(eta in A) P_eta`.

The primitive boundary carrier theorem already rules out:

- zero carrier;
- time-only or space-only carriers;
- non-unit weighted carriers;
- quotient carriers that discard retained multiplicity;
- scalar free-energy carriers that belong to a different object class.

Thus the microscopic one-step gravitational boundary incidence charge is

`N_grav = P_A`.

This statement contains no value `1/4`; it is an operator statement.

## Theorem 3: finite event Ward identity fixes the normal-ordered pressure

Let `N_grav` be the primitive boundary incidence charge and let `rho_cell` be
the source-free primitive-cell state.

The finite-source derivation theorem proves

`d/ds log Tr(rho_cell exp(s N_grav))|_(s=0) = Tr(rho_cell N_grav)`.

Same-source covariance identifies this primitive event-source generator with
the Schur normal-ordered pressure:

`sup spec(G_nu) = d/ds log Tr(rho_cell exp(s N_grav))|_(s=0)`.

Therefore

`sup spec(G_nu) = Tr(rho_cell N_grav)`.

### Reason

A primitive boundary cell has only one source-free unit-bearing insertion
group:

`exp(s N_grav)`.

If the normal-ordered growth were

`Tr(rho_cell N_grav) + c`

with `c != 0`, then `c` would be an extra additive boundary-action datum not
attached to any retained primitive event charge.

If the normal-ordered growth were

`alpha Tr(rho_cell N_grav)`

with `alpha != 1`, then the primitive incidence unit would be rescaled or
copied, which the primitive boundary action unit theorem already excludes.

Therefore the finite-source event Ward derivative plus same-source covariance
forces

`p_normal = Tr(rho_cell N_grav)`.

This is the constant-term Ward identity that the previous source-response
audit was missing.

## Corollary 1: the additive density is forced

Combining Theorems 1 to 3:

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

Therefore

`delta = m_axis`.

On the source-free cell,

`rho_cell = I_16 / 16`,

and `rank(P_A) = 4`, so

`Tr(rho_cell P_A) = 4/16 = 1/4`.

Thus

`delta = 1/4`.

## Corollary 2: the witness density is `nu = 5/4`

For the exact rational Schur witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

the spectrum is

`spec(L_Sigma) = {1, 5/3}`.

Hence

`lambda_min(L_Sigma) = 1`.

The closure law gives

`nu = lambda_min(L_Sigma) + 1/4 = 5/4`.

Then the exact pressure is

`p_*(nu) = nu - lambda_min(L_Sigma) = 1/4`.

## Corollary 3: area/action normalization gives conventional Planck length

The microscopic boundary density is

`S_cell / k_B = (1/4) A / a^2`.

The standard gravitational area/action density is

`S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`.

Equating the same physical boundary density gives

`(1/4) / a^2 = 1 / (4 l_P^2)`,

so

`a^2 = l_P^2`,

and since both lengths are positive,

`a = l_P`.

## Hostile-Review Status

The coefficient is no longer an imported value on this surface. The derivation
does not insert `nu = 5/4`; it derives it from:

- the Schur spectral floor `lambda_min(L_Sigma) = 1`;
- the forced primitive boundary incidence charge `P_A`;
- the source-free event state `I_16/16`;
- the finite-source Ward derivative of `exp(s P_A)`;
- same-source covariance with the Schur normal-ordered pressure;
- primitive unit-count semantics.

The remaining possible rejection is now sharper:

> reject same-source covariance between the Schur normal-ordered boundary
> pressure and the primitive incidence insertion generator.

That is a rejection of the primitive boundary-event action surface, not a
coefficient objection. If the event Ward identity is accepted, the additive
density is closed.
