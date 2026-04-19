# DM Leptogenesis PMNS Observation-Free Normalization Boundary

**Date:** 2026-04-16  
**Status:** exact current-stack boundary on replacing the observational closure
surface by a native value law  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_observation_free_normalization_boundary.py`

## Question

Can the current exact PMNS-assisted `N_e` stack replace the closure condition

`eta_{i_*} / eta_obs = 1`

by a purely native observation-free value law on the exact reduced domain?

## Bottom line

Not yet.

The current exact branch does expose a clean observation-free family, but not a
derived normalization law.

The selected closure source can be rewritten as a local stationary point of the
one-parameter free-energy family

`Phi_a(H_e) = log F_{i_*}(H_e) - a S_rel(H_e || H_seed)`,

where:

- `F_{i_*}` is the exact favored-column transport functional
- `S_rel` is the exact sole-axiom effective action

But the required coefficient is a tuned number

- `a_* = 0.518479949928...`

and the current branch does not derive it.

More importantly:

- transport extremality alone overshoots
- the natural unit-scale free-energy law underproduces
- the tuned `a_*` law is not itself derived from the current bank
- current bounded observation-free searches do not turn that local rewrite into
  a theorem-grade global selector

So the observational closure surface is still doing real scientific work on the
current branch.

## Exact content

### 1. The current closure source sits inside a one-parameter free-energy family

On the exact reduced `N_e` domain, the selected closure source remains:

- `x_* = (0.471675, 0.553811, 0.664514)`
- `y_* = (0.208063, 0.464383, 0.247554)`
- `delta_* ~ 0`
- `eta / eta_obs = (1.0, 0.75917896, 0.48458840)`

At that point:

- the exact KKT multiplier of the observational closure problem gives
  `a_* = 1 / lambda_* = 0.518479949928...`
- with that `a_*`, the gradient of `Phi_{a_*}` vanishes locally at the closure
  source

So the closure source is compatible with an observation-free free-energy
rewrite.

### 2. Transport extremality alone overshoots

Setting `a = 0` means maximizing the exact transport functional alone.

That exact law selects an off-seed source with

- `eta / eta_obs = 1.05100433...`

so it overshoots the closure value.

Therefore transport extremality by itself is not the missing normalization law.

### 3. The natural unit-scale free-energy law underproduces

Setting `a = 1` gives the obvious unit-scale observation-free free-energy
objective

`log F_{i_*} - S_rel`.

Its global maximizer is a low-action source near the seed and gives

- `eta / eta_obs < 0.9`

So the simplest observation-free combination of exact transport gain and exact
effective-action cost does **not** recover the closure source either.

### 4. The tuned family is not yet a derived global value law

One might hope that using the tuned local coefficient `a_*` would solve the
problem.

Not yet.

What the current branch actually shows is weaker and more precise:

- a bounded observation-free search at the tuned `a_*` does not simply return
  the exact closure source
- that search still lands on an underproducing alternative source
- the current search evidence therefore does **not** upgrade the tuned family
  into a theorem-grade global selector

So the current branch does **not** yet carry a derived observation-free global
value law for the positive PMNS-assisted lane. The exact missing theorem is
still the normalization/value law that fixes `a` natively.

## Consequence

This sharpens the remaining weakness precisely.

What is already closed:

- the exact reduced domain
- the exact favored transport column
- the exact effective-action selector structure
- the exact microscopic Schur-completion quotient

What is still open:

- the observation-free normalization/value law that fixes the coefficient `a`
  and thereby selects the exact closure source without using `eta_obs`
- secondarily, a theorem-grade global uniqueness statement once such a
  normalization law is in hand

So the remaining science is no longer a vague “PMNS might still be open.”
It is one exact missing normalization theorem.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_observation_free_normalization_boundary.py
```
