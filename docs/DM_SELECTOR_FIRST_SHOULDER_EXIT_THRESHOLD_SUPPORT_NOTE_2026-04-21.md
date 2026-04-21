# DM Selector First-Shoulder-Exit Threshold Support Note

**Date:** 2026-04-21  
**Status:** selector-side support theorem on the open DM gate  
**Primary runner:** `scripts/frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21.py`

## Statement

The exact intrinsic threshold-volume selector family now contains a genuinely
canonical breakpoint candidate, not just a broad stabilization interval.

For each recovered lift, let

```text
tau_b(i) = log(1 + b_i)
```

where `b_i` is the middle inverse eigenvalue of the common-shifted positive
comparison window `A_mu(H_i)`.

Then on the recovered bank:

1. the minimum of `tau_b(i)` is unique;
2. it belongs to the preferred recovered lift `0`;
3. it lies inside the previously certified stabilization window;
4. evaluating the exact threshold-volume field at this breakpoint already
   makes the preferred recovered lift the unique minimizer.

So the selector-side burden is now narrower than “derive some threshold law in
the stabilization interval.” There is already one canonical breakpoint
candidate inside that interval.

## Relation to the earlier selector results

### Earlier nonrealization result

The earlier note
`docs/DM_NEUTRINO_SOURCE_SURFACE_ATOMIC_WITNESS_VOLUME_SELECTOR_NONREALIZATION_NOTE_2026-04-18.md`
proved:

- the canonical full-family witness-volume field `V_tau(H)` is exact and
  intrinsic;
- but the current exact bank does not force one unique threshold, since
  `tau = 0.13` chooses recovered lift `1` and `tau = 0.14` chooses lift `0`.

That reduced the missing datum to an intrinsic threshold law.

### Earlier stabilization result

The later note
`docs/DM_SELECTOR_THRESHOLD_STABILIZATION_SUPPORT_THEOREM_NOTE_2026-04-21.md`
proved:

- there is an exact stabilization onset
  `tau_star = 0.131637578221552...`;
- above `tau_star`, the preferred recovered lift becomes the unique minimizer;
- it remains unique until the next zero-volume tie at
  `0.271641142726493...`.

That reduced the selector burden to a threshold law landing in this window.

## New breakpoint result

### Intrinsic middle-branch thresholds

Because the exact piecewise witness-volume formula is

```text
V_tau(H) = 1                                  for c <= g
V_tau(H) = 1 - (c-g)^2 / ((a-g)(b-g))         for g < c <= b
V_tau(H) = (a-c)^2 / ((a-b)(a-g))             for b < c < a
V_tau(H) = 0                                  for c >= a
```

with `c = exp(tau) - 1`, every recovered lift carries a canonical middle-branch
breakpoint

```text
tau_b = log(1 + b).
```

On the recovered bank these are:

```text
lift 0: 0.148036252277635
lift 1: 0.176381906802132
lift 2: 0.177376441792114
lift 3: 0.171204804996079
lift 4: 0.160534730480452
```

So the earliest such breakpoint is

```text
tau_b,min = 0.148036252277635,
```

and it belongs uniquely to the preferred recovered lift `0`.

### Placement inside the stabilization window

This canonical breakpoint satisfies

```text
tau_star < tau_b,min < tau_zero(next),
```

numerically

```text
0.131637578221552 < 0.148036252277635 < 0.271641142726493.
```

So it lies strictly inside the previously certified stabilization window.

### Selection consequence

Evaluating the exact threshold-volume field at `tau_b,min` gives

```text
V_tau_b,min =
  (0.72425153, 0.87034280, 0.88320396, 0.92614267, 0.99161327),
```

so the preferred recovered lift is already the unique minimizer there.

## Consequence

This still does not close the selector law.

It does mean that the selector-side burden has narrowed again:

- before: derive an intrinsic threshold law;
- then: derive a threshold law landing in the stabilization window;
- now: derive why the physical threshold law is the earliest middle-branch
  breakpoint `tau_b,min`, or else derive a stronger microscopic selector law
  that bypasses the threshold-volume family.

So the current exact family already supplies one canonical threshold candidate.

## Boundary

This is a support theorem only.

It does **not** prove that the physical threshold law must be

```text
tau_phys = tau_b,min.
```

It proves only that `tau_b,min` is now the cleanest intrinsic selector
candidate already present on the exact family.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21.py
```

Expected:

```text
PASS=11 FAIL=0
```
