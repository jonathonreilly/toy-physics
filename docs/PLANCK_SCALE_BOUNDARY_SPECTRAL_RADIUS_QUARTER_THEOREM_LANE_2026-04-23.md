# Planck-Scale Boundary Spectral-Radius Quarter Theorem Lane

**Date:** 2026-04-23  
**Status:** science-only third-wave boundary obstruction/classification lane  
**Audit runner:** `scripts/frontier_planck_boundary_spectral_radius_quarter_theorem_lane.py`

## Question

After reducing the boundary route to a genuinely collective gravitational
Perron/pressure carrier, can one now force the exact coefficient

`rho(T_grav) = e^(1/4)`

without importing that value?

Equivalently, can one force exact pressure

`P_grav := log rho(T_grav) = 1/4`

from a natural same-surface boundary transfer law?

## Verdict

Not on the currently natural transfer classes.

The sharpened exact result is:

1. **Markov/stochastic normalization cannot work:** if the boundary carrier is
   normalized as a probability transfer kernel, then `rho(T) = 1`, not
   `e^(1/4)`.
2. **Parameter-free finite algebraic carriers cannot work:** if the exact
   finite transfer operator is built from purely algebraic data, then its
   spectral radius is algebraic, so it cannot equal the transcendental target
   `e^(1/4)`.
3. **One-parameter Gibbs/Perron lifts do not derive the coefficient:** on a
   family `T(mu, theta) = e^mu B(theta)` with positive primitive base operator
   `B(theta)`, the quarter condition is exactly

   `mu = 1/4 - log rho(B(theta))`.

   So exact quarter spectral radius on that class is a **tuning equation** for
   the extra normalization parameter `mu`, not a theorem consequence of the
   operator class.
4. Therefore an exact boundary spectral-radius quarter theorem still needs a
   **new parameter-free gravitational normalization principle** that selects one
   specific operator with `rho = e^(1/4)` internally, rather than by external
   weight choice.

This is stronger than the earlier boundary reduction. It does not just say
"the surviving class is some weighted transfer operator." It says:

> on every currently natural finite-state transfer class, exact quarter either
> fails outright or simply relocates the open bridge into one free
> normalization parameter.

## Inputs

This lane uses the existing boundary reductions plus standard transfer/Perron
logic:

- [PLANCK_SCALE_COLLECTIVE_BOUNDARY_ENTROPY_CARRIER_LANE_2026-04-23.md](./PLANCK_SCALE_COLLECTIVE_BOUNDARY_ENTROPY_CARRIER_LANE_2026-04-23.md)
- [PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md](./PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md)
- [PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md](./PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md)
- [BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md](./BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md)

The upstream boundary reductions already established:

- the current free-fermion RT/Widom carrier misses `1/4` exactly;
- local geometric boundary densities are dead;
- naive independent cell counting is dead;
- finite-state collective counting and finite-dimensional algebraic transfer
  carriers are dead.

This note attacks the sharpened remaining question directly:

> even after allowing a weighted boundary transfer operator, does exact
> `rho = e^(1/4)` become natural, or does it still require a hidden import?

## Setup

On the surviving collective boundary route, the effective entropy density is
carried by the asymptotic pressure of a positive transfer operator:

`s_* = P_grav = lim_(N -> infty) (1/N) log Z_N = log rho(T_grav)`.

Exact conventional Planck on the boundary route requires

`s_* = 1/4`,

equivalently

`rho(T_grav) = e^(1/4)`.

So the whole question reduces to the exact coefficient logic of one positive
operator.

## Theorem 1: Markov/stochastic normalization no-go

Suppose the candidate boundary carrier is normalized as a stochastic transfer
kernel:

- finite or countable state space,
- nonnegative entries,
- each row sum equals `1`.

Then the vector of all ones is a right eigenvector with eigenvalue `1`. By
Perron-Frobenius, the spectral radius of a nonnegative stochastic matrix is

`rho(T) = 1`.

Therefore:

> no stochastic / Markov-normalized boundary carrier can realize exact
> `rho(T) = e^(1/4)`.

### Consequence

If the surviving boundary carrier is real, it cannot be a probability transfer
law or any exact normalization equivalent to one. It must remain an
unnormalized growth / pressure carrier.

## Theorem 2: parameter-free finite algebraic carrier no-go

Let `T` be a finite-dimensional positive transfer operator whose entries are
exact algebraic numbers. Then every eigenvalue of `T`, including its Perron
root, is algebraic.

But the target root is

`e^(1/4)`,

which is transcendental by Lindemann-Weierstrass.

Therefore:

> no parameter-free finite algebraic boundary transfer carrier can realize
> exact `rho(T) = e^(1/4)`.

This restates the previous collective-boundary narrowing in the exact
spectral-radius language.

## Theorem 3: Gibbs/Perron scale-family tuning theorem

Now consider the strongest natural rescue move:

`T(mu, theta) = e^mu B(theta)`,

where:

