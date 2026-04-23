# Planck-Scale Collective Boundary Entropy Carrier Lane

**Date:** 2026-04-23  
**Status:** science-only second-wave boundary reduction  
**Audit runner:** `scripts/frontier_planck_collective_boundary_entropy_carrier_lane.py`

## Question

After ruling out:

- the current free-fermion RT/Widom carrier,
- local geometric boundary densities,
- and naive independent cell counting,

can exact conventional

`a = l_P`

still come from a genuinely **collective gravitational boundary entropy
carrier**?

## Verdict

Yes, but only in a much narrower form than "some collective boundary law."

The current exact reduction is:

1. **No finite-state finite-memory collective boundary code can give exact
   effective surface entropy density `s_* = 1/4`.**
2. **More generally, no finite-dimensional collective transfer carrier with
   purely algebraic exact data can give exact `s_* = 1/4`.**
3. Therefore the only serious surviving boundary route is a
   **weighted gravitational Perron / pressure carrier** whose exact spectral
   radius is

   `rho(T_grav) = e^(1/4)`.

That is a real narrowing. It says the surviving boundary route is not just
"collective rather than local." It must also go beyond:

- finite-state combinatorial counting,
- finite-memory hard-constraint codes,
- and finite-dimensional transfer carriers built only from algebraic exact
  numbers.

## Inputs

This lane uses only the already narrowed boundary program plus existing exact
transfer-operator culture in the repo:

- [PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md](./PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_DENSITY_ROUTE_REDUCTION_NOTE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_DENSITY_ROUTE_REDUCTION_NOTE_2026-04-23.md)
- [BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md](./BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md)
- [PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md](./PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md)

The first-wave boundary lane already proved:

- local geometry cannot carry the exact area-law coefficient;
- naive integer tensor-product counting cannot carry exact `a = l_P`;
- any surviving route must therefore be a collective gravitational carrier.

This note tightens that again by classifying which collective carriers are
still impossible.

## Setup

Let a horizon/boundary cross-section be coarse-grained into `N_dA` physical
boundary cells of area `a^2`, so `A = N_dA * a^2`.

If a collective boundary carrier has exact asymptotic state count / partition
law

`Z_N = exp(S_N)` with `N := N_dA`,

define its effective entropy density by

`s_* := lim_(N -> infty) S_N / N`

whenever the limit exists.

Matching Bekenstein-Hawking would then require

`S_N = A / (4 l_P^2) + o(A) = N * a^2 / (4 l_P^2) + o(N)`.

So exact conventional

`a = l_P`

is equivalent to exact effective density

`s_* = 1/4`.

The question is therefore:

> what collective boundary carrier classes can or cannot realize exact
> `s_* = 1/4` without imports?

## Theorem 1: finite-state collective code no-go

Consider any exact finite-state finite-memory collective boundary carrier.
After standard block presentation, its exact word-count / admissible-state
count can be written

`Z_N = u^T A^(N-1) v`

for some nonnegative integer adjacency matrix `A` and nonzero boundary vectors
`u, v`.

By Perron-Frobenius,

`s_* = lim_(N -> infty) (1/N) log Z_N = log rho(A)`,

where `rho(A)` is the Perron spectral radius.

Because `A` has integer entries, every eigenvalue of `A` is an algebraic
integer. In particular `rho(A)` is an algebraic integer.

But exact `s_* = 1/4` would require

`rho(A) = e^(1/4)`.

By the Lindemann-Weierstrass theorem, `e^(1/4)` is transcendental, hence not
an algebraic integer.

Therefore:

> no exact finite-state finite-memory collective boundary code can realize
> exact `s_* = 1/4`.

### Consequence

This rules out a much broader class than naive independent cell counting.
What is closed negatively now includes:

- hard-constraint subshifts of finite type,
- finite-memory boundary tilings,
- finite hidden-Markov/state-machine horizon codes,
- and any exact finite-state collective combinatorics whose asymptotic entropy
  is governed by an integer adjacency matrix.

## Theorem 2: algebraic finite-dimensional transfer no-go

