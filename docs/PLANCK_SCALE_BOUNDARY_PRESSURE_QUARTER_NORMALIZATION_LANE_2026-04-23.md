# Planck-Scale Boundary Pressure Quarter Normalization Lane

**Date:** 2026-04-23  
**Status:** science-only fourth-wave normalization obstruction / no-go  
**Audit runner:** `scripts/frontier_planck_boundary_pressure_quarter_normalization_lane.py`

## Question

After the time-lock reduction and the collective boundary Schur route, can one
now derive the additive pressure target

`p_* = sup spec(G_Sigma) = 1/4`

from a canonical same-surface normalization principle?

Equivalently:

- is there now a theorem-native reason the correct boundary generator should
  have top pressure `1/4`;
- or does quarter still enter only by choosing one normalization offset / scale?

## Bottom line

Not yet.

The strongest honest result on the present same-surface boundary route is a
**normalization obstruction**:

1. the time-locked Schur-complement class still carries an exact affine
   normalization gauge

   `G -> lambda G + mu I`, `lambda > 0`;

2. semigroup structure, positivity, collective boundary origin, and the
   boundary/worldtube support are all preserved under that affine action;
3. the top pressure transforms as

   `p_* -> lambda p_* + mu`;

4. therefore quarter is **not** fixed by the current class itself;
5. the obvious canonical normalization attempts either
   - kill the route (`p_* = 0` on stochastic/Markov normalization),
   - miss the target (`p_* = 5/8`, `1/sqrt(2)`, or `1` on standard witness
     normalizations),
   - or realize quarter only as a trivial scalar identity shift.

So the current boundary route does **not** yet derive

`p_* = 1/4`.

What it does prove is sharper:

> exact quarter cannot be obtained from the time-locked collective boundary
> Schur class by semigroup positivity plus the usual normalization choices
> alone.

Any future exact quarter theorem must therefore supply a genuinely new
**non-affine, unit-bearing same-surface normalization principle**.

## Inputs

This lane builds only on the already narrowed boundary/time-lock program:

- [PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_COLLECTIVE_BOUNDARY_ENTROPY_CARRIER_LANE_2026-04-23.md](./PLANCK_SCALE_COLLECTIVE_BOUNDARY_ENTROPY_CARRIER_LANE_2026-04-23.md)
- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md](./PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md)

The upstream branch already established:

- the surviving boundary route is a one-clock semigroup on the time-locked
  worldtube;
- the boundary carrier must be genuinely collective;
- exact conventional Planck on that route is equivalent to

  `p_* = sup spec(G_Sigma) = 1/4`;

- the earlier spectral-radius note already ruled out stochastic, finite
  algebraic, and scaled Gibbs/Perron finite-memory closures as exact
  derivations.

This note attacks the remaining question:

> maybe the right **normalization principle** on the admitted boundary
> generator class forces quarter.

## Setup

The surviving same-surface boundary class is:

`T_grav(tau) = exp(tau G_Sigma)`,

with `G_Sigma` a collective boundary generator induced by the time-locked
Schur-complement reduction of the exact gravity carrier.

The minimal exact witness already on the branch is

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

whose eigenvalues are

`lambda_min(L_Sigma) = 1`,

`lambda_max(L_Sigma) = 5/3`.

The canonical positivity-preserving affine generator family built from this
same witness is

`G_(lambda,mu) := mu I - lambda L_Sigma`, `lambda > 0`.

Its eigenvalues are

`p_1(lambda,mu) = mu - lambda`,

`p_2(lambda,mu) = mu - 5 lambda / 3`,

so the top pressure is exactly

`p_*(lambda,mu) = mu - lambda`.

Quarter therefore becomes the affine tuning line

`mu = lambda + 1/4`.

That is already the core obstruction in explicit coordinates.

## Theorem 1: affine normalization gauge obstruction

Let `G_Sigma` be any positive one-clock boundary generator on the admitted
time-locked same-surface class. Then for every `lambda > 0` and every
`mu in R`,

`G'_Sigma := lambda G_Sigma + mu I`

belongs to the same structural class:

- it generates a one-clock semigroup

  `T'_grav(tau) = exp(tau G'_Sigma) = e^(mu tau) exp(lambda tau G_Sigma)`;

- it preserves the same eigenspaces;
- it preserves positivity/improving order whenever the original semigroup does;
- it preserves the same boundary/worldtube support;
- it preserves the same collective/nonlocal Schur origin.

But its top pressure transforms affinely:

`p'_* = lambda p_* + mu`.

Therefore:

> semigroup structure, positivity, collective Schur origin, and time-lock do
> **not** by themselves determine the additive quarter coefficient.

They determine the generator class, but not its absolute normalization.

### Proof sketch

Everything listed above is stable under positive rescaling and identity
shifts. Positive rescaling only reparametrizes the clock variable and identity
shift multiplies the semigroup by the scalar factor `e^(mu tau)`. Neither move
changes the underlying boundary carrier or its Schur-complement provenance.
But top spectral growth is affine in these two operations, hence not fixed.

