# Planck-Scale Boundary Non-Affine Pressure Normalization Lane

**Date:** 2026-04-23  
**Status:** science-only fifth-wave theorem/reduction on the remaining boundary normalization problem  
**Audit runner:** `scripts/frontier_planck_boundary_nonaffine_pressure_normalization_lane.py`

## Question

The boundary route is now sharply narrowed:

- the exact time-locked `3+1` gravity carrier forces the collective Schur
  boundary operator `L_Sigma`;
- the canonical one-clock transfer law `T_can(tau) = exp(-tau L_Sigma)` is
  exact but contractive;
- quarter pressure is not fixed by the surviving affine gauge
  `G -> lambda G + mu I`.

So the exact remaining question is:

> can the same-surface Schur boundary carrier itself force a genuinely
> non-affine normalization/pressure law, without importing quarter
> `1/4` or `e^(1/4)` by hand?

## Bottom line

Yes, but it lands as a **new exact normalization law plus one sharp remaining
bridge**, not a full Planck close.

The exact Schur boundary action already provides a canonical source-free
Gaussian partition on the time-locked boundary worldtube. After unit-carrier
normalization on the same boundary mode space, that partition is exactly

`Z_hat(L_Sigma) = det(L_Sigma)^(-1/2)`.

This forces a genuinely non-affine same-surface vacuum pressure density

`p_vac(L_Sigma) := -(1/n) log Z_hat(L_Sigma) = (1/(2n)) log det(L_Sigma)`,

where `n` is the boundary carrier rank.

This law is:

1. exact from the Schur boundary action;
2. basis invariant;
3. additive on independent direct sums at the level of total free energy
   `F_vac := n p_vac = (1/2) log det(L_Sigma)`;
4. genuinely non-affine on the old gauge.

So the branch now has an exact same-surface non-affine normalization law.

But on the minimal exact witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

it gives

`p_vac(L_Sigma) = (1/4) log(5/3) ~= 0.127706`,

not `1/4`.

So the remaining open ingredient is now very specific:

> derive the physical identification that turns the canonical Schur vacuum
> density `p_vac(L_Sigma)` into the physical boundary growth pressure
> `p_* = sup spec(G_Sigma)`.

That bridge is now the only live content on the boundary normalization lane.

## Inputs

This lane uses only already-opened same-surface ingredients:

- [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](./OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md](./PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md)

The earlier lanes already proved:

1. exact time-lock `a_s = c a_t`;
2. exact Schur boundary action on the same microscopic lattice carrier;
3. exact bulk-to-boundary Schur completion for the surviving boundary route;
4. exact canonical transfer law `T_can(tau) = exp(-tau L_Sigma)`;
5. failure of affine/trace/Frobenius/operator-norm normalizations to force
   quarter.

This note attacks the next question:

> is there an exact non-affine normalization law already contained in the
> same Schur boundary carrier itself?

## Setup

On the time-locked boundary worldtube, let the exact zero-source Schur
boundary action be

`I_Sigma(b ; 0) = (1/2) b^T L_Sigma b`,

with `L_Sigma > 0` on an `n`-dimensional real boundary mode space.

The exact source-free Gaussian partition is then

`Z_Sigma(L_Sigma) := integral exp(-(1/2) b^T L_Sigma b) db`.

By the standard exact Gaussian formula,

`Z_Sigma(L_Sigma) = (2 pi)^(n/2) det(L_Sigma)^(-1/2)`.

The universal measure factor `(2 pi)^(n/2)` is not Planck data. It is the
same Gaussian measure constant already present for the unit carrier `I_n` on
the same mode space. So the exact same-surface normalized vacuum partition is

`Z_hat(L_Sigma) := Z_Sigma(L_Sigma) / Z_Sigma(I_n) = det(L_Sigma)^(-1/2)`.

This is the first exact non-affine scalar available from the current boundary
carrier that does not pass through the old affine gauge on `G_Sigma`.

## Theorem 1: exact same-surface Gaussian normalization law

Assume:

1. exact time-lock `a_s = c a_t`;
2. exact Schur boundary quadratic carrier `I_Sigma(b ; 0) = (1/2) b^T L_Sigma b`
   with `L_Sigma > 0`;
3. no added boundary source;
4. unit-carrier normalization against `I_n` on the same boundary mode space.

Then the exact normalized one-step vacuum partition is

`Z_hat(L_Sigma) = det(L_Sigma)^(-1/2)`.

Therefore the exact same-surface vacuum free-energy density is

