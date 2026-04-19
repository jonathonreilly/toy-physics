# Quark Up-Amplitude sqrt(7) Counterexample Simplification

**Date:** 2026-04-19  
**Status:** bounded simplification of the exact denominator-side
counterexamples to the direct `sqrt(7)` anchored law  
**Primary runner:**
`scripts/frontier_quark_up_amplitude_sqrt7_counterexample_simplification.py`

## Safe statement

The direct anchored support law

```text
a_u = sqrt(5/6) * (6/7 - delta_A1 / sqrt(7))
```

is **not** the endpoint of the current exact search surface.

On a bounded denominator-side exact grammar, there are multiple exact
counterexamples with better anchored CKM+`J` score than the direct `sqrt(7)`
law.

This note compresses that raw "many beaters" result to the smallest honest
bounded statement:

- the simplest exact beater is the projector-rescaled denominator
  `sqrt(42/5) = sqrt(7) / sqrt(5/6)`;
- the strongest current bounded two-step beater is `2 + sqrt(5/6)`;
- the remaining beaters are higher-complexity variants in the same narrow
  lifted-denominator window above `sqrt(7)`.

That is a bounded counterexample classification, not a retained derivation.

## Denominator-side setup

Stay on the exact-support anchor already fixed elsewhere on this branch:

- `delta_A1(q_dem) = 1/42`
- `sin(delta_std) = sqrt(5/6)`
- support base `6/7`

and write the denominator-dressed amplitude as

```text
a_u(D) = sqrt(5/6) * (6/7 - delta_A1 / D).
```

The direct anchored law is the benchmark denominator

```text
D0 = sqrt(7).
```

On this branch that gives

- `a_u = 0.774245730253`
- anchored aggregate CKM+`J` deviation `0.722589%`
- full-package refit max deviation `1.062090%`

So this is already strong, but not obviously optimal.

## Bounded denominator grammar

The simplification lane tests a deliberately small exact denominator grammar
built from the atoms

```text
{sqrt(7), sqrt(5/6), 2, 1}
```

with one-step and one-more-step exact operations

```text
x + y
x - y
x * y
x / y
sqrt(x * y)
1 - x
```

restricted to positive denominators that still produce a physical-band
amplitude.

This is not a theorem grammar. It is a bounded counterexample audit designed to
compress the live exact beater set cleanly.

The runner finds:

- `429` distinct positive denominators in the bounded grammar
- `17` exact denominators that beat the direct `sqrt(7)` anchored law

The raw beaters break down as:

- complexity `3`: `2`
- complexity `5`: `7`
- complexity `6`: `8`

So the question is no longer whether beaters exist. The question is whether
they compress to a small exact representative set.

## Minimal representatives

### Simplest exact beater

The first clean beater is

```text
D = sqrt(42/5) = sqrt(7) / sqrt(5/6).
```

It gives

- `a_u = 0.774961501337`
- anchored aggregate `0.716378%`
- full-package refit max `1.031008%`

So one exact projector rescaling of the direct `sqrt(7)` denominator already
captures most of the bounded improvement.

In fact, this simplest beater captures about `95.9%` of the full anchored gain
achieved by the strongest bounded two-step counterexample.

### Strongest bounded two-step beater

The best exact two-step denominator in the bounded grammar is

```text
D = 2 + sqrt(5/6).
```

It gives

- `a_u = 0.774999078203`
- anchored aggregate `0.716114%`
- full-package refit max `1.029376%`

So the strongest bounded two-step lift is only slightly stronger than the
projector-rescaled beater.

### What the raw beater set reduces to

Once the raw `17` beaters are sorted by score and complexity, the honest
compression is:

1. **projector-rescaled representative:** `sqrt(42/5)`
2. **additive projector-lift representative:** `2 + sqrt(5/6)`

Everything else is a higher-complexity denominator sitting in the same narrow
window

```text
2.659075191684 <= D <= 2.955442792204
```

with no simpler formula beating those two representatives on the axis that
matters here.

## Why they beat `sqrt(7)`

The mechanism is simple and bounded.

At fixed support base,

```text
a_u(D) = sqrt(5/6) * (6/7 - delta_A1 / D)
```

so increasing `D` above `sqrt(7)` reduces the subtraction term `delta_A1 / D`.
That lifts `a_u` upward relative to the direct law.

This is exactly what happens in every bounded counterexample found here:

- every beater satisfies `D > sqrt(7)`
- every beater therefore weakens the direct `delta_A1 / sqrt(7)` subtraction
- the resulting `a_u` moves from `0.7742457...` into the narrow improved band
  near `0.77496 - 0.77511`

So the denominator-side counterexample mechanism is not mysterious. The direct
`sqrt(7)` law simply subtracts a little too much on the current exact-support
anchor, and the beater family consists of exact lifts of that denominator.

## Exact endpoint

The clean endpoint of this lane is:

- the raw "many beaters" result **does** compress sharply;
- it does **not** compress to one forced exact law;
- it compresses to two canonical exact representatives:
  `sqrt(42/5)` and `2 + sqrt(5/6)`;
- the remaining beaters are higher-complexity variants in the same narrow
  denominator window.

So the sharpest current bounded statement is:

> the direct `sqrt(7)` anchored law is not isolated; the smallest exact
> denominator-side counterexamples are the projector-rescaled beater
> `sqrt(42/5)` and the stronger bounded two-step beater `2 + sqrt(5/6)`, but
> this lane still does not force a unique theorem-grade replacement law.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_sqrt7_counterexample_simplification.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_sqrt7_counterexample_simplification.py`:
  `PASS=7 FAIL=0`