## Theorem 2: the exact witness exhibits the full affine freedom

For the minimal exact boundary witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

the affine same-surface family

`G_(lambda,mu) = mu I - lambda L_Sigma`

has exact top pressure

`p_*(lambda,mu) = mu - lambda`.

Therefore:

1. every point on the line
   `mu = lambda + 1/4`
   gives exact quarter pressure;
2. every point off that line misses quarter;
3. the current carrier class alone does not isolate one distinguished point.

So quarter is not a theorem consequence of the witness class. It is an
underdetermined normalization condition on that class.

## Theorem 3: standard canonical normalizations do not force quarter

The usual normalization moves one would try next all fail.

### 3A. Markov/stochastic normalization kills the route

If one insists that `exp(tau G_Sigma)` be an exact stochastic/Markov evolution
for each `tau`, then its spectral radius is `1`, so

`p_* = log rho(exp(G_Sigma)) = 0`.

That was already visible in the earlier spectral-radius lane and remains fatal
here.

### 3B. Trace-one positive normalization misses quarter on the witness

Normalize the positive witness directly by trace:

`G_tr := L_Sigma / Tr(L_Sigma) = (3/8) L_Sigma`.

Then

`spec(G_tr) = {5/8, 3/8}`,

so

`p_*(G_tr) = 5/8 != 1/4`.

### 3C. Centered trace-zero normalization leaves a free scale

The centered witness is

`C := L_Sigma - (Tr(L_Sigma)/2) I = [[0, 1/3], [1/3, 0]]`,

with eigenvalues `+- 1/3`.

Any trace-zero normalization has the form

`G_0(lambda) = lambda C`.

Then

`p_*(G_0(lambda)) = lambda / 3`,

so quarter again appears only on the tuned value

`lambda = 3/4`.

### 3D. Operator-norm and Frobenius normalizations miss quarter

For the same centered witness `C`:

- `||C||_op = 1/3`, so
  `G_op := C / ||C||_op`
  has
  `p_*(G_op) = 1`;
- `||C||_F = sqrt(2)/3`, so
  `G_F := C / ||C||_F`
  has
  `p_*(G_F) = 1/sqrt(2)`.

Neither is quarter.

So the standard parameter-free matrix normalizations do not close the
coefficient.

## Theorem 4: democratic `3+1` dimension counting does not rescue quarter

The most tempting remaining idea is:

> after time-lock, maybe the exact `3+1` democracy itself forces quarter.

That does **not** work on its own.

Take any positive `4 x 4` generator `G >= 0` with

`Tr(G) = 1`.

Then the top eigenvalue obeys

`p_* = lambda_max(G) >= 1/4`,

with equality iff all four eigenvalues are equal, i.e.

`G = I_4 / 4`.

So quarter appears in the trace-one democratic class only in the completely
scalar case.

That is not the desired gravitational closure, because:

- it carries no collective Schur-boundary structure;
- it is just a pure identity shift;
- `exp(tau G) = e^(tau/4) I_4` contains no nontrivial boundary dynamics.

Therefore:

> the exact number of locked spacetime directions does not by itself derive the
> quarter pressure. It only identifies the trivial scalar lower-bound case.

This kills the cleanest "there are four equal directions, so pressure is
automatically `1/4`" rescue.

## Corollary: what a real quarter theorem would have to add

The surviving exact quarter route now needs a new ingredient that is **not**
invariant under the affine normalization gauge.

Concretely, it would have to supply a same-surface law of one of these types:

1. **boundary action normalization**
   tying the additive generator pressure directly to one exact gravitational
   action density on the time-locked worldtube;
2. **boundary information/entropy conversion**
   tying `p_*` to an exact non-affine information or action quantum;
3. **boundary vacuum reference theorem**
   selecting one exact zero/one point for `G_Sigma` that is not preserved under
   arbitrary identity shifts and positive rescalings.

Until one of those exists, quarter remains unclosed on the boundary route.

## What this closes

This note closes several still-tempting moves:

- "maybe the collective boundary Schur class already fixes the additive
  coefficient";
- "maybe positivity plus semigroup structure kills the last freedom";
- "maybe trace/centered/Frobenius/operator normalization naturally produces
  `1/4`";
- "maybe exact `3+1` democracy alone explains the quarter."

All of those are now negative.

## What this does not close

This note does **not** prove:

- that no future same-surface quarter theorem exists;
- that the information/action route is dead;
- that the boundary route is dead;
- that exact conventional Planck is impossible on the framework.

It proves the narrower but important statement:

> on the current admitted time-locked collective boundary Schur class, exact
> quarter pressure is still not derivable from the obvious normalization
> principles. Any future success has to come from a new non-affine, unit-bearing
> theorem.

## Use

Use this note as:

- the current best honesty surface for the boundary normalization problem;
- a guardrail against calling quarter "derived" too early;
- the entrypoint for any future boundary action / information normalization
  theorem.