`p_vac(L_Sigma) := -(1/n) log Z_hat(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

This law is forced by the admitted Schur boundary action itself. It does not
import quarter, `e^(1/4)`, or an external boundary entropy carrier.

### Proof sketch

The Schur boundary action is already exact on the same microscopic lattice
carrier. Gaussian integration of a positive quadratic form is exact and gives

`Z_Sigma(L_Sigma) = (2 pi)^(n/2) det(L_Sigma)^(-1/2)`.

Dividing by the identical expression at `L_Sigma = I_n` removes the universal
measure factor and leaves

`Z_hat(L_Sigma) = det(L_Sigma)^(-1/2)`.

Taking `-(1/n) log` gives the claimed density.

## Theorem 2: this law is genuinely non-affine

The exact same-surface law

`p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`

is genuinely non-affine on the previously surviving gauge class.

### 2A. Positive rescaling

For every `lambda > 0`,

`p_vac(lambda L_Sigma) = p_vac(L_Sigma) + (1/2) log lambda`.

So the law is additive in `log lambda`, not affine in `lambda`.

### 2B. Identity shift

If `L_Sigma` has eigenvalues `ell_1, ..., ell_n`, then

`p_vac(L_Sigma + mu I_n) = (1/(2n)) sum_i log(ell_i + mu)`.

Its second derivative is

`d^2/d mu^2 p_vac(L_Sigma + mu I_n)`
`= -(1/(2n)) sum_i (ell_i + mu)^(-2)`,

which is strictly negative whenever `mu > -min_i ell_i`.

So the law is not affine in the additive shift either.

This is exactly what the earlier boundary lane asked for:

> a same-surface normalization law that breaks the old affine gauge without
> simply choosing `mu` or `lambda` by hand.

## Theorem 3: additivity and basis invariance

The total vacuum free energy

`F_vac(L_Sigma) := n p_vac(L_Sigma) = (1/2) log det(L_Sigma)`

is additive on independent direct sums:

`F_vac(L_1 (+) L_2) = F_vac(L_1) + F_vac(L_2)`.

Equivalently, the density is the weighted average

`p_vac(L_1 (+) L_2)`
`= (n_1 p_vac(L_1) + n_2 p_vac(L_2)) / (n_1 + n_2)`.

And because it depends only on `det(L_Sigma)`, it is basis invariant.

So `p_vac` is a structurally sensible normalization law:

- exact on the same surface;
- insensitive to basis packaging;
- compatible with independent composition;
- non-affine on the old boundary gauge.

## Minimal exact witness

Take the exact rational Schur witness already fixed by the earlier lanes:

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`.

Its spectrum is

`{1, 5/3}`,

so

`det(L_Sigma) = 5/3`.

Because `n = 2`, the exact vacuum pressure density is

`p_vac(L_Sigma) = (1/4) log(5/3) ~= 0.127706`.

This is the strongest exact same-surface non-affine number now available on
the boundary lane.

## Corollary: the boundary lane now has a canonical non-affine law, but not quarter

The branch now genuinely improves on the earlier obstruction notes:

1. the boundary carrier is no longer only a class up to affine pressure gauge;
2. the exact Schur boundary action forces one canonical non-affine scalar law
   on that carrier;
3. but that law does **not** equal `1/4` on the exact witness.

So the open problem is no longer:

> find any non-affine same-surface normalization law.

It is now:

> derive why the physical Planck boundary pressure `p_* = sup spec(G_Sigma)`
> should be identified with, or derived from, the canonical Schur vacuum
> density `p_vac(L_Sigma)`.

That is a much sharper target.

## The remaining bridge in exact form

The current branch now has two exact same-surface scalars on the boundary route:

1. the canonical growth-pressure target

   `p_* := sup spec(G_Sigma)`,

   which must equal `1/4` for exact conventional Planck;
2. the canonical Schur vacuum density

   `p_vac(L_Sigma) := (1/(2n)) log det(L_Sigma)`.

What is still missing is an exact theorem of one of the following forms:

- **identification theorem**

  `p_* = p_vac(L_Sigma)`;

- **conversion theorem**

  `p_* = Phi(p_vac(L_Sigma), spec(L_Sigma))`;

- **generator theorem**

  `G_Sigma = Psi(L_Sigma)`

  with `sup spec(Psi(L_Sigma)) = (1/(2n)) log det(L_Sigma)` or another exact
  same-surface relation.

Without one of those, quarter remains open.

## The theorem-level statement

**Theorem (Canonical non-affine Schur vacuum normalization / reduction).**
Assume:

1. the exact time-locked `3+1` boundary route;
2. the exact Schur boundary action on the surviving collective boundary
   carrier;
3. no added boundary source;
4. unit-carrier normalization on the same boundary mode space.

Then:

1. the exact normalized vacuum partition is
   `Z_hat(L_Sigma) = det(L_Sigma)^(-1/2)`;
2. the exact same-surface vacuum pressure density is
   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;
3. this law is basis invariant, composition-compatible, and genuinely
   non-affine on the previous normalization gauge;
4. on the minimal exact witness `L_Sigma = [[4/3,1/3],[1/3,4/3]]`, it gives
   `p_vac = (1/4) log(5/3)`, not `1/4`;
5. therefore the boundary route now contains an exact non-affine
   normalization law, but exact conventional Planck still requires one
   additional theorem identifying physical boundary growth pressure with a
   scalar derived from the Schur carrier.

## What this closes

This closes three previously open points:

1. the branch can now point to an exact same-surface non-affine normalization
   law, not only to obstructions;
2. that law is derived from the exact Schur boundary action itself, not from a
   new entropy carrier or tuned pressure shift;
3. the remaining boundary problem is now reduced to one explicit physical
   identification theorem.

## What this does not close

This note still does **not** prove:

1. `p_* = 1/4`;
2. `rho(T(1)) = e^(1/4)`;
3. that physical Planck boundary pressure equals the Schur vacuum density
   `p_vac`;
4. exact conventional `a = l_P`.

So this lane is a real theorem-grade narrowing, not a fake Planck close.
