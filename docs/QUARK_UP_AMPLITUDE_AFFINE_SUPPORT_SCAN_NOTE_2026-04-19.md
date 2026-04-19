# Quark Up-Amplitude Affine-Support Scan

**Date:** 2026-04-19
**Status:** bounded affine-support scan on the exact-support reduced quark
closure surface
**Primary runner:** `scripts/frontier_quark_up_amplitude_affine_support_scan.py`

## Safe statement

The current branch still does **not** derive the remaining reduced up-sector
amplitude `a_u`.

But the support-side grammar can now be narrowed further.

After the earlier parameter audit and candidate scans, the next serious
question was:

> if we restrict to bounded exact affine-support laws centered on
> `a_u = sin(delta_std) * (c0 + c1 delta_A1)`, does the current projector /
> support machinery force one support-native law?

This scan answers that cleanly:

- **best affine refit law:** `sin(delta_std) * (6/7 - delta_A1/6)`
- **best affine anchored law:** `sin(delta_std) * (6/7 - delta_A1/sqrt(7))`
- **cleanest exact support law:** `sin(delta_std) * (1 - 6 delta_A1)`
- **bounded no-go:** no affine-support law in this bounded exact family beats
  both the external `7/9` refit baseline and the external `sqrt(3/5)`
  anchored baseline at once

So the quark lane now has a real bounded affine-support compression, but not a
retained derivation.

## Exact support anchor

This scan stays on the exact-support anchor isolated in
[QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md):

- `a_d = 1/sqrt(42)`
- `phi = -1/42 rad`
- `delta_A1(q_dem) = 1/42`
- `sin(delta_std) = sqrt(5/6)`

with the solved anchored reference value

```text
a_u = 0.778161628656
```

The point here is not to reopen a general expression search. It is to test the
smallest support-native exact family that the current notes already suggest.

## Bounded affine family

The runner uses three pieces of current exact quark/support structure:

1. exact projector magnitude `sin(delta_std) = sqrt(5/6)`
2. exact democratic support datum `delta_A1 = 1/42`
3. exact democratic noncentral support fraction `6/7 = 1 - 6 delta_A1`

It then scans a bounded affine-support family made of:

- the canonical support law `sin(delta_std) * (1 - 6 delta_A1)`
- the scalar-comparison variant `sin(delta_std) * (1 - sqrt(42) delta_A1)`
- centered affine laws `sin(delta_std) * (6/7 +/- k delta_A1)`

with the bounded exact coefficient shortlist

- `k = 1/7`
- `k = 1/6`
- `k = 1/sqrt(42)`
- `k = 1/sqrt(7)`
- `k = 1/sqrt(6)`
- `k = 6/7`
- `k = 1`

This is deliberately narrow. It is a support-native bounded grammar, not an
open numerology search.

## Main results

### Best affine refit law

The strongest affine law on the two-ratio refit score is

```text
a_u = sin(delta_std) * (6/7 - delta_A1/6)
    = sqrt(5/6) * (6/7 - 1/252)
    = 0.778838292749
```

It gives

- anchored CKM+`J` aggregate deviation: `0.892%`
- two-ratio refit objective: `0.052796`
- full-package max deviation after the two-ratio refit: `0.862%`

So the affine-support family already contains a refit law that is extremely
close to the current `7/9` baseline while remaining fully support-native.

### Best affine anchored law

The strongest affine law on the anchored CKM+`J` package is

```text
a_u = sin(delta_std) * (6/7 - delta_A1/sqrt(7))
    = 0.774245730253
```

It gives

- anchored aggregate CKM+`J` deviation: `0.723%`
- anchored max component deviation: `0.668%`
- full-package refit max deviation: `1.062%`

So the affine-support family also contains a very strong anchored law. But it
does not keep the full refit package below `1%`, so it does not dominate the
refit side.

### Cleanest exact support law

The structurally cleanest exact law is still

```text
a_u = sin(delta_std) * (1 - 6 delta_A1)
    = sin(delta_std) * (6/7)
    = 0.782460796436
```

This is the most literal support-native law because it uses the exact
democratic support fraction directly.

Numerically it remains strong:

- two-ratio refit objective: `0.055543`
- full-package refit max deviation: `0.928%`
- anchored CKM+`J` aggregate deviation: `1.106%`

So even the cleanest exact support law already keeps the refit package inside
`1%`.

### Scalar-comparison affine variant

The strongest nearby scalar-comparison law in the same affine language is

```text
a_u = sin(delta_std) * (1 - sqrt(42) delta_A1)
    = sin(delta_std) * (1 - 1/sqrt(42))
    = 0.772011886721
```

It gives anchored aggregate `0.742%` and anchored max deviation `0.612%`.

So the earlier projector/support-native shortlist survives the affine-support
restriction almost unchanged.

## Comparison against the external bounded baselines

The relevant bounded external baselines remain:

- **refit baseline:** `7/9`
- **anchored baseline:** `sqrt(3/5)`

On this branch:

- `7/9` still has the best current refit score
- `sqrt(3/5)` still has the best current anchored aggregate

The affine-support scan finds **no** law in its bounded exact family that
beats both of those at once.

That is the decisive negative result of this lane.

## Interpretation

This sharpens the quark endpoint again.

Before this scan, the honest statement was:

- the remaining freedom had been reduced to a bounded shortlist;
- the native expression family still split between different winners.

After this scan, the sharper statement is:

- the strongest support-native affine laws all sit on the exact `6/7` support
  base plus a small negative correction;
- one affine law is best for refit;
- a different affine law is best for the anchored package;
- even the cleanest exact support law is numerically strong;
- but no bounded affine-support law dominates the existing `7/9` and
  `sqrt(3/5)` baselines simultaneously.

So the current exact projector/support surface is now compressed to a very
small support-affine band, but still not forced to one theorem-grade law.

## Relation to the earlier notes

- [QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
  isolates the remaining scalar freedom on the exact-support anchor.
- [QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md)
  compresses that freedom to a bounded exact shortlist.
- [QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md)
  gives the earlier one-step native-expression no-go.
- This note is the bounded affine-support follow-on, focused only on the exact
  support grammar suggested by the tensor/support notes.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_affine_support_scan.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_affine_support_scan.py`: `PASS=7 FAIL=0`
