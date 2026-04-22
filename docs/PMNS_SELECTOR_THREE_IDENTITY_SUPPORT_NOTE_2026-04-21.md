# PMNS Selector Three-Identity Support Note

**Date:** 2026-04-21  
**Status:** Support proposal on the affine Hermitian PMNS chart. Not a retained
closure theorem.

## Statement

Consider the retained affine Hermitian chart

```text
H(m, delta, q_+) = H_base + m T_M + delta T_Delta + q_+ T_Q
```

with the existing chart constants

```text
gamma = 1/2
E1 = sqrt(8/3)
E2 = sqrt(8)/3
Q_Koide = 2/3
SELECTOR = sqrt(6)/3
```

The support proposal is the three-equation system

```text
Tr(H)       = Q_Koide
delta * q_+ = Q_Koide
det(H)      = E2
```

On the current active-chamber working surface, that system has a numerically
recovered interior solution

```text
(m_*, delta_*, q_+*) = (2/3, 0.9330511..., 0.7145018...)
```

and the PMNS observables extracted from `H(m_*, delta_*, q_+*)` lie in the
runner's current NuFit 5.3 normal-ordering `1 sigma` bands.

## Retained inputs vs proposed inputs

### Retained/chart-side inputs used directly

- the affine Hermitian chart `H_base, T_M, T_Delta, T_Q`;
- the chart constants `gamma, E1, E2`;
- the scalar identity `SELECTOR^2 = Q_Koide = 2/3`;
- the trace identity `Tr(H) = m`.

### Proposed inputs, not yet promoted

- `delta * q_+ = Q_Koide`;
- `det(H) = E2`.

These two equations are the live candidate selector laws. The support package
keeps them explicit as proposals rather than hiding them under retained
language.

## Executable content

The runner verifies four kinds of facts:

1. exact scalar/chart identities already present on the retained chart:

```text
SELECTOR^2 = Q_Koide
2 * SELECTOR / sqrt(3) = E2
Tr(H) = m
```

2. numerical solution of the proposed three-equation system;
3. chamber/signature/PMNS checks at the recovered point;
4. heuristic multi-start evidence that the audited search box returns one
   chamber cluster.

## Recovered point and observables

At the recovered point, the runner reports

```text
m     = 0.666666666666667
delta = 0.933051059...
q_+   = 0.714501805...
```

with

```text
sin^2(theta_12) = 0.306178
sin^2(theta_13) = 0.022139
sin^2(theta_23) = 0.543623
sin(delta_CP)   = -0.990477
|Jarlskog|      = 0.033084
```

## Why this is support, not closure

Three scientific gaps remain explicit:

1. The second and third equations are proposed selector laws, not retained
   derivations.
2. The uniqueness statement is based on a bounded multi-start search, not an
   analytic uniqueness theorem.
3. The broader PMNS/DM flagship gate remains open on the current package
   surface; this proposal gives one compact candidate law on the current chart
   but does not settle the remaining selector-side or sheet-choice obligations.

## What would promote this package

Promotion would require at least:

1. a retained derivation of `delta * q_+ = Q_Koide`;
2. a retained derivation of `det(H) = E2`;
3. a theorem-grade basin uniqueness argument;
4. integration with the remaining open PMNS/DM gate without overstating what is
   already closed elsewhere on the current package surface.

## Review-safe takeaway

The honest value of this package is narrow and useful:

```text
compact candidate law
+ strong numerical fit
+ clear open obligations
= worth retaining as support
```
