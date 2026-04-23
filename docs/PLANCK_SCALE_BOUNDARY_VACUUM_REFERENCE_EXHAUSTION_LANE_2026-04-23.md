# Planck-Scale Boundary Vacuum Reference Exhaustion Lane

**Date:** 2026-04-23  
**Status:** science-only classification theorem / sharp no-go on same-surface boundary vacuum references  
**Audit runner:** `scripts/frontier_planck_boundary_vacuum_reference_exhaustion_lane.py`

## Question

The boundary route is now reduced to a very narrow coefficient problem.

The branch already has:

- canonical zero-vacuum action normalization

  `nu_0(L_Sigma) = 0`;

- canonical Gaussian vacuum-pressure matching

  `nu_gauss(L_Sigma) = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

- and the exact quarter target on the action-pressure lane

  `nu_quarter(L_Sigma) = lambda_min(L_Sigma) + 1/4`.

So the remaining question is:

> if one systematically exhausts the admissible same-surface boundary vacuum
> reference laws already available on the exact Schur carrier, does quarter
> follow, or does it still require one explicit new datum?

## Bottom line

The strongest honest result is **outcome (2)** from the target brief:

> any admissible same-surface Gaussian boundary vacuum-reference law that lands
> on quarter must introduce one explicit new datum.

More precisely:

1. every same-surface Gaussian vacuum-reference law on the exact Schur carrier
   has the form

   `nu_R(L) = (1/(2n)) log det(L) - (1/(2n)) log det(R(L))`

   for a positive same-surface reference operator `R(L)` on the same boundary
   mode space;
2. the dependence on the reference is therefore reduced to one scalar datum,
   namely

   `r_R(L) := (1/(2n)) log det(R(L))`;
3. the current branch supplies exactly two canonical no-datum choices:

   - self reference `R(L) = L`, giving `nu_R(L) = 0`;
   - unit reference `R(L) = I_n`, giving `nu_R(L) = p_vac(L)`;

4. exact quarter would require

   `r_R(L) = p_vac(L) - lambda_min(L) - 1/4`,

   equivalently

   `det(R(L)) = det(L) * exp(-2n (lambda_min(L) + 1/4))`.

So quarter is not hidden in the present same-surface vacuum-reference grammar.
It appears only after adding one explicit new scalar reference datum.

On the exact witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

this required datum is

`det(R(L_Sigma)) = (5/3) exp(-5)`,

or equivalently

`delta_quarter = nu_quarter - p_vac = 5/4 - (1/4) log(5/3) ~= 1.122294`.

That datum is not supplied by the current Schur/action stack.

## Inputs

This lane uses only already-earned same-surface boundary results:

- [PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)

What those notes already fixed:

1. exact Schur boundary carrier `L_Sigma > 0`;
2. exact action family

   `I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`;

3. exact pressure law

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

4. exact canonical Gaussian vacuum density

   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

5. exact quarter requirement

   `nu_quarter(L_Sigma) = lambda_min(L_Sigma) + 1/4`;

6. exact `C^16` bridge candidate

   `nu = lambda_min(L_Sigma) + m_axis`

   with `m_axis = 1/4`, as a possible new bridge law rather than a current
   vacuum-reference theorem.

## Setup: Gaussian vacuum-reference laws on the same boundary carrier

Let `L > 0` act on an `n`-dimensional real boundary mode space.

The exact source-free Schur Gaussian partition is

`Z(L) = integral exp(-(1/2) b^T L b) db`

and equals

`Z(L) = (2 pi)^(n/2) det(L)^(-1/2)`.

Now let `R(L) > 0` be a positive same-surface reference operator on the same
mode space. Define the normalized vacuum-reference partition ratio

`Z_ref(L ; R) := Z(L) / Z(R(L))`.

Then the induced vacuum-reference density is

`nu_R(L) := -(1/n) log Z_ref(L ; R)`

`= (1/(2n)) log det(L) - (1/(2n)) log det(R(L))`.

This is the natural exact Gaussian reference grammar on the current boundary
carrier: no new carriers, no new sources, and no change of microscopic mode
space.

## Theorem 1: every Gaussian same-surface vacuum-reference law reduces to one scalar datum

Assume:

1. exact source-free Schur boundary action on the same `n`-mode carrier;
2. positive same-surface reference operator `R(L) > 0` on that same mode space;
3. vacuum reference defined by Gaussian partition comparison
   `Z(L) / Z(R(L))`.

Then the induced vacuum-reference density is

`nu_R(L) = p_vac(L) - r_R(L)`

with

`p_vac(L) = (1/(2n)) log det(L)`,

`r_R(L) := (1/(2n)) log det(R(L))`.

So every admissible same-surface Gaussian reference law is parameterized by one
scalar reference datum `r_R(L)`.

### Consequences

- **basis invariance:** because `det(U^T L U) = det(L)` and
  `det(U^T R(L) U) = det(R(L))`, the law depends only on conjugacy-invariant
  spectral data;
- **direct-sum additivity of total vacuum free energy:**

  `F_R(L) := n nu_R(L) = (1/2) log det(L) - (1/2) log det(R(L))`

  is additive on independent direct sums.

So the same-surface Gaussian reference grammar has no hidden functional freedom
beyond the single scalar `r_R(L)`.

## Corollary 1: the current branch supplies exactly two canonical no-datum choices

Within the current boundary stack, two canonical reference choices are already
present.

### 1A. Self reference

Choose

`R(L) = L`.

Then

`r_R(L) = (1/(2n)) log det(L) = p_vac(L)`,

so

`nu_R(L) = 0`.

This is exactly the empty-vacuum action normalization already isolated in
[PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md).

### 1B. Unit reference

Choose

`R(L) = I_n`.

Then

`r_R(L) = 0`,

so

`nu_R(L) = p_vac(L) = (1/(2n)) log det(L)`.

This is exactly the canonical Gaussian vacuum-pressure matching already fixed in
[PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md).

These are the only canonical no-datum reference laws presently earned on the
branch. Everything else requires a nontrivial reference scalar
`r_R(L)`.

## Theorem 2: quarter requires one explicit new reference datum

Let

`nu_quarter(L) := lambda_min(L) + 1/4`.

Then a same-surface Gaussian reference law satisfies

`nu_R(L) = nu_quarter(L)`

if and only if

`r_R(L) = p_vac(L) - lambda_min(L) - 1/4`,

equivalently

`det(R(L)) = det(L) * exp(-2n (lambda_min(L) + 1/4))`.

So quarter does not arise automatically from the Gaussian same-surface vacuum
grammar. It appears only after specifying one explicit reference datum,
represented either by:

- the scalar shift

  `delta_R(L) := nu_quarter(L) - p_vac(L)`,

  or

- the reference determinant

  `det(R(L))`.

This is the sharpest honest exhaustion result on the current branch.

## Corollary 2: current same-surface vacuum references do not supply quarter

The two already-earned canonical laws are:

- `nu_0(L) = 0`;
- `nu_gauss(L) = p_vac(L)`.

The quarter value

`nu_quarter(L) = lambda_min(L) + 1/4`

differs from both unless one adds the explicit reference datum from Theorem 2.

So the current branch does not hide quarter in a different vacuum-reference
packaging. It still needs one new boundary datum or bridge theorem.

## Minimal exact witness

Take the exact Schur witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`.

