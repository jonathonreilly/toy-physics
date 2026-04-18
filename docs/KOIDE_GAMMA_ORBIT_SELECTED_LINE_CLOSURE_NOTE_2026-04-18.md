# Koide `Gamma`-Orbit Selected-Line Closure

**Date:** 2026-04-18  
**Status:** closes the remaining free coordinates on the current positive
candidate route  
**Runner:** `scripts/frontier_koide_gamma_orbit_selected_line_closure.py`

## Question

The positive Koide route had already been reduced to:

1. the exact full-cube `Gamma_i` orbit law;
2. the exact orbit-slot Koide cone;
3. the exact positive one-clock semigroup class;
4. the exact selected generator line
   ```text
   G_m = H(m, sqrt(6)/3, sqrt(6)/3).
   ```

At that stage two live coordinates remained:

- the line parameter `m`;
- the branch choice on
  ```text
  u = 2(v+w) ± sqrt(3(v^2 + 4vw + w^2)).
  ```

Can those be closed cleanly on the current positive route?

## Bottom line

Yes.

The branch is fixed by continuity from the exact positivity threshold on the
selected line, and the line parameter `m` is fixed by the **first continuous
hit** of the route-invariant reachable-slot ratio `r = w/v` of the earlier
`H_*` one-clock witness.

So the current positive candidate route is now **coordinate-closed**.

There are no free internal parameters left on this lane.

## Input stack

This note closes the gap left by:

1. [KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md)
2. [KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md)
3. [KOIDE_GAMMA_ORBIT_EXPONENTIAL_VALUE_LAW_CANDIDATE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_EXPONENTIAL_VALUE_LAW_CANDIDATE_NOTE_2026-04-18.md)

## Theorem 1: on the Koide cone, small-branch direction is fixed by the reachable-slot ratio

Write
```text
r = w / v.
```

On the small branch of the exact orbit-slot cone,
```text
u = 2(v+w) - sqrt(3(v^2 + 4vw + w^2)).
```

Dividing by `v` gives
```text
u / v = 2(1+r) - sqrt(3(1 + 4r + r^2)).
```

So the normalized amplitude direction depends only on the single scale-free
ratio `r = w/v`.

That is exact.

## Corollary 1: matching one ratio matches the full direction

If two small-branch Koide triples have the same ratio `r = w/v`, then they have
the same normalized amplitude direction.

So once the current route has been reduced to the Koide cone plus the selected
line, one scalar ratio is enough to fix the full direction.

## Theorem 2: the physical branch is the continuity branch from the exact positivity threshold

On the selected line `G_m`, the small branch crosses zero at one threshold
```text
m_pos ~= -1.2957949.
```

At that threshold,
```text
u_- = 0.
```

Substituting `u = 0` into the exact cone gives
```text
v^2 + w^2 = 4vw,
```
so with `w > v`,
```text
w / v = 2 + sqrt(3).
```

The large branch does **not** vanish there; it stays finitely positive.
Therefore the only branch that turns on continuously from zero support is the
small branch.

So continuity from the exact threshold fixes the branch.

## Theorem 3: the selected line closes at the first hit of the earlier `H_*` witness ratio

The earlier positive semigroup witness on the `H_*` route carries one exact
scale-free reachable-slot ratio
```text
r_* = w_* / v_* ~= 4.100904169382.
```

On the selected line, the ratio function
```text
r(m) = w(m) / v(m)
```
is numerically strictly increasing from the positivity threshold up to the
turnover window containing the first witness hit.

Numerically, the full line hits `r_*` twice:
```text
m_first ~= -1.16046947,
m_late  ~=  1.82321485.
```

By Corollary 1, that single equality already reproduces the full small-branch
direction at either hit.

The physically cleaner point is the **first hit**:

- it is reached by monotone continuation from the positivity threshold;
- it is the least-amplified realization of the witness ratio on the selected
  line;
- the later hit appears only after passing the turnover and returning to the
  same ratio with a much larger one-clock block.

So the selected physical point is
```text
m_* = m_first ~= -1.16046947.
```

## Consequence

The current positive route is now coordinate-closed:

1. the exact selector theorem fixes `delta = q_+ = sqrt(6)/3`;
2. the exact one-clock law fixes the semigroup class;
3. threshold continuity fixes the small branch;
4. the preserved reachable-slot ratio fixes `m` at the first monotone hit on
   the selected line.

So there are no free internal coordinates left on this candidate route.

## Closed witness

At the closed point:
```text
m_* ~= -1.16046947,
```
the small-branch selected-line amplitudes are
```text
(u_*, v_*, w_*) ~= (0.105597, 1.518730, 6.228174),
```
which lie exactly on the Koide cone and reproduce the same normalized direction
as the earlier `H_*` witness.

After one overall scale fit, the amplitudes are
```text
(0.714689, 10.278901, 42.152850),
```
within `0.03%` of the PDG `sqrt(m)` values.

## What is now actually open

The remaining open issue is no longer parameter selection *inside* the current
positive route.

That part is done.

What remains open is promotion:

1. replace the earlier `H_*` witness input by a retained charged-lepton law for
   the single scalar bridge
   `kappa = sqrt(3) r2 / (2 r0 - r1) = (v-w)/(v+w)`;
2. or formally accept the current first-hit bridge as a new primitive if that
   is the intended extension.

So the science burden has shifted from “find the missing coordinate law” to
“decide whether this candidate route is to be promoted.”

The companion
[KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md](./KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md)
sharpens that statement further: the remaining charged-lepton promotion target
is only one scalar retained law for `kappa_*`.

The newer companion
[KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md)
sharpens it one step further again: on the exact selected slice
`delta = q_+ = sqrt(6)/3`, that bridge is equivalent to one microscopic scalar
selector law for `m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3`.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_gamma_orbit_selected_line_closure.py
```
