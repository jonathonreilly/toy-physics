# DM Selector Threshold Stabilization Support Theorem

**Date:** 2026-04-21  
**Status:** selector-side support theorem on the open DM gate  
**Primary runner:** `scripts/frontier_dm_selector_threshold_stabilization_support_2026_04_21.py`

## Statement

The exact intrinsic threshold-volume selector family on the recovered DM bank
already contains a nontrivial high-threshold stabilization window.

More precisely, let `V_tau(H)` be the canonical full-family witness-volume
selector already isolated in
`docs/DM_NEUTRINO_SOURCE_SURFACE_ATOMIC_WITNESS_VOLUME_SELECTOR_NONREALIZATION_NOTE_2026-04-18.md`.
On the recovered bank of five lifts, the preferred recovered lift

```text
lift 0 = (1.021038842009447, 1.380791428981559, 0.215677476525045)
```

is not selected at every threshold, but it does become the unique minimizer of
`V_tau` immediately above one exact crossover value

```text
tau_star = 0.131637578221552...
```

and it remains the unique minimizer until the next lift first reaches zero
witness volume, at

```text
tau_zero(next) = 0.271641142726493...
```

So the remaining selector-side burden is narrower than “derive an arbitrary
threshold law.” It is enough to derive an intrinsic threshold law whose value
lands in this exact stabilization window.

## Inputs already on branch

### 1. Exact intrinsic threshold-volume family

The existing nonrealization theorem already proved that on one common positive
comparison window `A_mu(H) = H + mu I > 0`, the full-family Haar witness-volume
field

```text
V_tau(H) = Vol{P rank-one positive : W(A_mu(H); P) >= tau}
```

is:

- exact,
- intrinsic / basis-free,
- presentation-blind,
- and fully determined by the atomic singleton response field.

It also proved the current-bank nonrealization fact:

- at `tau = 0.13`, the unique minimizer is recovered lift `1`;
- at `tau = 0.14`, the unique minimizer is recovered lift `0`.

So the missing datum was already narrowed to an intrinsic threshold law.

### 2. Recovered bank and preferred lift

The selector support module fixes:

- the recovered bank of five lifts,
- the preferred recovered lift `0`,
- and one common positive shift `mu_bank`.

No new candidate forest or new microscopic data are introduced here.

## Exact spectral parameters

For each recovered lift, let

```text
a_i >= b_i >= g_i > 0
```

be the inverse eigenvalues of `A_mu(H_i)`.

On the recovered bank these are:

```text
lift 0: (a,b,g) = (0.241586090133, 0.159554932108, 0.128322735096)
lift 1: (a,b,g) = (0.312116054425, 0.192893545828, 0.114894973603)
lift 2: (a,b,g) = (0.330338253485, 0.194080510339, 0.114930915644)
lift 3: (a,b,g) = (0.522540316974, 0.186733773140, 0.111923120733)
lift 4: (a,b,g) = (5.000000000000, 0.174138550828, 0.107108917667)
```

The exact piecewise formula from the earlier note gives `V_tau(H_i)` as a
closed-form function of `(a_i, b_i, g_i)` and `c = exp(tau) - 1`.

## New theorem

### Pairwise crossover structure

Comparing the preferred lift `0` against each competitor gives one relevant
high-threshold crossover:

```text
tau_04 = 0.122908754273491...
tau_03 = 0.128170243960314...
tau_02 = 0.130612182569963...
tau_01 = 0.131637578221552...
```

The last crossover is therefore

```text
tau_star = tau_01 = 0.131637578221552...
```

Immediately above `tau_star`, the preferred lift is already below all four
competitors.

### Zero-volume ordering

The preferred lift also has the smallest terminal inverse eigenvalue:

```text
tau_zero(0)    = log(1 + a_0) = 0.216389667205294...
tau_zero(next) = min_{j>0} log(1 + a_j) = 0.271641142726493...
```

So on

```text
tau in [tau_zero(0), tau_zero(next))
```

the preferred lift has exactly zero witness volume while every competing lift
still has strictly positive witness volume.

### Support theorem

**Support theorem.** On the recovered bank, the preferred recovered lift is
the unique minimizer of the exact intrinsic threshold-volume selector family
for every

```text
tau in (tau_star, tau_zero(next)).
```

The interval is nonempty and explicit:

```text
(0.131637578221552..., 0.271641142726493...).
```

## Consequence

This does not close the selector law.

It does, however, sharpen the open object. The branch no longer needs an
arbitrary microscopic threshold law. It needs one that lands in the exact
stabilization window already present in the intrinsic threshold-volume family.

So the right-sensitive selector-side target is now:

1. derive an intrinsic threshold law landing in the stabilization window; or
2. derive a stronger microscopic law that bypasses the threshold family
   entirely.

Either way, the selector target is more structured than it was before this
theorem.

## Boundary

This is a support theorem, not flagship closure.

It does **not** prove that the true microscopic selector must factor through
the threshold-volume family alone. It proves only that once one works inside
that exact intrinsic family, the preferred recovered lift already has a broad
high-threshold stabilization window.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_selector_threshold_stabilization_support_2026_04_21.py
```

Expected result:

```text
PASS=14 FAIL=0
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [scalar_selector_remaining_open_imports_2026-04-20](SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md)