- `B(theta)` is a positive primitive finite-state transfer operator,
- `theta` denotes the remaining local geometric / combinatorial couplings,
- `mu` is a global surface potential / pressure normalization.

Then spectral radii factor exactly:

`rho(T(mu, theta)) = e^mu rho(B(theta))`.

So the quarter condition is

`e^mu rho(B(theta)) = e^(1/4)`,

hence exactly

`mu = 1/4 - log rho(B(theta))`.

Therefore:

> on every such Gibbs/Perron scale family, exact quarter spectral radius does
> not emerge from the class. It simply defines the unique tuned value of the
> extra normalization parameter `mu`.

### Consequence

This is the exact sense in which the quarter coefficient is still not derived.
Even after admitting a positive collective transfer operator, exact quarter on
that family is only:

- one codimension-one solution surface,
- one renormalization choice,
- one boundary chemical potential,
- or one pressure offset.

It is not a theorem consequence of the finite-state weighted-transfer class.

## Corollary 1: exact quarter is underdetermined on scaled transfer families

Fix any positive primitive base family `B(theta)` for which `rho(B(theta))` is
defined exactly.

Then every allowed `theta` determines one exact value

`mu_*(theta) := 1/4 - log rho(B(theta))`

for which

`rho(T(mu_*(theta), theta)) = e^(1/4)`.

So the quarter condition does not isolate one same-surface operator. It leaves
an entire tuning manifold unless another theorem fixes `mu`.

This is a sharp obstruction to calling the coefficient derived.

## Theorem 4: canonical unscaled Ising-type boundary family still misses the target

Take the standard two-state symmetric nearest-neighbor transfer matrix

`B(J) = [[e^J, e^(-J)], [e^(-J), e^J]]`.

Its eigenvalues are

`lambda_+(J) = e^J + e^(-J) = 2 cosh J`,

`lambda_-(J) = e^J - e^(-J)`.

Hence

`rho(B(J)) = 2 cosh J >= 2`.

But

`e^(1/4) = 1.284025... < 2`.

Therefore:

> the canonical unscaled two-state Gibbs/Ising transfer family cannot realize
> exact quarter spectral radius at all.

The only way to force it on that family is again to introduce an external
scale parameter `mu`, in which case

`mu_*(J) = 1/4 - log(2 cosh J)`.

So even the most natural weighted finite-memory boundary family does not solve
the coefficient problem internally.

## Classification of what is left

After Theorems 1 to 4, exact `rho(T_grav) = e^(1/4)` can only survive in one
of three forms:

1. **direct transcendental import**
   with a local or global weight already containing the target coefficient;
2. **tuned scale-family realization**
   where quarter is achieved by choosing
   `mu = 1/4 - log rho(B(theta))`;
3. **new parameter-free gravitational theorem**
   that constructs one exact same-surface operator whose spectral radius is
   fixed internally to `e^(1/4)`.

Only option 3 would count as a clean Planck derivation on the boundary lane.

## What this closes

This note closes several tempting but still too-weak moves:

- "maybe a stochastic boundary transfer law gives the quarter coefficient";
- "maybe once we allow a weighted transfer operator, the exact coefficient is
  automatic";
- "maybe a canonical finite-memory Gibbs family already prefers `1/4`";
- "maybe exact quarter on a one-parameter weighted family counts as derived."

All of those are now closed negatively.

## What this does not close

This note does **not** prove:

- that a genuinely gravitational infinite-dimensional pressure carrier is
  impossible;
- that a time-locked spacetime boundary operator cannot fix the coefficient;
- that the information/action conversion route is dead;
- that a new parameter-free operator cannot still exist.

It only proves the sharper strategy statement:

> exact boundary pressure `1/4` is not forced by the currently natural
> finite-state transfer classes; it either fails or reduces to tuning a free
> normalization parameter.

## Bottom line

The boundary spectral-radius route survives only in a very narrow form:

- not a stochastic boundary kernel,
- not a parameter-free algebraic transfer operator,
- not a canonical finite-memory Gibbs family by itself,
- and not a scale-family realization unless the scale is independently fixed.

So the exact quarter theorem, if real, still needs a new same-surface
gravitational principle that fixes the boundary pressure internally instead of
through an adjustable normalization.

## Verification

Run:

```bash
python3 scripts/frontier_planck_boundary_spectral_radius_quarter_theorem_lane.py
```

The runner:

1. confirms the target root `e^(1/4)` and pressure `1/4`;
2. checks representative stochastic carriers and verifies `rho = 1`;
3. checks representative parameter-free algebraic positive carriers and
   verifies their Perron roots are algebraic and miss the target;
4. verifies exactly on several primitive base matrices that the scaled-family
   quarter condition is `mu_* = 1/4 - log rho(B)`;
5. verifies on the canonical symmetric Ising family that
   `rho(B(J)) = 2 cosh J >= 2 > e^(1/4)` and therefore misses the target
   without extra scaling;
6. checks the note states the honest classification.

Expected summary:

`PASS = 10, FAIL = 0`.
