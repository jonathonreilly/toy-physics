# Weak-Coupling Retention Note

**Date:** 2026-04-11  
**Script:** `frontier_weak_coupling_retained.py`  
**Status:** retained sign-sensitive regime, narrowly and explicitly

## Question

Can the weak-coupling parity-coupled irregular-graph regime be frozen as a
retained sign-sensitive result on a broader family/size/seed surface, or does
it remain exploratory?

This note answers that question narrowly. It does **not** claim a universal
off-lattice directional-force closure across all operating points. It only
freezes what survives under the audited weak-coupling surface.

## Audited Surface

- graph families:
  - random geometric
  - growing
  - layered cycle
- sizes:
  - random geometric: `side=8`, `side=10`
  - growing: `n_target=64`, `n_target=100`
  - layered cycle: `8x8`, `10x10`
- seeds: `42..46`
- couplings: `G=5`, `G=10`
- total runs: `60`
- evolution:
  - `N_ITER = 40`
  - `DT = 0.12`
  - parity coupling `(m + Phi) * epsilon`

Each run compares:

- attractive parity coupling
- repulsive parity coupling
- zero-field control

## Observables and Gates

The audit measured four sign-sensitive candidates:

1. `width_asymmetry < 1`
   - contraction under attraction divided by contraction under repulsion
2. `gap_ratio > 1`
   - spectral gap under attraction divided by spectral gap under repulsion
3. `shell_strict`
   - `tw_a >= 36` and `tw_r <= 4`
4. `shell_margin`
   - `tw_a - tw_r >= 10`

Norm conservation was also required:

- `| ||psi|| - 1 | < 1e-10` for both attractive and repulsive runs

## Exact Pass Counts

Across the full `60`-run audited surface:

- width asymmetry `< 1`: `56/60`
- gap ratio `> 1`: `56/60`
- shell strict split: `47/60`
- shell ordered (`tw_a > tw_r`): `60/60`
- shell margin `>= 10`: `60/60`
- norm conserved: `60/60`

By family:

- random geometric:
  - width: `20/20`
  - gap: `20/20`
  - shell strict: `11/20`
  - shell margin: `20/20`
- growing:
  - width: `16/20`
  - gap: `16/20`
  - shell strict: `16/20`
  - shell margin: `20/20`
- layered cycle:
  - width: `20/20`
  - gap: `20/20`
  - shell strict: `20/20`
  - shell margin: `20/20`

## Strongest Sign-Selective Observable

The strongest retained observable is:

> **shell-force margin**
>  
> `tw_a - tw_r >= 10` on `60/60` audited runs

This is stronger than a trivial ordering test. On the full audited surface,
attraction exceeds repulsion by at least `10` TOWARD-count steps out of `40`
in every single run.

The weaker but still useful supporting observables are:

- width asymmetry
- spectral gap ratio

They are real, but not universal enough to carry retention by themselves.

## Retained Claim

The weak-coupling regime can now be frozen as a retained **sign-sensitive
regime** on admissible irregular bipartite graphs, with this exact wording:

> At weak coupling (`G=5,10`), attractive parity coupling produces a uniformly
> larger shell-force TOWARD count than repulsive parity coupling across the
> audited irregular graph surface (`60/60` runs), with a minimum separation of
> `10/40` steps and exact norm conservation.

## What This Still Does NOT Claim

This does **not** establish:

- universal off-lattice directional gravity at all operating points
- coordinate-force closure on irregular graphs
- that width asymmetry or gap ratio are themselves retained universal rows

So the blocker is only partially resolved:

- weak-coupling sign sensitivity is now retained
- full irregular off-lattice directional closure outside this regime remains a
  separate question

## Practical Use

Use this result when the scientific claim is specifically about:

- weak-coupling irregular-graph sign sensitivity
- retained attractive-vs-repulsive separation at low `G`
- graph-native sign selection without coordinate-force reconstruction

Do **not** use it to replace the exact-force cubic card or to overstate the
status of the broader irregular directional-observable blocker.
