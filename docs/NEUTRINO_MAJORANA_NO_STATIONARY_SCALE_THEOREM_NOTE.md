# Majorana No-Stationary-Scale Theorem

**Date:** 2026-04-15
**Status:** exact scale-selection no-go on the admitted Majorana source class
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_no_stationary_scale_theorem.py`

## Question

After the Nambu source principle, source-ray theorem, and staircase-blindness
theorem, could the **admitted Majorana Pfaffian/Nambu family itself** already
contain an intrinsic stationary or endpoint selector for the absolute
staircase scale?

Equivalently:

- maybe the current source class is homogeneous only at the level of raw
  structure, but the bosonic generator on that class still hides a preferred
  finite scale
- maybe a hierarchy-style effective-potential or endpoint argument is already
  latent on the Majorana lane

## Bottom line

No.

On the current admitted source class:

1. the one-generation local bosonic generator is exactly

   `W_1(mu) = log(mu) + const`

2. the fixed three-generation `Z_3` lift scales exactly as

   `W_3(lambda) = 3 log(lambda) + const`

3. the remaining exact class invariants are scale-invariant

So the current admitted Pfaffian/Nambu family has **no intrinsic stationary
scale** and **no internal staircase anchor**.

The remaining blocker is therefore even sharper than the staircase-blindness note:

> any full Majorana scale-setting law must introduce a genuinely new
> non-homogeneous ingredient beyond the present admitted source class.

## Inputs

This theorem combines three already-exact Majorana surfaces:

- [NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md](./NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md)
- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md)

Those notes already prove:

1. once the local bilinear lane is admitted, the one-generation bosonic
   generator is uniquely `log|Pf| = log(mu)`
2. the genuinely new one-generation source increment is one ray `mu J_x`
3. the fixed three-generation `Z_3` texture class is homogeneous under
   positive rescaling

So the remaining loophole is narrower:

> maybe the admitted source family is homogeneous as a class, but still has a
> hidden stationary scale as a bosonic system

## Exact theorem

### 1. The one-generation generator is monotone on `mu > 0`

The local Pfaffian-uniqueness theorem gives the exact one-generation generator

`W_1(mu) = log(mu) + const`.

So its exact source derivative is

`dW_1 / dmu = 1 / mu`.

That derivative never vanishes on `mu > 0`.

So the one-generation admitted local Pfaffian lane has no intrinsic stationary
scale.

### 2. The fixed three-generation lift is still only logarithmic in scale

Take any fixed nonzero `Z_3` texture representative `M_0` and scale it by

`M(lambda) = lambda M_0`,  `lambda > 0`.

Then the admitted three-generation pairing block is

`Delta(lambda) = M(lambda) \otimes J_2 = lambda Delta_0`.

Because the one-generation local amplitude is Pfaffian and the `6 x 6`
antisymmetric block has three pairing pairs,

`Pf(Delta(lambda)) = lambda^3 Pf(Delta_0)`.

So the exact scale-sensitive additive generator on that admitted fixed texture
class is

`W_3(lambda) = log|Pf(Delta(lambda))| = 3 log(lambda) + const`,

with exact derivative

`dW_3 / dlambda = 3 / lambda`.

That derivative also never vanishes on `lambda > 0`.

So the admitted three-generation source class still has no intrinsic
stationary staircase anchor.

### 3. The remaining exact class invariants are scale-invariant

The staircase-blindness theorem already implies:

- normalized pairing blocks are unchanged by positive rescaling
- normalized singlet/doublet spectra are unchanged by positive rescaling
- charge classification is unchanged by positive rescaling

So the remaining exact structural data organize the source **class**, but do
not pick its absolute scale.

### 4. Therefore the current admitted source class has no internal scale
selector

On the current admitted source class:

- the scale-sensitive exact bosonic generator is affine in `log(scale)`
- the remaining exact class invariants are scale-invariant

Neither type of exact datum can produce an intrinsic finite stationary scale.

So no exact scale-setting law exists **inside the current admitted
Pfaffian/Nambu family itself**.

## The theorem-level statement

**Theorem (No stationary Majorana scale on the current admitted source
class).**
Assume:

1. the admitted local Nambu/Pfaffian Majorana source class
2. the one-generation source-ray theorem
3. the fixed three-generation `Z_3` texture class
4. the current exact bosonic generator furnished by local Pfaffian uniqueness

Then:

1. the one-generation scale-sensitive generator is `W_1(mu) = log(mu) + const`
   and has no stationary point on `mu > 0`
2. the fixed three-generation lifted generator is
   `W_3(lambda) = 3 log(lambda) + const` and has no stationary point on
   `lambda > 0`
3. the remaining exact class invariants are scale-invariant
4. therefore the current admitted Majorana source class has no intrinsic
   stationary or endpoint selector for the absolute staircase scale

Equivalently: any full Majorana scale-setting law must add a genuinely new
non-homogeneous ingredient beyond the present admitted source class.

## Relationship to the staircase-blindness theorem

The staircase-blindness theorem says the current exact Majorana source stack is
homogeneous under rescaling, so it fixes the source ray and texture class but
not the absolute staircase anchor.

This new theorem is stronger in one specific way:

- it closes the loophole that a hidden stationary or endpoint principle might
  already live **inside the admitted source family**

The answer is still no.

The current source family is not just structurally scale-blind. Its exact
scale-sensitive bosonic generator is also monotone in log-scale.

## Relationship to hierarchy-style selectors

The mainline atlas does contain genuinely non-homogeneous selectors elsewhere,
for example on the hierarchy / EWSB side:

- [HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md](./HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)
- [HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md](./HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md)

But those notes themselves stop at the physical insertion problem, and more
importantly they do **not** descend to the Majorana source family. The current
Majorana lane has no analogous non-homogeneous endpoint structure.

So hierarchy-style exact selectors do not rescue the present Majorana scale
problem.

## What this closes

This closes the last honest loophole of the form:

- maybe the admitted Pfaffian/Nambu family already contains a hidden exact
  stationary-scale principle

Answer: no.

So the branch no longer needs to describe the blocker vaguely as
"find the scale somehow." The remaining theorem target is now precise:

> on the earlier logarithmic observable family, derive some genuinely new
> non-homogeneous Majorana activation / scale-selection principle

Later branch work closes that wording partially: the branch now has both a
local non-homogeneous comparator and a local background-normalized response
curve. So the remaining blocker is narrower:

> derive the finite-point selection / staircase-embedding law on that already-
> normalized local curve, then lift it to the full three-generation
> `A/B/epsilon` amplitudes

## What this does not close

This note does **not** prove:

- that no future framework extension can ever select the scale
- that the universal-theory program is ruled out
- that the final three-generation amplitudes are impossible to derive

It is a theorem about the **current admitted source class** only.

## Safe wording

**Can claim**

- the admitted Majorana Pfaffian/Nambu family has no intrinsic stationary
  scale on the current stack
- the exact scale-sensitive generator is logarithmic in the overall source
  scale
- the remaining exact class invariants are scale-invariant
- on the earlier logarithmic family, no intrinsic stationary scale existed
- later branch work narrows the remaining blocker further to finite-point
  selection on the already-normalized local response curve

**Cannot claim**

- no future extension can ever close the Majorana lane
- the final DM program is impossible in principle

## Command

```bash
python3 scripts/frontier_neutrino_majorana_no_stationary_scale_theorem.py
```
