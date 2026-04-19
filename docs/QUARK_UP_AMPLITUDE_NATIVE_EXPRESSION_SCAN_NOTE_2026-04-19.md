# Quark Up-Amplitude Native-Expression Scan

**Date:** 2026-04-19
**Status:** bounded restricted native-grammar scan for the remaining reduced
quark amplitude law
**Primary runner:** `scripts/frontier_quark_up_amplitude_native_expression_scan.py`

## Safe statement

The current quark branch still does **not** derive the remaining reduced
up-sector amplitude `a_u`.

After the earlier candidate scan, the honest next question was narrower:

> if we restrict to one-step scalar expressions built only from the exact quark
> projector/support constants already promoted in the repo, does one native law
> emerge that dominates the bounded shortlist?

This note answers that question cleanly:

- **best native one-step refit law:** `atan(sqrt(5)) - sqrt(5)/6`
- **best native one-step anchored law:** `sqrt(5/6) * (1 - 1/sqrt(42))`
- **restricted no-go:** no native one-step expression beats both the external
  `7/9` refit baseline and the external `sqrt(3/5)` anchored baseline at once

So the exact projector/support family is sharper than before, but still not
forced to a single dominant law.

## Restricted grammar

The scan uses only the current exact projector/support constants already live
in the quark package:

- `rho = 1/sqrt(42)`
- `supp = 6/7`
- `pmag = sqrt(5/6)`
- `pphase = atan(sqrt(5))`
- `eta = sqrt(5)/6`
- `pr = sqrt(1/6)`

and the restricted one-step scalar grammar

```text
x
1 - x
x + y
x - y
x * y
x / y
sqrt(x * y)
```

with no deeper nesting.

This is deliberate. The point is to test the smallest semantically native
expression family already justified by the current quark atlas, not to do open
numerology.

## Main result

### Best native one-step refit law

The strongest native one-step law on the two-ratio refit score is

```text
a_u = atan(sqrt(5)) - sqrt(5)/6 = 0.777583995261
```

It gives

- `m_u/m_c`: `-0.917%`
- `m_c/m_t`: `-0.149%`
- `|V_us|`: `-0.000%`
- `|V_cb|`: `-0.004%`
- `|V_ub|`: `-0.070%`
- `J`: `-0.744%`

with full-package max deviation below `1%`.

So the native exact family already contains a strong refit law.

### Best native one-step anchored law

The strongest native one-step law on the anchored CKM+`J` package is

```text
a_u = sqrt(5/6) * (1 - 1/sqrt(42)) = 0.772011886721
```

It gives anchored aggregate CKM+`J` absolute deviation

```text
0.742%
```

with anchored max component deviation

```text
0.612%
```

So the native exact family also contains a very strong projector/support
dressing law.

### Cleanest structural projector/support instance

There is a second distinction worth keeping explicit.

The cleanest exact projector/support combination on the current note stack is

```text
a_u = sqrt(5/6) * (6/7)
    = sin(delta_std) * (1 - 6 delta_A1(q_dem))
```

because:

- `sqrt(5/6)` is the exact projector magnitude,
- `delta_A1(q_dem) = 1/42` is the exact democratic support datum,
- `6/7` is the exact democratic noncentral support fraction.

So this is the cleanest structurally native one-step affine support dressing.

But numerically it is **not** the strongest native law. It stays close, but the
restricted scan still prefers

- `atan(sqrt(5)) - sqrt(5)/6` on refit quality, and
- `sqrt(5/6) * (1 - 1/sqrt(42))` on anchored quality.

That is exactly why the native family still counts as bounded rather than
forced.

## Restricted no-go

The key negative result is the comparison against the external bounded
baselines already identified in the earlier candidate scan:

- `7/9` is still the strongest current refit baseline
- `sqrt(3/5)` is still the strongest current anchored baseline

The restricted native one-step scan finds **no** expression that beats both of
those at the same time.

That means the current native projector/support surface is still split:

- one native law is best for refit,
- another native law is best for the anchored package,
- and neither dominates the bounded shortlist outright.

This is the sharpest current bounded no-go on the remaining scalar.

## Interpretation

This is better than simply saying “one scalar remains free.”

The branch now supports three progressively sharper statements:

1. the reduced closure isolates the remaining freedom to one scalar `a_u`;
2. the widened exact-candidate scan compresses that scalar to a short shortlist;
3. the restricted native-expression scan shows that even the current exact
   projector/support grammar does not yet force a single dominant law.

So the remaining gap is no longer unconstrained, but it is still open.

## Relation to the earlier notes

- [QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
  isolates the remaining scalar.
- [QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md)
  compresses the scalar to a bounded exact shortlist.
- [QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md)
  is the follow-on widened affine-support no-go.
- This note is the follow-on restricted native-family no-go.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_native_expression_scan.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_native_expression_scan.py`: `PASS=5 FAIL=0`
