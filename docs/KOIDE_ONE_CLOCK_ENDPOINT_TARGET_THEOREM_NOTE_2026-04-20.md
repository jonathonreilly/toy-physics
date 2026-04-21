# Koide One-Clock Endpoint Target Theorem

**Date:** 2026-04-20  
**Status:** exact constructive reduction on current `main`  
**Runner:** `scripts/frontier_koide_one_clock_endpoint_target_theorem_2026_04_20.py`

## Question

After the April 18 charged-lepton support stack and the retained anomaly-forced
time theorem, what is the single highest-value theorem target left on the
positive Koide route?

## Bottom line

It is now exactly one endpoint law.

More precisely, the current-main constructive charged-lepton Koide lane has
been reduced to:

```text
derive one ambient one-clock endpoint law for

  m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3

on the selected generator line

  G_m = H(m, sqrt(6)/3, sqrt(6)/3).
```

Equivalent forms of the same remaining target are:

- derive the selected-line endpoint value `m_*`,
- derive the microscopic scalar `Re K12`,
- derive the cyclic-response bridge `kappa(m)`,
- derive the reachable-slot ratio `r(m) = w(m)/v(m)`.

Any retained ambient one-clock law fixing that endpoint already closes the
remaining internal coordinates on the current positive route.

## Input stack

This note synthesizes five existing retained-main results:

1. [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)
2. [KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md)
3. [KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md)
4. [KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md)
5. [KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md)

## Theorem 1: the native ambient grammar is one-clock `3+1`

The retained anomaly-forced-time theorem closes the ambient physics grammar as:

```text
d_t = 1 uniquely,
spacetime is 3+1 dimensional.
```

So any framework-native constructive completion must live inside a one-clock
ambient `3+1` evolution law, not in an unconstrained multi-time or purely
static algebraic ansatz.

## Theorem 2: the one-clock Koide search is already collapsed to one real line

The positive one-clock semigroup theorem proves that any repeated-step positive
law on the reachable charged-lepton block has the exact form

```text
X_beta = exp(beta G)
```

for one Hermitian generator `G`.

The observable-selector theorem then fixes

```text
delta = q_+ = sqrt(6)/3,
```

so the generator search is no longer a multi-real chart. It is the one-real
selected family

```text
G_m = H(m, sqrt(6)/3, sqrt(6)/3).
```

That line already contains the near-exact charged-lepton witness.

## Theorem 3: on the selected line, closing the route means fixing one endpoint

The selected-line closure note proves:

1. the physical branch is fixed by continuity from the positivity threshold;
2. once one scale-free endpoint value is fixed, the whole normalized
   charged-lepton direction is fixed;
3. the current positive route closes internally at the first continuous hit of
   the witness ratio.

So the remaining open problem is not "choose more internal coordinates."
It is:

```text
fix the selected endpoint on the one-real line.
```

## Theorem 4: that endpoint is exactly one microscopic scalar

The microscopic scalar selector note proves that on the selected slice:

```text
m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3
```

and every other exact source / slot / CP datum on that slice is frozen.

It also proves that on the physical first branch:

```text
m <-> kappa(m) <-> r(m) = w(m)/v(m)
```

is one-to-one.

So the endpoint problem is exactly one microscopic scalar problem.

## Corollary: the highest-value theorem target is one ambient endpoint law

Combining Theorems 1-4:

> The strongest remaining constructive target on current `main` is to derive a
> one-clock ambient `3+1` endpoint law for the selected-line microscopic scalar
>
> ```text
> m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3.
> ```
>
> Any retained law fixing that endpoint already fixes `kappa`, the reachable
> ratio `r = w/v`, the selected-line point, and therefore the full internal
> charged-lepton Koide candidate route.

This is the cleanest current statement of "what to work on next" that the repo
supports exactly.

## Why this is the right next theorem

This theorem target is stronger than the older formulations:

- not "derive a full parent law",
- not "derive a generic readout",
- not "derive a whole matrix selector",
- not even "derive a free selected point in a multi-real chart".

It is only:

```text
derive one ambient one-clock endpoint law for one microscopic scalar.
```

That is the smallest constructive charged-lepton target currently visible on
`main`.

## Scope boundary

This note does **not** yet derive that endpoint law.

It proves something narrower but useful:

- the ambient grammar is fixed,
- the generator family is fixed to one real line,
- the branch is fixed,
- and the endpoint target is fixed to one microscopic scalar.

So the live theorem burden is now singular and explicit.

## Forward use

If the actual-route Berry/Brannen lane is later promoted, this is also the
right native object to attack on that side: the selected-line phase problem can
only close by fixing the corresponding one-clock endpoint on the charged-lepton
ambient route.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_one_clock_endpoint_target_theorem_2026_04_20.py
```
