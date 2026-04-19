# Quark Up-Amplitude Two-Step Native Scan

**Date:** 2026-04-19
**Status:** bounded controlled two-step native-grammar scan for the remaining
reduced quark amplitude law
**Primary runner:** `scripts/frontier_quark_up_amplitude_two_step_native_scan.py`

## Safe statement

The reduced quark closure branch still does **not** derive the remaining
up-sector amplitude `a_u`.

But the one-step native scan left an obvious next question:

> if we allow exactly one more semantically native operation beyond the
> one-step projector/support grammar, does the reduced quark lane collapse to a
> single dominant exact law?

This note answers that directly:

- **best native two-step refit law:**
  `sqrt((1 - sqrt(5)/6) * (1 + sqrt(5)/6 - sqrt(1/6)))`
- **best native two-step anchored law:**
  `sqrt((1 - 1/sqrt(42)) * (1 - sqrt(1/6))) / sqrt(5/6)`
- **two-step persistence no-go:**
  no native two-step expression beats both the `7/9` refit baseline and the
  `sqrt(3/5)` anchored baseline at once

So the two-step native family is stronger than the one-step family, but it
still does **not** force one dominant `a_u` law.

## Controlled two-step grammar

The scan starts from the exact projector/support constants already live in the
current quark package:

- `1/sqrt(42)`
- `6/7`
- `sqrt(5/6)`
- `atan(sqrt(5))`
- `sqrt(5)/6`
- `sqrt(1/6)`

It first rebuilds the earlier one-step native family from

```text
x
1 - x
x + y
x - y
x * y
x / y
sqrt(x * y)
```

keeping only amplitudes in the physical band `0.3 < a_u < 1.2`.

Then it allows **one additional controlled step**:

```text
E -> 1 - E
E -> E ± p
E -> E * p
E -> E / p
E -> p / E
E -> sqrt(E * p)
```

where `E` is a one-step native expression and `p` is one native primitive or
positive complement.

That gives:

- `104` one-step native amplitudes
- `2712` distinct two-step native amplitudes in the allowed band

This is intentionally still restrictive. The point is to test the next exact
native family, not to open an unconstrained search.

## Main result

### Best native two-step refit law

The strongest native two-step law on the two-ratio refit score is

```text
a_u = sqrt((1 - sqrt(5)/6) * (1 + sqrt(5)/6 - sqrt(1/6)))
    = 0.777822586140
```

It gives

- anchored CKM+`J` aggregate deviation: `0.837%`
- anchored max component deviation: `0.758%`
- refit objective: `0.052747`
- full-package refit max deviation: `0.906%`

with refit deviations

- `m_u/m_c`: `-0.906%`
- `m_c/m_t`: `-0.150%`
- `|V_us|`: `-0.000%`
- `|V_cb|`: `-0.004%`
- `|V_ub|`: `-0.075%`
- `J`: `-0.753%`

So the native two-step family now slightly beats both the earlier native
one-step refit law and the external `7/9` refit baseline on the refit score.

### Best native two-step anchored law

The strongest native two-step law on the anchored CKM+`J` package is

```text
a_u = sqrt((1 - 1/sqrt(42)) * (1 - sqrt(1/6))) / sqrt(5/6)
    = 0.774939304779
```

It gives

- anchored CKM+`J` aggregate deviation: `0.717%`
- anchored max component deviation: `0.686%`
- refit objective: `0.054332`
- full-package refit max deviation: `1.032%`

with anchored component deviations

- `|V_us|`: `-0.027%`
- `|V_cb|`: `-0.003%`
- `|V_ub|`: `+0.002%`
- `J`: `-0.686%`

So the native two-step family now also beats both the earlier native one-step
anchored law and the external `sqrt(3/5)` anchored baseline on the anchored
package.

## What changed and what did not

The two-step scan does improve the bounded picture in a real way.

Compared with the one-step native scan:

- best native refit objective improves from `0.052782` to `0.052747`
- best native anchored aggregate improves from `0.742%` to `0.717%`

That is not noise-level in this workstream: the extra native step is doing real
work.

But the key structural fact does **not** change.

The best native two-step refit law and the best native two-step anchored law
are still different expressions. And more importantly:

```text
number of native two-step candidates with
  refit_obj < refit_obj(7/9)
  and
  anchor < anchor(sqrt(3/5))
= 0
```

So the current two-step native surface still does not produce one law that
dominates both external bounded baselines at once.

That is the clean persistence no-go.

## Interpretation

This sharpens the reduced quark status again.

The branch now supports the following progression:

1. the reduced closure isolates the remaining freedom to one scalar `a_u`;
2. the widened candidate scan compresses that scalar to a short exact shortlist;
3. the one-step native scan shows the current exact projector/support grammar
   still splits by axis;
4. the controlled two-step native scan shows that one extra native step
   improves both axes, but the split still persists.

So the remaining gap is smaller than before, but it is still open.

## Honest endpoint

The strongest current statement from this lane is:

- the native quark projector/support grammar remains competitive even after a
  second controlled step;
- it yields stronger native laws on both the refit axis and the anchored axis;
- but it still does not collapse to one dominant amplitude law;
- therefore the reduced up-sector closure remains **bounded**, not retained.

## Relation to the earlier notes

- [QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
  isolates the remaining scalar on the exact-support anchor.
- [QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md)
  gives the widened shortlist.
- [QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md)
  is the earlier one-step native-family no-go.
- This note is the one-more-step follow-on.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_two_step_native_scan.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_two_step_native_scan.py`: `PASS=5 FAIL=0`
