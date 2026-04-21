# Koide Selected-Line / Brannen Phase Orbit Bridge

**Date:** 2026-04-21  
**Status:** exact support theorem on the current constructive phase target  
**Runner:** `scripts/frontier_koide_selected_line_brannen_phase_orbit_bridge_2026_04_21.py`

## Question

The current constructive charged-lepton stack already sharpened the live
endpoint target to one cyclic-response phase

```text
theta = atan2(r2, r1)
```

on the exact selected line. Is that phase genuinely new, or is it already the
same phase variable that appears in the Brannen/circulant parameterization of
the charged-lepton amplitudes?

## Bottom line

It is the same phase variable.

More precisely:

- on the current selected-line slot order `(e, mu, tau)`,
  ```text
  theta = -arg(b_sel),
  ```
  where `b_sel` is the nontrivial `C_3` Fourier coefficient of the cyclic
  Hermitian target;
- on the standard Brannen order `(tau, e, mu)`,
  ```text
  delta = arg(b_std),
  ```
  where `delta` is the Brannen phase in
  ```text
  λ_k = a (1 + sqrt(2) cos(delta + 2 pi k / 3));
  ```
- the two Fourier coefficients differ by one exact `C_3` relabeling:
  ```text
  arg(b_sel) = delta + 2 pi / 3.
  ```

So on the current selected-line convention:

```text
theta = -(delta + 2 pi / 3)    (mod 2 pi).
```

This does **not** yet close the ambient `delta = 2/9` bridge. But it removes a
different ambiguity: the selected-line endpoint phase is not a second local
phase identification problem. It is already the Brannen phase variable, up to
fixed orbit bookkeeping.

## Input stack

This note combines:

1. [KOIDE_CIRCULANT_WILSON_TARGET_NOTE_2026-04-18.md](./KOIDE_CIRCULANT_WILSON_TARGET_NOTE_2026-04-18.md)
2. [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)
3. [KOIDE_SELECTED_LINE_CYCLIC_PHASE_TARGET_NOTE_2026-04-20.md](./KOIDE_SELECTED_LINE_CYCLIC_PHASE_TARGET_NOTE_2026-04-20.md)
4. [KOIDE_ONE_CLOCK_ENDPOINT_TARGET_THEOREM_NOTE_2026-04-20.md](./KOIDE_ONE_CLOCK_ENDPOINT_TARGET_THEOREM_NOTE_2026-04-20.md)

## Theorem 1: on the current selected-line order, `theta` is exactly the Fourier phase

For the current slot order `(u, v, w) = (e, mu, tau)`, define

```text
r1 = 2u - v - w,
r2 = sqrt(3) (v - w),
b_sel = (u + ω̄ v + ω w) / 3.
```

Then the runner verifies exactly:

```text
Re(b_sel) = r1 / 6,
Im(b_sel) = -r2 / 6.
```

So the selected-line phase

```text
theta = atan2(r2, r1)
```

is not a new free angle. It is exactly the negative Fourier phase:

```text
theta = -arg(b_sel)    (mod 2 pi).
```

## Theorem 2: the standard Brannen phase is the same Fourier phase on the standard order

Write the Brannen amplitudes in the standard order `(tau, e, mu)`:

```text
λ_tau = a (1 + sqrt(2) cos(delta)),
λ_e   = a (1 + sqrt(2) cos(delta + 2 pi / 3)),
λ_mu  = a (1 + sqrt(2) cos(delta + 4 pi / 3)).
```

Then the nontrivial Fourier coefficient on that standard order is

```text
b_std = (λ_tau + ω̄ λ_e + ω λ_mu) / 3
      = (a / sqrt(2)) exp(i delta).
```

So `delta` is exactly the Fourier phase in the standard Brannen labeling.

## Corollary: the current selected-line phase differs only by one exact `C_3` relabeling

The current selected-line packet uses the cyclic order `(e, mu, tau)`, which is
the one-step `C_3` rotation of the standard Brannen order `(tau, e, mu)`.

The same Fourier coefficient on that current order becomes

```text
b_sel = (a / sqrt(2)) exp(i (delta + 2 pi / 3)).
```

Combining with Theorem 1:

```text
theta = -arg(b_sel) = -(delta + 2 pi / 3)    (mod 2 pi).
```

So the selected-line phase target and the Brannen phase are not independent
phase observables. They are the same `C_3` phase, written in two fixed order
conventions.

## Numerical check on the live charged-lepton target

Using the PDG `sqrt(m)` amplitudes:

- the standard Brannen-order Fourier phase is
  ```text
  delta_fit ~= 0.222229631490,
  ```
  numerically close to `2/9`;
- the current selected-order phase is
  ```text
  theta_pdg ~= -2.316624733883;
  ```
- the runner verifies
  ```text
  theta_pdg + delta_fit + 2 pi / 3 = 0
  ```
  up to numerical precision.

It also compares that phase with the current selected-line witness point from
the existing one-clock route and finds

```text
theta_* ~= -2.316624963970,
```

matching the PDG selected-order phase at the `10^-7` scale.

So the new bridge is not only formal. It lands exactly on the live endpoint
target already isolated on current `main`.

## What this changes

This note does **not** yet derive the final ambient law selecting `delta`.

It does something narrower but useful:

- it identifies the selected-line endpoint phase with the same Fourier/Brannen
  phase variable already present in the cyclic Hermitian target,
- it shows that the current slot orientation adds only a fixed minus sign,
- and it shows that the current selected-line convention differs from the
  standard Brannen convention by only one exact `C_3` cycle shift.

So the remaining open physical bridge is now sharper:

```text
ambient law for delta
  -> fixed orbit bookkeeping
  -> selected-line target phase theta
  -> selected endpoint.
```

The branch no longer needs a second independent local-selected-line phase
identification beyond that.

## Scope boundary

This note does **not** claim:

- that the ambient APS invariant is already the physical Brannen phase,
- that the `delta = 2/9` support route is fully closed,
- or that charged leptons are retained closed on current `main`.

It only proves that once the physical Brannen phase is fixed, the current
selected-line cyclic phase target is fixed automatically by exact `C_3` orbit
bookkeeping.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_selected_line_brannen_phase_orbit_bridge_2026_04_21.py
```
