# Weak-Coupling Retention Note

**Date:** 2026-04-11 (status line narrowed 2026-04-28 per audit-lane verdict)
**Script:** `frontier_weak_coupling_retained.py`
**Status:** bounded conditional sign-sensitive weak-coupling regime on the selected finite audit surface — the runner verifies shell-ordering 60/60 and shell margin 60/60, but the registered runner path is wrong, the secondary gap count is live-stale at 54/60, and the note's broader inference (theorem for admissible irregular bipartite graphs, coordinate-force closure, stable secondary spectral-gap row) is not closed by the current packet.

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

## Stable Pass Counts

The runner was rerun four times in the physics venv. Three observables were
stable across all four reruns:

- width asymmetry `< 1`: `56/60`
- shell strict split: `47/60`
- shell ordered (`tw_a > tw_r`): `60/60`
- shell margin `>= 10`: `60/60`
- norm conserved: `60/60`

Stable by-family counts:

- random geometric:
  - width: `20/20`
  - shell strict: `11/20`
  - shell ordered: `20/20`
  - shell margin: `20/20`
- growing:
  - width: `16/20`
  - shell strict: `16/20`
  - shell ordered: `20/20`
  - shell margin: `20/20`
- layered cycle:
  - width: `20/20`
  - shell strict: `20/20`
  - shell ordered: `20/20`
  - shell margin: `20/20`

## Unstable Secondary Observable

The spectral-gap tally is not stable enough to freeze as an exact retained
count. Across four identical reruns, the script reported:

- gap ratio `> 1`: `55/60`, `56/60`, `57/60`, `55/60`
- growing-family gap count: `15/20`, `16/20`, `17/20`, `15/20`

So the gap ratio remains a useful supporting indicator, but not a frozen
retained row. The retained claim below relies only on the stable shell-force
and norm observables.

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

Width asymmetry is stable but not universal enough to carry retention by
itself. Spectral gap ratio is directionally useful, but its exact pass count is
runner-sensitive and is therefore not frozen here.

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

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, medium criticality, 16 transitive
descendants):

> Issue: the finite runner verifies shell ordered 60/60, shell margin
> >=10 on 60/60, and norm conservation 60/60, but the note promotes
> this selected audit surface to a retained weak-coupling sign-
> sensitive regime while the registered runner path is wrong and the
> secondary gap count is live-stale at 54/60. Why this blocks: a
> hostile auditor can accept the finite shell-margin table but cannot
> infer a theorem for admissible irregular bipartite graphs, a
> coordinate-force closure, or a stable secondary spectral-gap row
> from the current packet.

## What this note does NOT claim

- A theorem for admissible irregular bipartite graphs.
- A coordinate-force closure.
- A stable secondary spectral-gap row (current count is 54/60,
  live-stale).
- A correctly registered runner path; the registered path is wrong.

## What would close this lane (Path A future work)

Promoting from bounded conditional to retained would require:

1. Fixing the registered runner path.
2. Adding explicit hard PASS thresholds for shell-ordering, shell
   margin, secondary spectral-gap stability, and norm conservation.
3. Refreshing the secondary gap count to 60/60 (currently 54/60).
4. Either narrowing the claim to the finite shell-margin diagnostic
   or registering separate audit-clean theorems for the broader
   inferences.
