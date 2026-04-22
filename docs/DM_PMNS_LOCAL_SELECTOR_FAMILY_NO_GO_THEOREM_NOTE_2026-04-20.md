# DM PMNS Local-Selector-Family No-Go Theorem

**Date:** 2026-04-20  
**Status:** exact no-go for the current exact local selector families on the
remaining PMNS angle pin  
**Scope:** closes a named family of `I5`-style angle-pin attempts:
the current exact local parity-compatible / `23`-symmetric / microscopic-
polynomial selector routes do not force the physical PMNS angle triple  
**Does not close:** a future nonlocal point-selection law on the live branch  
**Dedicated verifier:**  
`scripts/frontier_dm_pmns_local_selector_family_no_go_theorem_2026_04_20.py`

## Summary

The current exact local selector families already on land reduce to the same
one-real selected line on the active DM source surface:

```text
delta = q_+ = sqrt(6)/3.
```

This follows from two exact inputs already in the atlas:

1. the parity-compatible observable-selector theorem on the full local
   family `D = diag(A,B,B)`, which selects `delta_* = q_+* = sqrt(6)/3`;
2. the active-curvature `23`-symmetric baseline theorem, which shows the
   broader Euclidean local family is exactly `D = diag(A,B,B)` and gives
   the same chamber minimizer `delta_* = q_+* = sqrt(6)/3` for every
   `A,B > 0`.

So the strongest current exact local route is not a 2-real selector any more.
It is the one-real Schur line

```text
L_S = { H(m, sqrt(6)/3, sqrt(6)/3) : m in R }.
```

The theorem here is that **the physical PMNS angle triple is not on that
line**.

## Inputs

### P1. Local-family reduction to the Schur line

Per:

- [DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_CURVATURE_23_SYMMETRIC_BASELINE_BOUNDARY_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_CURVATURE_23_SYMMETRIC_BASELINE_BOUNDARY_THEOREM_NOTE_2026-04-17.md)

the current exact local selector families select

```text
delta_* = q_+* = sqrt(6)/3.
```

### P2. Retained PMNS map

Per:

- [PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md](./PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md)

the PMNS observables are explicit functions of `H(m, delta, q_+)`, hence
explicit on `L_S`.

### P3. Physical target triple

The active PMNS target remains

```text
(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
  = (0.307, 0.0218, 0.545).
```

## Theorem statement

**Theorem (current exact local selector families do not close the PMNS angle
pin).** Let

```text
S = sqrt(6)/3,
L_S = { H(m,S,S) : m in R }.
```

Then:

1. `sin^2 theta_12(m,S,S)` has exactly two stationary points on the wide scan
   interval `[-2000,2000]`. Its global minimum on that interval occurs at

   ```text
   m_solar,min ~= 4.365005345286
   ```

   and equals

   ```text
   sin^2 theta_12,min = 0.331582718643... > 0.307.
   ```

   Therefore no point on `L_S` can realize the physical PMNS angle triple.

2. The full three-angle distance

   ```text
   chi^2_line(m)
     = (s12^2 - 0.307)^2 + (s13^2 - 0.0218)^2 + (s23^2 - 0.545)^2
   ```

   has a unique stationary point on `[-200,200]`, at

   ```text
   m_best ~= 1.278322119585,
   chi^2_line,min = 0.011428083950...
   ```

   with best-fit triple

   ```text
   (0.37920275, 0.05563746, 0.47379695).
   ```

3. The current explicit local candidate points

   ```text
   {Schur-Q, det-crit, Tr(H^2)-boundary, K12-character, F1 parity-mixing}
   ```

   all miss the physical PMNS triple by visible margins; every one has
   `max |angle error| > 0.05` and `chi^2 > 0.03`.

Hence the current exact local selector families do **not** close the remaining
PMNS angle pin. The missing ingredient is a **nonlocal point-selection law on
the live branch**, not another local parity-compatible / `23`-symmetric /
microscopic-polynomial selector.

## Proof sketch

### 1. The current exact local routes have already collapsed to one line

The parity-compatible theorem derives `delta_* = q_+* = sqrt(6)/3` on the
full local family `D = diag(A,B,B)`. The `23`-symmetric active-curvature
theorem then shows that this is already the full Euclidean local family on the
active pair, not just the scalar subfamily.

So the local selector problem is no longer a two-real search over
`(delta,q_+)`. It has reduced to a one-real line `L_S`.

### 2. The Schur line misses already at the solar angle

The verifier computes the PMNS map on `L_S` and numerically isolates the
stationary set of `sin^2 theta_12(m,S,S)` on a wide interval `[-2000,2000]`.
There are exactly two stationary points:

- a local maximum near `m ~= -0.41013790`,
- and a local minimum near `m ~= 4.36500535`.

At that minimum:

```text
sin^2 theta_12,min = 0.331582718643...
```

which is strictly above the physical target

```text
0.331582718643... - 0.307 = 0.024582718643... > 0.
```

So the Schur line is excluded before even imposing the reactor and atmospheric
angles.

### 3. The best full fit still misses visibly

The same verifier computes the full three-angle line distance
`chi^2_line(m)` and finds a unique stationary point on `[-200,200]`, at

```text
m_best ~= 1.278322119585.
```

At this best-fit point:

```text
chi^2_line,min = 0.011428083950...
```

with PMNS triple

```text
(0.37920275, 0.05563746, 0.47379695),
```

which is visibly displaced from the physical target.

### 4. The explicit current candidate points also all miss

The verifier checks the current explicit local candidate points from the
existing selector-obstruction stack:

| candidate | `(m, delta, q_+)` | `chi^2` | largest angle error |
|---|---|---:|---:|
| Schur-Q | `(0.5, 0.8165, 0.8165)` | `0.06280` | `0.25057` |
| det-crit | `(0.613, 0.964, 1.552)` | `0.03113` | `0.15544` |
| `Tr(H^2)` boundary | `(0.385, 1.268, 0.365)` | `0.08696` | `0.21848` |
| `K12` character | `(0.0, 0.8, 1.0)` | `0.25719` | `0.50457` |
| F1 parity-mixing | `(0.62854, 1.14618, 0.48682)` | `0.04655` | `0.20500` |

So the miss is not an artifact of one particular point choice. It persists
across the whole current local-selector packet.

## Consequence for the remaining PMNS angle pin

The remaining PMNS angle task is now sharper:

- the current exact local selector families are **not enough**;
- the missing ingredient is **not** another local Euclidean-curvature or
  microscopic-polynomial selector;
- the remaining target is a **nonlocal point-selection law** on the live
  branch.

So the honest status is:

```text
I5 is still open positively,
but the current exact local selector families are now closed negatively.
```

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_local_selector_family_no_go_theorem_2026_04_20.py
```

Expected:

```text
PASS=15 FAIL=0
```
