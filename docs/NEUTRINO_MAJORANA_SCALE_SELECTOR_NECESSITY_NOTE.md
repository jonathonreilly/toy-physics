# Majorana Scale-Selector Necessity

**Date:** 2026-04-15  
**Status:** exact historical necessity theorem on the earlier logarithmic
observable family; superseded in part by the later quadratic-comparator and
background-normalization theorems  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_scale_selector_necessity.py`

## Question

After the positive local Nambu radial observable and the negative
no-stationary-scale theorem, can a **canonically meaningful finite Majorana
scale selector** be built from the current exact observables alone?

This is the sharper form of the remaining blocker:

- maybe the current branch already has enough observables
- maybe the missing ingredient is just a more clever equation among them
- maybe we do not need a genuinely new pairing-sector comparator after all

## Bottom line

On the earlier logarithmic observable family alone: no.

On that earlier observable set, the exact observables split into two
types only:

1. **scale-sensitive generators** that are affine in `t = log(scale)` up to
   additive constants
2. **class data** that are exactly scale-invariant

That has two consequences:

1. any value-based selector built from the current logarithmic generators
   depends on unfixed additive constants and is therefore not canonical
2. any additive-shift-invariant differential selector built from their
   derivatives or curvatures is scale-independent and therefore cannot pick a
   finite scale

At that stage, any successful Majorana scale selector had to add one of:

1. a genuinely new **non-homogeneous** pairing-sector comparator
2. a canonically fixed endpoint / background normalization that ties the
   additive constants to a physical reference surface

## Inputs

This theorem sits directly on the earlier local stack:

- [NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md)
- [NEUTRINO_MAJORANA_NO_STATIONARY_SCALE_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_NO_STATIONARY_SCALE_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)

The current exact branch now knows:

1. the admitted local Nambu family carries the positive local bosonic
   observable

   `W_N(s) = log ||s|| + const`

2. on the pure-pairing ray this reduces to

   `W_M(mu) = log(mu) + const`

3. the fixed three-generation `Z_3` lift carries

   `W_3(lambda) = 3 log(lambda) + const`

4. the remaining exact class invariants are scale-invariant

So the only remaining loophole is:

> maybe those observables already determine a finite scale when combined in a
> smarter way

## Exact theorem

### 1. The current scale-sensitive observables are only logarithmic

On the admitted source class, the current exact scale-sensitive generators are:

- `W_M(mu) = log(mu) + const`
- `W_N(s) = log ||s|| + const`
- `W_3(lambda) = 3 log(lambda) + const`

So in the logarithmic scale coordinate `t = log(lambda)` they are all affine:

- `a t + b`

with fixed slope `a` and unfixed additive constant `b`.

They have zero curvature in `t`.

### 2. The remaining exact class data are scale-invariant

The staircase-blindness theorem already proves:

- normalized pairing blocks are unchanged by rescaling
- normalized singlet/doublet spectra are unchanged by rescaling
- charge classification is unchanged by rescaling

So the remaining exact class data carry no scale derivative at all.

### 3. Value-based selectors are not canonical

A value-based selector from the current generators would equate or combine
quantities like:

- `W_M`
- `W_N`
- `W_3`

But each is defined only up to an additive constant.

So any finite scale extracted from their raw values shifts when those additive
constants are shifted.

Therefore such a selector is not canonical on the present stack.

### 4. Shift-invariant differential data are scale-independent

To remove the additive ambiguity, one can pass to:

- derivatives in `t = log(lambda)`
- derivative ratios
- curvatures

But for the current logarithmic generators:

- first derivatives are constants
- derivative ratios are constants
- second derivatives vanish

So every additive-shift-invariant differential datum available on the present
source class is itself scale-independent.

Therefore no finite critical scale can be selected from those data alone.

## The theorem-level statement

**Theorem (Historical necessity on the logarithmic Majorana observable
family).**
Assume the earlier admitted Majorana source class on branch
`codex/dm-main-derived`, together with:

1. the current exact logarithmic scale-sensitive generators
2. the current exact scale-invariant class data
3. the existing additive-constant freedom of those logarithmic generators

Then:

1. every current scale-sensitive exact observable is affine in `log(scale)`
2. every current exact class invariant is scale-independent
3. every value-based selector built from the current logarithmic observables is
   non-canonical because it depends on unfixed additive constants
4. every additive-shift-invariant differential selector built from the same
   observables is scale-independent
5. therefore no canonically meaningful finite Majorana scale selector exists
   on that earlier logarithmic observable family

Equivalently: at that stage any future exact Majorana scale selector had to add
either a genuinely new non-homogeneous comparator or a canonically fixed
endpoint/background normalization.

## What this closes

This closes the last weak escape hatch:

- maybe the current branch already has the right observables, and only lacks
  a better combination of them

Answer: no.

At that stage the current branch had:

- the positive local Nambu-complete bosonic observable
- the negative no-stationary-scale theorem
- and now the necessity theorem saying why no canonical finite selector can be
  built from the current observable family alone

## Later development

Two later local theorems now close one branch of this old necessity result
positively:

1. [NEUTRINO_MAJORANA_NAMBU_QUADRATIC_COMPARATOR_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_QUADRATIC_COMPARATOR_NOTE.md)
   supplies the exact local non-homogeneous comparator `Q_2 = ||s||^2`
2. [NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md)
   supplies the exact local background-normalized response curve
   `W_rel = (1/2) log(1 + rho^2)`, `Q_rel = rho^2`

So the live blocker is now narrower than this old note:

> finite-point selection on the already-normalized local response curve

## Minimal successful next invention

This theorem does not only block. It also specifies the target.

On the earlier logarithmic family, any successful new Majorana comparator had
to do at least one of the following:

1. provide a new pairing-sector observable `C(lambda)` whose response is
   **not** affine in `log(lambda)`
2. provide a canonically fixed endpoint/background surface that removes the
   additive ambiguity between the current logarithmic generators
3. provide a new charge-`2` primitive carrying a second exact scaling weight
   or critical datum beyond the present admitted Pfaffian/Nambu class

In other words, the branch no longer needs a vague request for "some scale law."
It now has an exact specification for the missing object.

## Relationship to the current blocker notes

At the time, this theorem sharpened the denominator blocker from:

> derive a genuinely new non-homogeneous Majorana activation /
> staircase-selection law

to:

> derive a new pairing-sector comparator with either non-logarithmic scale
> response or canonically fixed endpoint/background normalization

That is the real last-mile theorem target now.

## What this does not close

This note does **not** prove:

- that such a new comparator is impossible in principle
- that the universal-theory program is ruled out
- that no future charge-`2` primitive can provide the missing datum

It is a necessity theorem on the **earlier logarithmic admitted source
family**.

## Safe wording

**Can claim**

- on the earlier logarithmic observable family alone, no canonical finite
  scale selector existed
- the later local comparator/background-normalization theorems close one
  branch of this old blocker positively
- the remaining gap is now finite-point selection on the already-normalized
  response curve

**Cannot claim**

- no future extension can ever close the Majorana lane

## Command

```bash
python3 scripts/frontier_neutrino_majorana_scale_selector_necessity.py
```
