# Koide `Gamma`-Orbit Observable-Selector Generator Line

**Date:** 2026-04-18  
**Status:** exact reduction of the one-clock generator search to a one-real
line, plus a positive charged-lepton witness on that line  
**Runner:** `scripts/frontier_koide_gamma_orbit_observable_selector_generator_line.py`

## Question

After the exact full-cube orbit law and the exact positive one-clock semigroup
reduction, the live Koide target became:

```text
derive the charged-lepton generator G and the physical cone branch.
```

Can the repo’s exact observable-selector theorem collapse that generator search
further without going negative first?

## Bottom line

Yes.

If the generator is taken inside the native affine Hermitian chart
```text
H(m, delta, q_+),
```
and the exact parity-compatible observable-selector theorem is imposed, then
the active pair is fixed exactly at
```text
delta_* = q_+* = sqrt(6)/3.
```

So the selected generator family is not a three-real chart anymore. It is the
one-real line
```text
G_m = H(m, sqrt(6)/3, sqrt(6)/3),
```
once one-clock normalization is used.

That line already contains a near-perfect charged-lepton witness at
```text
m_* ~= -1.1604674
```
on the small cone branch, with direction cosine
```text
0.999999999989
```
against the PDG `sqrt(m)` direction and maximum relative amplitude error below
`0.03%` after one overall scale fit.

So the live positive target is now sharper again:

```text
derive the m-selection law and the branch selector.
```

## Input stack

This note combines three earlier exact pieces:

1. the exact parity-compatible observable-selector theorem
   [DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md)
2. the exact full-cube `Gamma_i` orbit law
   [KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md](./KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md)
3. the exact positive one-clock semigroup reduction
   [KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md)

## Theorem 1: the exact observable selector fixes the active pair

On the exact parity-compatible diagonal baseline route, the observable-principle
selector minimizes
```text
delta^2 + q_+^2
```
on the exact source boundary
```text
q_+ = sqrt(8/3) - delta.
```

This gives the unique stationary point
```text
delta_* = q_+* = sqrt(6)/3.
```

That part is already exact in the April 17 theorem.

## Corollary 1: on the affine Hermitian chart, the selected family is a one-real line

Inside the live affine chart
```text
H(m, delta, q_+),
```
Theorem 1 forces
```text
delta = q_+ = sqrt(6)/3.
```

So the generator search collapses to
```text
H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3).
```

That is one real shape parameter `m`.

## Corollary 2: one-clock normalization removes the extra semigroup scale

The positive one-clock semigroup note already proved that the microscopic law is
fully determined by the physical one-clock block `X_1`.

So once the selected generator is inserted into the one-clock law, the search
family can be written simply as
```text
X_1(m) = exp(H_sel(m)).
```

That is why the selected generator family is a genuine one-real line on the
present positive route.

## Charged-lepton witness on the exact line

Read the exact reachable slot values from the one-clock block:
```text
v(m) = [exp(H_sel(m))]_(110,110),
w(m) = [exp(H_sel(m))]_(101,101).
```

Then the exact orbit-slot Koide selector fixes the `O_0` slot:
```text
u(m) = 2(v+w) ± sqrt(3(v^2 + 4vw + w^2)).
```

On the small branch:

- positivity turns on at
  ```text
  m_pos ~= -1.2957949;
  ```
- the best charged-lepton direction fit occurs at
  ```text
  m_* ~= -1.1604674.
  ```

At that point:
```text
(u_*, v_*, w_*) ~= (0.105597, 1.518730, 6.228174),
```
which lies exactly on the Koide cone and has direction cosine
```text
0.999999999989
```
against the PDG `sqrt(m)` direction.

After one overall scale fit, the predicted amplitudes are:
```text
(0.714689, 10.278901, 42.152850),
```
with maximum relative deviation below `0.03%`.

So the exact selected generator line is not empty. It already contains the
charged-lepton witness.

## Why this is a real positive advance

Before this step, the live open target on the semigroup route was:

```text
choose a Hermitian generator G and a branch.
```

After this step it is:

```text
choose one real line parameter m and a branch.
```

That is a genuine reduction in the science burden.

It also stays on the user’s preferred positive track:

- full-cube / `3+1` route stays explicit;
- no obstruction note is needed to get here;
- the reduction comes from an exact selector theorem already in the tree;
- the selected line already contains the observed charged-lepton witness.

## What remains open

This note does **not** yet close the remaining free coordinates by itself.

The companion closure note
[KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md)
finishes that part of the current positive route:

1. the small branch is fixed by continuity from the exact positivity threshold;
2. `m` is fixed uniquely by matching the preserved reachable-slot ratio of the
   earlier `H_*` witness;
3. so the current positive candidate route becomes coordinate-closed.

What remains after that is only promotion beyond the current candidate route:

1. replace the earlier `H_*` witness input by a retained charged-lepton law;
2. or explicitly accept that bridge as a new primitive if that is the intended
   extension.

## Consequence

The Koide lane is still on a good positive track, and it is narrower than it
was one step ago.

The exact selector plus the exact one-clock reduction collapse the generator
problem to a one-real line. The companion closure note then fixes both `m` and
the branch on that line. So the next singular target is no longer internal
coordinate selection. It is:

```text
decide whether to promote the coordinate-closed positive route beyond candidate status.
```

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_gamma_orbit_observable_selector_generator_line.py
```