Then:

- `spec(L_Sigma) = {1, 5/3}`;
- `lambda_min(L_Sigma) = 1`;
- `det(L_Sigma) = 5/3`;
- `n = 2`.

Therefore:

- self reference gives

  `nu_0(L_Sigma) = 0`;

- unit reference gives

  `nu_gauss(L_Sigma) = (1/4) log(5/3) ~= 0.127706`;

- quarter would require

  `nu_quarter(L_Sigma) = 1 + 1/4 = 5/4`.

The missing explicit datum is therefore

`delta_quarter(L_Sigma) = nu_quarter(L_Sigma) - nu_gauss(L_Sigma)`

`= 5/4 - (1/4) log(5/3) ~= 1.122294`.

Equivalently, the reference determinant would have to be

`det(R(L_Sigma)) = (5/3) exp(-5)`.

That quantity is not selected by the current same-surface Schur/action notes.

## Interpretation

This exhaustion lane settles the vacuum-reference question as far as the
current branch honestly goes.

- If one asks for canonical no-datum same-surface vacuum references, there are
  exactly two:
  `nu = 0` and `nu = p_vac(L)`.
- If one asks for quarter, the answer is no longer vague:
  quarter requires one explicit new scalar reference datum.
- A future close could still come from a bridge theorem, for example

  `nu = lambda_min(L) + m_axis`,

  but that would be a new theorem connecting the boundary vacuum reference to
  the `C^16` carrier, not an already-earned consequence of the present
  Gaussian reference grammar.

So the honest scientific posture is:

> the same-surface boundary vacuum-reference laws are now exhausted sharply
> enough that quarter cannot be claimed as implicit. It must arrive, if at all,
> through one new explicit datum or bridge theorem.