One might try to rescue the route by allowing finite-dimensional collective
transfer weights rather than pure counting:

`Z_N = u^T T^(N-1) v`

with `T` a positive matrix whose entries are exact algebraic numbers.

Then the coefficients of the characteristic polynomial of `T` are algebraic,
so every eigenvalue of `T` is algebraic. In particular `rho(T)` is algebraic,
and again

`s_* = log rho(T)`.

Exact `s_* = 1/4` would require

`rho(T) = e^(1/4)`,

but `e^(1/4)` is transcendental.

Therefore:

> no finite-dimensional collective transfer carrier with purely algebraic
> exact matrix data can realize exact `s_* = 1/4`.

### Consequence

This rules out not only integer combinatorics, but also finite transfer
carriers built purely from exact algebraic data such as:

- rationals,
- radicals,
- finite exact trigonometric character values,
- and other finite algebraic constants.

So the surviving boundary route cannot close on a finite algebraic transfer
matrix alone.

## Surviving candidate class

After these reductions, the strongest surviving collective boundary candidate
class is:

> a same-surface gravitational Perron / pressure carrier with exact positive
> transfer operator `T_grav` such that
>
> `Z_N = Tr(T_grav^N)` or an equivalent exact collective partition law,
>
> and
>
> `rho(T_grav) = e^(1/4)`.

Then

`s_* = lim_(N -> infty) (1/N) log Z_N = log rho(T_grav) = 1/4`,

and exact conventional

`a = l_P`

would follow from the boundary-density route.

This surviving class is structurally natural on this repo, because the
framework already carries exact positive transfer/Perron reductions on other
surfaces, for example
[GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md).

But it is still only a target class, not a closure:

- the local geometric class is already dead,
- the naive counting class is already dead,
- the finite-state collective class is now dead,
- the finite-dimensional algebraic-transfer class is now dead.

So any surviving exact `1/4` theorem has to be a **genuinely weighted,
genuinely gravitational, genuinely collective Perron/pressure theorem**.

## What an acceptable future carrier would have to prove

An acceptable same-surface collective boundary carrier would now need to show:

1. an exact gravitational construction of `T_grav` on the physical boundary /
   horizon surface;
2. positivity or Perron control sufficient to define one canonical leading
   spectral radius;
3. exact asymptotic entropy density
   `s_* = log rho(T_grav)`;
4. exact coefficient
   `rho(T_grav) = e^(1/4)`,
   not by hand, but from the same-surface gravitational data;
5. no hidden import of the coefficient through an externally fixed transcendental
   weight.

## What this closes

This note closes another tempting but wrong class of boundary routes:

- "maybe the right collective finite-state boundary code gives `1/4`";
- "maybe a finite-memory horizon tiling / automaton gives the coefficient";
- "maybe a finite exact transfer matrix with radicals or character values gives
  the Perron root."

All of those classes now close negatively.

## What this does not close

This note does **not** prove:

- the existence of the required `T_grav`;
- that the surviving carrier is finite-dimensional or infinite-dimensional;
- that the exact coefficient can already be derived from the current admitted
  gravity/action stack;
- that the information/action route is dead.

It only proves the sharper strategy statement:

> if the boundary route survives, it survives as a genuinely weighted
> gravitational Perron/pressure theorem with exact spectral radius `e^(1/4)`,
> not as any finite-state or finite-algebraic collective combinatorics.

## Verification

Run:

```bash
python3 scripts/frontier_planck_collective_boundary_entropy_carrier_lane.py
```

The runner:

1. verifies `exp(1/4)` is transcendental on the symbolic backend;
2. checks representative integer adjacency examples and confirms their Perron
   roots are algebraic integers and do not equal `exp(1/4)`;
3. checks representative algebraic weighted transfer matrices and confirms
   their Perron roots are algebraic and do not equal `exp(1/4)`;
4. constructs a positive weighted Perron witness with exact spectral radius
   `exp(1/4)` to show what the surviving carrier class would have to look like;
5. verifies the witness has asymptotic entropy density `1/4`;
6. confirms that this note states the correct surviving class honestly.
