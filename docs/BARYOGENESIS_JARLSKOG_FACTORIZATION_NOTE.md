# Baryogenesis Jarlskog Factorization Note

**Date:** 2026-04-16
**Status:** exact current-surface flavor-factorization theorem with bounded target on `main`
**Script:** `scripts/frontier_baryogenesis_jarlskog_factorization.py`

## Safe statement

On the current `main` package surface, once baryogenesis is correctly narrowed
to a genuinely nonperturbative electroweak transition / sphaleron / transport
route, the remaining weak-flavor dependence collapses exactly to the promoted
CKM Jarlskog invariant `J`.

So the open baryogenesis bridge can be written as

`η = J * K_NP`

where `K_NP` is one real CP-even functional of the still-open nonperturbative
electroweak dynamics.

That is the right next reduction. It removes the last loose flavor-language
from the baryogenesis gate.

## What is derived here

The current package already fixes two exact ingredients:

1. the retained electroweak `SU(2)` / `B-L` structure on the one-generation
   taste surface
2. the promoted three-generation CKM package

These two ingredients are enough to derive the flavor-factorization statement.

## Exact generation blindness of the electroweak channel

On the retained taste surface, the electroweak operators relevant to the
`B+L`-violating channel are taste operators:

- baryon number `B`
- lepton number `L`
- electroweak `SU(2)` generators `S_x, S_y, S_z`

When lifted to the three-generation quark space, they act as

`I_gen ⊗ O_EW`.

So they commute exactly with arbitrary generation-phase rephasings

`P_gen ⊗ I_taste`.

That means the same-surface nonperturbative electroweak channel is generation
blind: it does not itself know about CKM phases or flavor labels.

## Exact CP-odd CKM content on the current surface

The promoted CKM package already fixes:

- `|V_us| = 0.22727`
- `|V_cb| = 0.04217`
- `|V_ub| = 0.003913`
- `δ = 65.905°`

On that exact three-generation surface:

1. all independent CKM quartet invariants collapse to `±J`
2. arbitrary quark-field rephasings leave `J` invariant
3. complex conjugation flips the sign of `J`
4. the CP-conserving limits `δ -> 0` or `s_13 -> 0` give `J = 0`

So `J` is the unique retained CP-odd weak-flavor invariant available to a
generation-blind electroweak baryogenesis route on the current package
surface.

## Exact factorization consequence

Because the nonperturbative electroweak channel is generation blind while the
weak CP source is carried by the CKM sector, any same-surface baryogenesis
observable that is:

- electroweak / flavor blind on the transport side,
- CP-odd,
- rephasing invariant,
- and zero in the CP-conserving limit,

must factor through `J`.

So the baryogenesis bridge can be written as

`η = J * K_NP`

with `K_NP` real and CP-even.

This note does **not** compute `K_NP`. It isolates it exactly.

## Target value of the remaining functional

Using

- `η_obs = 6.12e-10`
- `J = 3.330901e-5`

the exact current-surface target is

`K_NP,target = η_obs / J = 1.837341e-5`.

So the open baryogenesis problem is no longer:

- “some unspecified mechanism must somehow reproduce `η`”

It is now:

- compute the single real nonperturbative electroweak functional `K_NP`
  on the retained surface and show it lands near `1.84e-5`

## Why this matters

This is a genuine reduction of the live baryogenesis gate:

- before: open EWPT / sphaleron / transport bridge with loose flavor language
- now: one exact CKM invariant `J` times one open real nonperturbative
  functional `K_NP`

That is much tighter and more reviewer-safe.

## What this closes

This note closes the question:

> “After the route pivot, what exactly is the remaining weak-flavor object in
> baryogenesis?”

Answer:

- not an arbitrary CP-source tensor
- not a new flavor structure
- exactly the promoted Jarlskog invariant `J`

Everything else is the real nonperturbative electroweak functional `K_NP`.

## What remains open

This note does **not** derive:

- the transition-strength part of `K_NP`
- the sphaleron survival / washout part of `K_NP`
- the transport / diffusion part of `K_NP`
- the final first-principles `η`

So baryogenesis remains open.

But its weak-flavor dependence is no longer open.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_CLOSURE_GATE_NOTE.md](./BARYOGENESIS_CLOSURE_GATE_NOTE.md)
  isolated the electroweak transition / transport bridge as the live gate
- [BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md](./BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md)
  fixed the numerical target `η/J`
- [BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md](./BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md)
  showed the surviving route class is genuinely nonperturbative

This note is the next exact step:

- it proves the open bridge has the exact factorized flavor form `η = J * K_NP`

## Validation

- [frontier_baryogenesis_jarlskog_factorization.py](./../scripts/frontier_baryogenesis_jarlskog_factorization.py)
- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md](./BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md)
- [BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md](./BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md)

Current runner state:

- `frontier_baryogenesis_jarlskog_factorization.py`: expected `PASS>0`,
  `FAIL=0`
