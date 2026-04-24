# Planck-Scale Boundary Density Three-Mechanism Audit

**Date:** 2026-04-23
**Status:** direct hostile-review audit of the last boundary-density step
**Verifier:** `scripts/frontier_planck_boundary_density_three_mechanism_audit.py`

## Post-Audit Note

This audit records the pre-closure state: ordinary source-response Ward
identities, action-phase quantization, and imported semiclassical boundary-term
normalization did not derive the additive density.

The follow-up closure attempt is:

- [PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_CLOSURE_THEOREM_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_CLOSURE_THEOREM_2026-04-23.md)

That theorem supplies a different Ward identity: the normal-ordered primitive
boundary event insertion identity. The no-go statements below remain valid for
the three mechanisms as formulated here.

## Question

Can the remaining boundary density

`nu = lambda_min(L_Sigma) + 1/4`

be derived, without importing the Planck result, by one of the three serious
mechanisms now left on the table?

1. a real Ward identity;
2. action-phase quantization;
3. microscopic gravitational boundary-term normalization.

## Result

Not on the current stack.

The three mechanisms are valuable because they define the right proof
obligations, but none of the current versions derives the required additive
density. They either leave the additive vacuum constant invisible, reduce the
problem to an unproved action/defect coefficient, or import the semiclassical
boundary coefficient rather than deriving it microscopically.

The exact status is:

- multiplicative boundary-unit ambiguity has been removed on the primitive
  and exact-action object classes;
- the surviving problem is additive:

  `I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`;

- exact quarter is equivalent to

  `delta := nu - lambda_min(L_Sigma) = 1/4`;

- the only already isolated positive candidate with that value is

  `m_axis = Tr(rho_cell P_A) = 1/4`;

- therefore the clean remaining theorem is not a broad "Planck matching"
  slogan. It is the exact same-surface readout law

  `delta = m_axis`.

On the rational witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

we have

`lambda_min(L_Sigma) = 1`,

`det(L_Sigma) = 5/3`,

`p_vac(L_Sigma) = (1/4) log(5/3)`,

and exact quarter requires

`nu = 5/4`.

## Mechanism 1: Ward identities do not see the additive density

For the retained same-surface action family,

`I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`,

the partition functional has the form

`Z_nu(j) = exp(tau nu) Z_0(j)`,

so

`W_nu(j) := log Z_nu(j) = tau nu + W_0(j)`.

Any Ward identity built from source response derivatives satisfies

`partial_j W_nu = partial_j W_0`,

`partial_j^2 W_nu = partial_j^2 W_0`,

and similarly at all higher source orders.

So source-response Ward identities fix the Schur operator, the response law,
and the correlation algebra. They do not fix the additive vacuum density
`nu`.

Additivity on independent boundary blocks can require

`nu(L_1 (+) L_2) = nu(L_1) + nu(L_2)`,

but it still does not choose the one-block value. On the witness, every value
of `nu` has the same source-response Ward identities.

The only Ward-like normalizations already present choose known non-quarter
values:

- empty-vacuum action normalization chooses `nu = 0`;
- scalar Gaussian observable normalization chooses
  `nu = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

On the witness these are `0` and `(1/4) log(5/3)`, not `5/4`.

Therefore a Ward route can close the theorem only if it is not merely a
source-response Ward identity. It must be a new boundary Ward identity that
couples the Schur spectral floor to the primitive event-sector count and forces

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

That identity is not yet derived.

## Mechanism 2: action-phase quantization reduces the target but does not fix it

The elementary action-phase reduction gives the exact relation

`a^2 / l_P^2 = 8 pi q_* / eps_*`,

where

- `q_* = S_* / hbar` is the elementary action phase quantum;
- `eps_*` is the elementary geometric defect quantum on the same carrier.

Exact conventional Planck length requires

`q_* / eps_* = 1 / (8 pi)`.

That is a precise coefficient theorem. It is not a consequence of merely
knowing that the lattice has a primitive cell, a spinorial phase, or a
finite-dimensional event packet.

The current `C^16` stack gives exact counting numbers:

`1/16` per primitive event and `4/16 = 1/4` for the axis-sector packet.

Those are real structural numbers, but by themselves they are not an action
phase quantum and a geometric defect quantum on the same elementary process.
To close by action-phase quantization, the theory must prove both sides of the
same elementary relation:

`q_* = eps_* / (8 pi)`.

Equivalently, on the additive boundary-action route it must prove that the
positive residual above the Schur floor is the axis-sector action packet:

`delta = m_axis`.

The present action-phase lane supplies the target equation. It does not yet
derive the required ratio.

## Mechanism 3: microscopic gravitational boundary-term normalization is the right route only if it is microscopic

The standard gravitational area/action law is

`S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`.

Matching this law to the already derived primitive coefficient

`S_cell / k_B = c_cell A / a^2`, with `c_cell = 1/4`,

gives

`a^2 = 4 c_cell l_P^2 = l_P^2`.

That dimensional normalization is correct and fully accounted for. But if the
law is simply imported as the external semiclassical gravitational
normalization, then it is not a bare-lattice derivation of the microscopic
boundary density.

To make this route native, one needs a microscopic boundary-term theorem:

1. derive the gravitational boundary action as a same-surface primitive-cell
   count or exact reduced boundary action;
2. show that its additive density is

   `nu = lambda_min(L_Sigma) + Tr(rho_cell P_A)`;

3. equivalently, show on the witness that `nu = 5/4`.

The current exact Schur boundary action does not do this. Its canonical
same-surface values remain

`nu = 0`

or

`nu = p_vac(L_Sigma)`.

So boundary-term normalization is the most physically direct possible closure
route, but only after the boundary term is derived microscopically. Used before
that derivation, it is an explicit gravity normalization input.

## Theorem: the current three mechanisms do not derive the density

Assume the current retained boundary-action surface:

1. exact Schur Hessian `L_Sigma`;
2. exact one-clock action family `I_nu`;
3. source-response Ward identities on the same boundary variables;
4. the elementary action-phase reduction;
5. the standard area/action normalization accounted for as a separate
   dimensional law.

Then:

1. source-response Ward identities are invariant under
   `W -> W + tau nu`, so they cannot determine `nu`;
2. action-phase quantization reduces exact Planck closure to
   `q_* / eps_* = 1/(8 pi)`, but does not derive that ratio;
3. semiclassical boundary-term normalization derives `a = l_P` only after the
   microscopic boundary density has already been identified with the
   gravitational boundary/action carrier.

Therefore the current stack does not yet derive

`nu = 5/4`.

It reduces the remaining proof to one exact new theorem:

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

Equivalently:

`delta = m_axis`.

## What Would Close The Lane

Any one of the following would close the density step without smuggling it:

1. **Boundary Ward identity.** A real same-surface Ward identity whose
   constant term is not invisible and whose anomaly/residual is exactly
   `Tr(rho_cell P_A)`.
2. **Action-phase theorem.** A same-process derivation of
   `q_* / eps_* = 1/(8 pi)`, or equivalently a derivation that the elementary
   action residual is the axis-sector packet mass.
3. **Microscopic boundary-term theorem.** A derivation of the gravitational
   boundary term from the primitive lattice action showing
   `nu = lambda_min(L_Sigma) + m_axis`.

Until one of those is proved, the branch should not call the Planck result a
closed bare-axiom theorem. The correct reviewer-facing statement is:

> the branch derives the exact primitive quarter and reduces conventional
> Planck closure to the single same-surface boundary-density law
> `delta = m_axis`, but that law is not yet derived by the current Ward,
> phase, or boundary-term machinery.
